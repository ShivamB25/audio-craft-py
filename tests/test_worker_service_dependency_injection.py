"""
Test dependency injection and Redis configuration in WorkerService.
"""

import pytest
from unittest.mock import Mock
from audio_api.services.worker_service import WorkerService, WorkerManager
from audio_api.services.queue_service import QueueService
from audio_api.services.tts_service import TTSService
from audio_api.config import AudioConfig


class TestWorkerServiceDependencyInjection:
    """Test dependency injection in WorkerService."""

    def test_worker_service_uses_config_redis_setting(self):
        """Test that WorkerService uses the Redis setting from config."""
        # Test with Redis enabled
        config_with_redis = AudioConfig(
            gemini_api_key="test_key",
            use_redis=True
        )
        worker = WorkerService(config=config_with_redis)
        assert worker.queue_service.use_redis is True

        # Test with Redis disabled
        config_without_redis = AudioConfig(
            gemini_api_key="test_key",
            use_redis=False
        )
        worker = WorkerService(config=config_without_redis)
        assert worker.queue_service.use_redis is False

    def test_worker_service_accepts_injected_queue_service(self):
        """Test that WorkerService accepts an injected QueueService."""
        config = AudioConfig(
            gemini_api_key="test_key",
            use_redis=False
        )
        
        # Create a mock queue service
        mock_queue_service = Mock(spec=QueueService)
        mock_queue_service.use_redis = False
        
        worker = WorkerService(
            config=config,
            queue_service=mock_queue_service
        )
        
        assert worker.queue_service is mock_queue_service

    def test_worker_service_accepts_injected_tts_service(self):
        """Test that WorkerService accepts an injected TTSService."""
        config = AudioConfig(
            gemini_api_key="test_key",
            use_redis=False
        )
        
        # Create a mock TTS service
        mock_tts_service = Mock(spec=TTSService)
        
        worker = WorkerService(
            config=config,
            tts_service=mock_tts_service
        )
        
        assert worker.tts_service is mock_tts_service

    def test_worker_manager_uses_config_redis_setting(self):
        """Test that WorkerManager uses the Redis setting from config."""
        config = AudioConfig(
            gemini_api_key="test_key",
            use_redis=False
        )
        
        manager = WorkerManager(config=config)
        
        # Test the queue service factory
        queue_service = manager.queue_service_factory()
        assert queue_service.use_redis is False

    def test_worker_manager_accepts_queue_service_factory(self):
        """Test that WorkerManager accepts a custom queue service factory."""
        config = AudioConfig(
            gemini_api_key="test_key",
            use_redis=False
        )
        
        # Create a mock factory
        mock_queue_service = Mock(spec=QueueService)
        mock_factory = Mock(return_value=mock_queue_service)
        
        manager = WorkerManager(
            config=config,
            queue_service_factory=mock_factory
        )
        
        # Test that the factory is used
        result = manager.queue_service_factory()
        assert result is mock_queue_service
        mock_factory.assert_called_once()

    def test_config_validation_with_redis_disabled(self):
        """Test that config validation works when Redis is disabled."""
        config = AudioConfig(
            gemini_api_key="test_key",
            use_redis=False,
            redis_url=""  # Empty Redis URL should be fine when Redis is disabled
        )
        
        # Should not raise an exception
        config.validate_config()

    def test_config_validation_with_redis_enabled_requires_url(self):
        """Test that config validation requires Redis URL when Redis is enabled."""
        config = AudioConfig(
            gemini_api_key="test_key",
            use_redis=True,
            redis_url=""  # Empty Redis URL should cause validation error
        )
        
        with pytest.raises(ValueError, match="REDIS_URL is required when USE_REDIS is true"):
            config.validate_config()


class TestWorkerServiceFlexibility:
    """Test the flexibility improvements for testing and development."""

    def test_in_memory_queue_for_testing(self):
        """Test that in-memory queue can be used for testing."""
        config = AudioConfig(
            gemini_api_key="test_key",
            use_redis=False
        )
        
        # Create worker with in-memory queue
        worker = WorkerService(config=config)
        
        # Verify it uses in-memory queue
        assert worker.queue_service.use_redis is False
        assert hasattr(worker.queue_service, '_task_queue')  # In-memory queue attribute
        assert hasattr(worker.queue_service, '_results')     # In-memory results attribute

    def test_mock_services_for_unit_testing(self):
        """Test that services can be mocked for unit testing."""
        config = AudioConfig(
            gemini_api_key="test_key",
            use_redis=False
        )
        
        # Create mock services
        mock_queue_service = Mock(spec=QueueService)
        mock_tts_service = Mock(spec=TTSService)
        
        # Inject mocks
        worker = WorkerService(
            config=config,
            queue_service=mock_queue_service,
            tts_service=mock_tts_service
        )
        
        # Verify mocks are used
        assert worker.queue_service is mock_queue_service
        assert worker.tts_service is mock_tts_service