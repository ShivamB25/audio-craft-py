import asyncio
import logging
from audio_api.services.tts_service import TTSService
from audio_api.services.queue_service import QueueService
from audio_api.models import AudioRequest, AudioResponse

logger = logging.getLogger(__name__)


class WorkerService:
    def __init__(self, redis_url: str = "redis://localhost:6379/0"):
        self.tts_service = TTSService()
        self.queue_service = QueueService(redis_url)
        self.running = False

    async def start_worker(self, worker_id: str = "worker-1"):
        """Start the worker to process tasks from the queue."""
        self.running = True
        logger.info(f"Starting worker {worker_id}")

        while self.running:
            try:
                # Dequeue a task
                task_data = await self.queue_service.dequeue_task()

                if task_data:
                    await self._process_task(task_data)
                else:
                    # No tasks available, wait a bit
                    await asyncio.sleep(1)

            except Exception as e:
                logger.error(f"Worker error: {str(e)}")
                await asyncio.sleep(5)  # Wait before retrying

        logger.info(f"Worker {worker_id} stopped")

    async def stop_worker(self):
        """Stop the worker."""
        self.running = False
        logger.info("Stopping worker")

    async def _process_task(self, task_data: dict):
        """Process a single task."""
        task_id = task_data.get("task_id")
        batch_id = task_data.get("batch_id")

        try:
            logger.info(f"Processing task {task_id}")

            # Parse the audio request
            request_data = task_data.get("request", {})
            audio_request = AudioRequest(**request_data)

            # Generate audio
            result = await self.tts_service.generate_audio(audio_request)

            # Update task result
            await self.queue_service.update_task_result(task_id, result)

            # Update batch progress if this is part of a batch
            if batch_id:
                await self.queue_service.update_batch_progress(
                    batch_id, task_id, result.success
                )

            if result.success:
                logger.info(f"Task {task_id} completed successfully")
            else:
                logger.error(f"Task {task_id} failed: {result.error}")

        except Exception as e:
            logger.error(f"Error processing task {task_id}: {str(e)}")

            # Create error response
            error_result = AudioResponse(
                success=False, message="Task processing failed", error=str(e)
            )

            # Update task result with error
            await self.queue_service.update_task_result(task_id, error_result)

            # Update batch progress if this is part of a batch
            if batch_id:
                await self.queue_service.update_batch_progress(batch_id, task_id, False)


class WorkerManager:
    def __init__(
        self, redis_url: str = "redis://localhost:6379/0", num_workers: int = 3
    ):
        self.redis_url = redis_url
        self.num_workers = num_workers
        self.workers = []
        self.worker_tasks = []

    async def start_workers(self):
        """Start multiple worker instances."""
        logger.info(f"Starting {self.num_workers} workers")

        for i in range(self.num_workers):
            worker = WorkerService(self.redis_url)
            worker_id = f"worker-{i+1}"

            # Start worker in background task
            task = asyncio.create_task(worker.start_worker(worker_id))

            self.workers.append(worker)
            self.worker_tasks.append(task)

        logger.info(f"All {self.num_workers} workers started")

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
