import asyncio
import logging
import time
from typing import Optional
from audio_api.services.tts_service import TTSService
from audio_api.services.queue_service import QueueService
from audio_api.models import AudioRequest, AudioResponse
from audio_api.config import get_config, AudioConfig

logger = logging.getLogger(__name__)


class WorkerServiceError(Exception):
    """Base exception for worker service operations."""

    pass


class WorkerService:
    def __init__(self, config: Optional[AudioConfig] = None):
        """
        Initialize worker service with dependency injection.

        Args:
            config: Configuration instance (uses global config if None)
        """
        self.config = config or get_config()
        self.tts_service = TTSService(config=self.config)
        self.queue_service = QueueService(use_redis=True, config=self.config)
        self.running = False
        self.worker_id = None
        self.tasks_processed = 0
        self.start_time = None

    async def start_worker(self, worker_id: str = "worker-1"):
        """Start the worker to process tasks from the queue with improved monitoring."""
        self.worker_id = worker_id
        self.running = True
        self.start_time = time.time()
        self.tasks_processed = 0

        logger.info(
            f"Starting worker {worker_id} with config: "
            f"task_timeout={self.config.task_timeout}s"
        )

        # Use context manager for proper cleanup
        async with self.queue_service:
            while self.running:
                try:
                    # Check queue service health
                    if not await self.queue_service.health_check():
                        logger.warning(
                            f"Worker {worker_id}: Queue service unhealthy, waiting..."
                        )
                        await asyncio.sleep(5)
                        continue

                    # Dequeue a task with timeout
                    task_data = await asyncio.wait_for(
                        self.queue_service.dequeue_task(),
                        timeout=self.config.task_timeout,
                    )

                    if task_data:
                        await self._process_task(task_data)
                        self.tasks_processed += 1

                        # Log progress periodically
                        if self.tasks_processed % 10 == 0:
                            uptime = time.time() - self.start_time
                            rate = self.tasks_processed / uptime if uptime > 0 else 0
                            logger.info(
                                f"Worker {worker_id}: Processed {self.tasks_processed} tasks "
                                f"(rate: {rate:.2f} tasks/sec)"
                            )
                    else:
                        # No tasks available, wait a bit
                        await asyncio.sleep(1)

                except asyncio.TimeoutError:
                    logger.warning(f"Worker {worker_id}: Task dequeue timeout")
                    await asyncio.sleep(2)
                except Exception as e:
                    logger.error(f"Worker {worker_id} error: {str(e)}")
                    await asyncio.sleep(5)  # Wait before retrying

        total_uptime = time.time() - self.start_time if self.start_time else 0
        logger.info(
            f"Worker {worker_id} stopped after processing {self.tasks_processed} tasks "
            f"in {total_uptime:.1f}s"
        )

    async def stop_worker(self):
        """Stop the worker."""
        self.running = False
        logger.info("Stopping worker")

    async def _process_task(self, task_data: dict):
        """Process a single task with performance tracking and better error handling."""
        task_id = task_data.get("task_id")
        batch_id = task_data.get("batch_id")
        start_time = time.time()

        try:
            logger.info(f"Worker {self.worker_id}: Processing task {task_id}")

            # Parse the audio request
            request_data = task_data.get("request", {})
            audio_request = AudioRequest(**request_data)

            # Add timeout for audio generation
            result = await asyncio.wait_for(
                self.tts_service.generate_audio(audio_request),
                timeout=self.config.task_timeout,
            )

            # Add processing time to result
            processing_time = time.time() - start_time
            result.processing_time = processing_time

            # Update task result
            await self.queue_service.update_task_result(task_id, result)

            # Update batch progress if this is part of a batch
            if batch_id:
                await self.queue_service.update_batch_progress(
                    batch_id, task_id, result.success
                )

            if result.success:
                logger.info(
                    f"Worker {self.worker_id}: Task {task_id} completed successfully "
                    f"in {processing_time:.2f}s"
                )
            else:
                logger.error(
                    f"Worker {self.worker_id}: Task {task_id} failed: {result.error}"
                )

        except asyncio.TimeoutError:
            processing_time = time.time() - start_time
            error_msg = f"Task processing timeout after {processing_time:.1f}s"
            logger.error(f"Worker {self.worker_id}: {error_msg} for task {task_id}")

            # Create timeout error response
            error_result = AudioResponse(
                success=False, message="Task processing timeout", error=error_msg
            )
            error_result.processing_time = processing_time

            # Update task result with timeout error
            try:
                await self.queue_service.update_task_result(task_id, error_result)
                if batch_id:
                    await self.queue_service.update_batch_progress(
                        batch_id, task_id, False
                    )
            except Exception as update_error:
                logger.error(f"Failed to update timeout result: {update_error}")

        except Exception as e:
            processing_time = time.time() - start_time
            logger.error(
                f"Worker {self.worker_id}: Error processing task {task_id}: {str(e)}"
            )

            # Create error response
            error_result = AudioResponse(
                success=False, message="Task processing failed", error=str(e)
            )
            error_result.processing_time = processing_time

            # Update task result with error
            try:
                await self.queue_service.update_task_result(task_id, error_result)
                if batch_id:
                    await self.queue_service.update_batch_progress(
                        batch_id, task_id, False
                    )
            except Exception as update_error:
                logger.error(f"Failed to update error result: {update_error}")


class WorkerManager:
    def __init__(self, config: Optional[AudioConfig] = None):
        """
        Initialize worker manager with configuration.

        Args:
            config: Configuration instance (uses global config if None)
        """
        self.config = config or get_config()
        self.num_workers = self.config.num_workers
        self.workers = []
        self.worker_tasks = []
        self.start_time = None

    async def start_workers(self):
        """Start multiple worker instances with improved monitoring."""
        self.start_time = time.time()
        logger.info(
            f"Starting {self.num_workers} workers with config: "
            f"redis_url={self.config.redis_url}, "
            f"task_timeout={self.config.task_timeout}s"
        )

        for i in range(self.num_workers):
            try:
                worker = WorkerService(config=self.config)
                worker_id = f"worker-{i+1}"

                # Start worker in background task
                task = asyncio.create_task(worker.start_worker(worker_id))

                self.workers.append(worker)
                self.worker_tasks.append(task)

                logger.info(f"Started worker {worker_id}")

            except Exception as e:
                logger.error(f"Failed to start worker {i+1}: {str(e)}")
                raise WorkerServiceError(f"Failed to start worker {i+1}: {str(e)}") from e

        logger.info(f"All {self.num_workers} workers started successfully")

    async def stop_workers(self):
        """Stop all workers."""
        logger.info("Stopping all workers")

        # Signal all workers to stop
        for worker in self.workers:
            await worker.stop_worker()

        # Wait for all worker tasks to complete
        if self.worker_tasks:
            await asyncio.gather(*self.worker_tasks, return_exceptions=True)

        self.workers.clear()
        self.worker_tasks.clear()

        logger.info("All workers stopped")

    async def get_worker_status(self):
        """Get status of all workers."""
        return {
            "total_workers": len(self.workers),
            "running_workers": sum(1 for worker in self.workers if worker.running),
            "worker_details": [
                {"worker_id": f"worker-{i+1}", "running": worker.running}
                for i, worker in enumerate(self.workers)
            ],
        }
