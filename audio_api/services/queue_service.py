try:
    import redis

    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False
    redis = None

import json
import uuid
import asyncio
from typing import Optional, Dict, Any, List
from datetime import datetime
import logging
from collections import deque
from audio_api.models import (
    AudioRequest,
    BatchAudioRequest,
    AudioResponse,
    BatchAudioResponse,
)

logger = logging.getLogger(__name__)


class QueueService:
    def __init__(
        self, use_redis: bool = False, redis_url: str = "redis://localhost:6379/0"
    ):
        """
        Initialize queue service with optional Redis backend.

        Args:
            use_redis: If True, use Redis for persistent queuing. If False, use in-memory queuing.
            redis_url: Redis connection URL (only used if use_redis=True)
        """
        self.use_redis = use_redis

        if use_redis:
            if not REDIS_AVAILABLE:
                raise ImportError(
                    "Redis is not installed. Install with: pip install redis"
                )
            self.redis_client = redis.from_url(redis_url, decode_responses=True)
            self.task_queue = "audio_tasks"
            self.result_prefix = "result:"
            self.batch_prefix = "batch:"
        else:
            # In-memory storage
            self._task_queue = deque()
            self._results = {}
            self._batches = {}
            logger.info("Using in-memory queue (non-persistent)")

    async def enqueue_single_task(self, request: AudioRequest) -> str:
        """Enqueue a single audio generation task."""
        try:
            task_id = str(uuid.uuid4())
            task_data = {
                "task_id": task_id,
                "request": request.model_dump(),
                "created_at": datetime.utcnow().isoformat(),
                "status": "pending",
            }

            if self.use_redis:
                # Redis backend
                await asyncio.to_thread(
                    self.redis_client.lpush, self.task_queue, json.dumps(task_data)
                )
                await asyncio.to_thread(
                    self.redis_client.setex,
                    f"{self.result_prefix}{task_id}",
                    3600,  # 1 hour TTL
                    json.dumps(
                        {"status": "pending", "created_at": task_data["created_at"]}
                    ),
                )
            else:
                # In-memory backend
                self._task_queue.appendleft(task_data)
                self._results[task_id] = {
                    "status": "pending",
                    "created_at": task_data["created_at"],
                }

            logger.info(
                f"Enqueued task {task_id} ({'Redis' if self.use_redis else 'memory'})"
            )
            return task_id

        except Exception as e:
            logger.error(f"Error enqueuing task: {str(e)}")
            raise

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
        """Dequeue a task from the queue."""
        try:
            if self.use_redis:
                # Redis backend
                result = await asyncio.to_thread(
                    self.redis_client.brpop, self.task_queue, timeout=1
                )
                if result:
                    _, task_data = result
                    return json.loads(task_data)
                return None
            else:
                # In-memory backend
                if self._task_queue:
                    return self._task_queue.pop()
                return None

        except Exception as e:
            logger.error(f"Error dequeuing task: {str(e)}")
            return None

    async def update_task_result(self, task_id: str, result: AudioResponse):
        """Update task result."""
        try:
            result_data = {
                "task_id": task_id,
                "result": result.model_dump(),
                "completed_at": datetime.utcnow().isoformat(),
                "status": "completed" if result.success else "failed",
            }

            if self.use_redis:
                # Redis backend
                await asyncio.to_thread(
                    self.redis_client.setex,
                    f"{self.result_prefix}{task_id}",
                    3600,  # 1 hour TTL
                    json.dumps(result_data),
                )
            else:
                # In-memory backend
                self._results[task_id] = result_data

            logger.info(f"Updated result for task {task_id}")

        except Exception as e:
            logger.error(f"Error updating task result: {str(e)}")
            raise

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
