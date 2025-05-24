try:
    import redis
    import redis.asyncio as aioredis

    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False
    redis = None
    aioredis = None

import json
import uuid
import asyncio
from typing import Optional, Dict, Any
from datetime import datetime
import logging
from collections import deque
from audio_api.models import (
    AudioRequest,
    BatchAudioRequest,
    AudioResponse,
    BatchAudioResponse,
)
from audio_api.config import get_config, AudioConfig

logger = logging.getLogger(__name__)


class QueueServiceError(Exception):
    """Base exception for queue service operations."""

    pass


class QueueService:
    def __init__(self, use_redis: bool = False, config: Optional[AudioConfig] = None):
        """
        Initialize queue service with optional Redis backend and connection pooling.

        Args:
            use_redis: If True, use Redis for persistent queuing. If False, use in-memory queuing.
            config: Configuration instance (uses global config if None)
        """
        self.config = config or get_config()
        self.use_redis = use_redis
        self._redis_pool: Optional[aioredis.ConnectionPool] = None
        self._redis_client: Optional[aioredis.Redis] = None
        self._is_closed = False

        if use_redis:
            if not REDIS_AVAILABLE:
                raise QueueServiceError(
                    "Redis is not installed. Install with: pip install redis"
                )
            self._initialize_redis_pool()
            self.task_queue = "audio_tasks"
            self.result_prefix = "result:"
            self.batch_prefix = "batch:"
        else:
            # In-memory storage
            self._task_queue = deque()
            self._results = {}
            self._batches = {}
            logger.info("Using in-memory queue (non-persistent)")

    def _initialize_redis_pool(self):
        """Initialize Redis connection pool."""
        try:
            self._redis_pool = aioredis.ConnectionPool.from_url(
                self.config.redis_url,
                max_connections=self.config.redis_pool_size,
                decode_responses=True,
                retry_on_timeout=True,
                health_check_interval=30,
            )
            self._redis_client = aioredis.Redis(connection_pool=self._redis_pool)
            logger.info(
                f"Initialized Redis connection pool with {self.config.redis_pool_size} connections"
            )
        except Exception as e:
            logger.error(f"Failed to initialize Redis pool: {str(e)}")
            raise QueueServiceError(f"Redis initialization failed: {str(e)}")

    async def health_check(self) -> bool:
        """Check if the queue service is healthy."""
        try:
            if self.use_redis:
                if self._redis_client is None:
                    return False
                await self._redis_client.ping()
                return True
            else:
                return not self._is_closed
        except Exception as e:
            logger.error(f"Health check failed: {str(e)}")
            return False

    async def __aenter__(self):
        """Async context manager entry."""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit with cleanup."""
        await self.close()

    async def close(self):
        """Close Redis connections and cleanup resources."""
        if self._is_closed:
            return

        self._is_closed = True

        if self.use_redis and self._redis_pool:
            try:
                await self._redis_pool.disconnect()
                logger.info("Redis connection pool closed")
            except Exception as e:
                logger.error(f"Error closing Redis pool: {str(e)}")

    async def enqueue_single_task(self, request: AudioRequest) -> str:
        """Enqueue a single audio generation task with improved error handling."""
        if self._is_closed:
            raise QueueServiceError("Queue service is closed")

        try:
            task_id = str(uuid.uuid4())
            task_data = {
                "task_id": task_id,
                "request": request.model_dump(),
                "created_at": datetime.utcnow().isoformat(),
                "status": "pending",
                "priority": getattr(
                    request, "priority", 0
                ),  # Support for future priority feature
            }

            if self.use_redis:
                if not await self.health_check():
                    raise QueueServiceError("Redis connection is not healthy")

                # Use async Redis operations
                async with self._redis_client.pipeline(transaction=True) as pipe:
                    await pipe.lpush(self.task_queue, json.dumps(task_data))
                    await pipe.setex(
                        f"{self.result_prefix}{task_id}",
                        3600,  # 1 hour TTL
                        json.dumps(
                            {
                                "status": "pending",
                                "created_at": task_data["created_at"],
                                "enqueued_at": datetime.utcnow().isoformat(),
                            }
                        ),
                    )
                    await pipe.execute()
            else:
                # In-memory backend
                self._task_queue.appendleft(task_data)
                self._results[task_id] = {
                    "status": "pending",
                    "created_at": task_data["created_at"],
                    "enqueued_at": datetime.utcnow().isoformat(),
                }

            logger.info(
                f"Enqueued task {task_id} ({'Redis' if self.use_redis else 'memory'}), "
                f"text_length={len(request.text)}"
            )
            return task_id

        except QueueServiceError:
            raise
        except Exception as e:
            logger.error(f"Error enqueuing task: {str(e)}")
            raise QueueServiceError(f"Failed to enqueue task: {str(e)}")

    async def enqueue_batch_tasks(self, batch_request: BatchAudioRequest) -> str:
        """Enqueue multiple audio generation tasks as a batch."""
        try:
            batch_id = batch_request.batch_id or str(uuid.uuid4())
            task_ids = []

            # Create individual tasks
            for request in batch_request.requests:
                task_id = str(uuid.uuid4())
                task_data = {
                    "task_id": task_id,
                    "batch_id": batch_id,
                    "request": request.model_dump(),
                    "created_at": datetime.utcnow().isoformat(),
                    "status": "pending",
                }

                if self.use_redis:
                    # Redis backend
                    await asyncio.to_thread(
                        self.redis_client.lpush, self.task_queue, json.dumps(task_data)
                    )
                else:
                    # In-memory backend
                    self._task_queue.appendleft(task_data)

                task_ids.append(task_id)

            # Store batch metadata
            batch_data = {
                "batch_id": batch_id,
                "task_ids": task_ids,
                "total_requests": len(batch_request.requests),
                "completed": 0,
                "failed": 0,
                "status": "pending",
                "created_at": datetime.utcnow().isoformat(),
            }

            if self.use_redis:
                # Redis backend
                await asyncio.to_thread(
                    self.redis_client.setex,
                    f"{self.batch_prefix}{batch_id}",
                    3600,  # 1 hour TTL
                    json.dumps(batch_data),
                )
            else:
                # In-memory backend
                self._batches[batch_id] = batch_data

            logger.info(
                f"Enqueued batch {batch_id} with {len(task_ids)} tasks ({'Redis' if self.use_redis else 'memory'})"
            )
            return batch_id

        except Exception as e:
            logger.error(f"Error enqueuing batch: {str(e)}")
            raise

    async def dequeue_task(self) -> Optional[Dict[str, Any]]:
        """Dequeue a task from the queue with improved error handling."""
        if self._is_closed:
            return None

        try:
            if self.use_redis:
                if not await self.health_check():
                    logger.warning("Redis connection unhealthy, skipping dequeue")
                    return None

                # Use async Redis operations with timeout
                result = await self._redis_client.brpop(self.task_queue, timeout=1)
                if result:
                    _, task_data = result
                    task = json.loads(task_data)
                    logger.debug(f"Dequeued task {task.get('task_id', 'unknown')}")
                    return task
                return None
            else:
                # In-memory backend
                if self._task_queue:
                    task = self._task_queue.pop()
                    logger.debug(
                        f"Dequeued task {task.get('task_id', 'unknown')} from memory"
                    )
                    return task
                return None

        except Exception as e:
            logger.error(f"Error dequeuing task: {str(e)}")
            return None

    async def update_task_result(self, task_id: str, result: AudioResponse):
        """Update task result with improved error handling."""
        if self._is_closed:
            raise QueueServiceError("Queue service is closed")

        try:
            result_data = {
                "task_id": task_id,
                "result": result.model_dump(),
                "completed_at": datetime.utcnow().isoformat(),
                "status": "completed" if result.success else "failed",
                "processing_time": getattr(result, "processing_time", None),
            }

            if self.use_redis:
                if not await self.health_check():
                    raise QueueServiceError("Redis connection is not healthy")

                # Use async Redis operations
                await self._redis_client.setex(
                    f"{self.result_prefix}{task_id}",
                    3600,  # 1 hour TTL
                    json.dumps(result_data),
                )
            else:
                # In-memory backend
                self._results[task_id] = result_data

            status = "completed" if result.success else "failed"
            logger.info(f"Updated result for task {task_id}: {status}")

        except QueueServiceError:
            raise
        except Exception as e:
            logger.error(f"Error updating task result: {str(e)}")
            raise QueueServiceError(f"Failed to update task result: {str(e)}")

    async def update_batch_progress(self, batch_id: str, task_id: str, success: bool):
        """Update batch progress when a task completes."""
        try:
            if self.use_redis:
                # Redis backend
                batch_key = f"{self.batch_prefix}{batch_id}"
                batch_data_str = await asyncio.to_thread(
                    self.redis_client.get, batch_key
                )
                if not batch_data_str:
                    logger.warning(f"Batch {batch_id} not found")
                    return
                batch_data = json.loads(batch_data_str)
            else:
                # In-memory backend
                batch_data = self._batches.get(batch_id)
                if not batch_data:
                    logger.warning(f"Batch {batch_id} not found")
                    return

            if success:
                batch_data["completed"] += 1
            else:
                batch_data["failed"] += 1

            # Update status
            total_processed = batch_data["completed"] + batch_data["failed"]
            if total_processed >= batch_data["total_requests"]:
                batch_data["status"] = "completed"
            else:
                batch_data["status"] = "processing"

            if self.use_redis:
                # Redis backend
                batch_key = f"{self.batch_prefix}{batch_id}"
                await asyncio.to_thread(
                    self.redis_client.setex, batch_key, 3600, json.dumps(batch_data)
                )
            else:
                # In-memory backend (already updated in place)
                pass

            logger.info(
                f"Updated batch {batch_id} progress: {total_processed}/{batch_data['total_requests']}"
            )

        except Exception as e:
            logger.error(f"Error updating batch progress: {str(e)}")

    async def get_task_result(self, task_id: str) -> Optional[AudioResponse]:
        """Get task result by ID."""
        try:
            if self.use_redis:
                # Redis backend
                result_data_str = await asyncio.to_thread(
                    self.redis_client.get, f"{self.result_prefix}{task_id}"
                )
                if not result_data_str:
                    return None
                result_data = json.loads(result_data_str)
            else:
                # In-memory backend
                result_data = self._results.get(task_id)
                if not result_data:
                    return None

            if "result" in result_data:
                return AudioResponse(**result_data["result"])
            else:
                # Task is still pending
                return AudioResponse(
                    success=False,
                    message=f"Task {task_id} is still {result_data.get('status', 'pending')}",
                )

        except Exception as e:
            logger.error(f"Error getting task result: {str(e)}")
            return None

    async def get_batch_status(self, batch_id: str) -> Optional[BatchAudioResponse]:
        """Get batch status and results."""
        try:
            if self.use_redis:
                # Redis backend
                batch_data_str = await asyncio.to_thread(
                    self.redis_client.get, f"{self.batch_prefix}{batch_id}"
                )
                if not batch_data_str:
                    return None
                batch_data = json.loads(batch_data_str)
            else:
                # In-memory backend
                batch_data = self._batches.get(batch_id)
                if not batch_data:
                    return None

            # Get results for all tasks in batch
            results = []
            for task_id in batch_data["task_ids"]:
                task_result = await self.get_task_result(task_id)
                if task_result:
                    results.append(task_result)

            return BatchAudioResponse(
                batch_id=batch_id,
                total_requests=batch_data["total_requests"],
                completed=batch_data["completed"],
                failed=batch_data["failed"],
                results=results,
                status=batch_data["status"],
            )

        except Exception as e:
            logger.error(f"Error getting batch status: {str(e)}")
            return None

    async def cleanup_expired_tasks(self):
        """Clean up expired tasks and batches."""
        try:
            # This would be called periodically to clean up old data
            # Redis TTL handles most cleanup automatically
            logger.info("Cleanup completed")

        except Exception as e:
            logger.error(f"Error during cleanup: {str(e)}")
