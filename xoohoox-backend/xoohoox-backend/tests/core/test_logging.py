import os
import logging
import pytest
from unittest.mock import patch, MagicMock
from app.core.logging import setup_logging
from app.core.config import settings

def test_setup_logging_creates_log_directory(tmp_path):
    """Test that setup_logging creates the log directory if it doesn't exist."""
    # Mock the os.path.exists and os.makedirs functions
    with patch('os.path.exists', return_value=False) as mock_exists, \
         patch('os.makedirs') as mock_makedirs, \
         patch('app.core.logging.logging.getLogger') as mock_get_logger, \
         patch('app.core.logging.logging.handlers.RotatingFileHandler') as mock_file_handler, \
         patch('app.core.logging.logging.StreamHandler') as mock_console_handler:
        
        # Call the setup_logging function
        loggers = setup_logging()
        
        # Check that os.path.exists was called with the log directory
        mock_exists.assert_called_once_with("logs")
        
        # Check that os.makedirs was called with the log directory
        mock_makedirs.assert_called_once_with("logs")
        
        # Check that the file handler was created with the correct parameters
        mock_file_handler.assert_called_once()
        args, kwargs = mock_file_handler.call_args
        assert args[0] == "logs/app.log"
        assert kwargs["maxBytes"] == 10485760  # 10MB
        assert kwargs["backupCount"] == 5
        
        # Check that the console handler was created
        mock_console_handler.assert_called_once()
        
        # Check that the root logger was configured
        mock_get_logger.assert_called()
        
        # Check that the component loggers were created
        assert "api" in loggers
        assert "database" in loggers
        assert "security" in loggers
        assert "batch" in loggers
        assert "quality" in loggers
        assert "equipment" in loggers

def test_setup_logging_development_environment():
    """Test that setup_logging sets the correct log level in development environment."""
    # Mock the settings.ENVIRONMENT to be "development"
    with patch('app.core.logging.settings.ENVIRONMENT', "development"), \
         patch('os.path.exists', return_value=True), \
         patch('os.makedirs'), \
         patch('app.core.logging.logging.getLogger') as mock_get_logger, \
         patch('app.core.logging.logging.handlers.RotatingFileHandler'), \
         patch('app.core.logging.logging.StreamHandler'):
        
        # Create a mock logger
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger
        
        # Call the setup_logging function
        setup_logging()
        
        # Check that the root logger was set to DEBUG level
        mock_logger.setLevel.assert_called_with(logging.DEBUG)

def test_setup_logging_production_environment():
    """Test that setup_logging sets the correct log level in production environment."""
    # Mock the settings.ENVIRONMENT to be "production"
    with patch('app.core.logging.settings.ENVIRONMENT', "production"), \
         patch('os.path.exists', return_value=True), \
         patch('os.makedirs'), \
         patch('app.core.logging.logging.getLogger') as mock_get_logger, \
         patch('app.core.logging.logging.handlers.RotatingFileHandler'), \
         patch('app.core.logging.logging.StreamHandler'):
        
        # Create a mock logger
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger
        
        # Call the setup_logging function
        setup_logging()
        
        # Check that the root logger was set to INFO level
        mock_logger.setLevel.assert_called_with(logging.INFO)

def test_setup_logging_formatters():
    """Test that setup_logging creates the correct formatters."""
    with patch('os.path.exists', return_value=True), \
         patch('os.makedirs'), \
         patch('app.core.logging.logging.getLogger') as mock_get_logger, \
         patch('app.core.logging.logging.handlers.RotatingFileHandler') as mock_file_handler, \
         patch('app.core.logging.logging.StreamHandler') as mock_console_handler, \
         patch('app.core.logging.logging.Formatter') as mock_formatter:
        
        # Create mock handlers
        mock_file_handler_instance = MagicMock()
        mock_console_handler_instance = MagicMock()
        mock_file_handler.return_value = mock_file_handler_instance
        mock_console_handler.return_value = mock_console_handler_instance
        
        # Create mock formatters
        mock_file_formatter = MagicMock()
        mock_console_formatter = MagicMock()
        mock_formatter.side_effect = [mock_file_formatter, mock_console_formatter]
        
        # Call the setup_logging function
        setup_logging()
        
        # Check that the formatters were created with the correct format strings
        mock_formatter.assert_any_call('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        mock_formatter.assert_any_call('%(levelname)s: %(message)s')
        
        # Check that the formatters were set on the handlers
        mock_file_handler_instance.setFormatter.assert_called_with(mock_file_formatter)
        mock_console_handler_instance.setFormatter.assert_called_with(mock_console_formatter)

def test_setup_logging_component_loggers():
    """Test that setup_logging creates and configures component loggers."""
    with patch('os.path.exists', return_value=True), \
         patch('os.makedirs'), \
         patch('app.core.logging.logging.getLogger') as mock_get_logger, \
         patch('app.core.logging.logging.handlers.RotatingFileHandler'), \
         patch('app.core.logging.logging.StreamHandler'):
        
        # Create mock loggers
        mock_root_logger = MagicMock()
        mock_api_logger = MagicMock()
        mock_database_logger = MagicMock()
        mock_security_logger = MagicMock()
        mock_batch_logger = MagicMock()
        mock_quality_logger = MagicMock()
        mock_equipment_logger = MagicMock()
        
        # Set up the mock_get_logger to return different loggers based on the name
        def get_logger_side_effect(name=None):
            if name is None:
                return mock_root_logger
            elif name == 'api':
                return mock_api_logger
            elif name == 'database':
                return mock_database_logger
            elif name == 'security':
                return mock_security_logger
            elif name == 'batch':
                return mock_batch_logger
            elif name == 'quality':
                return mock_quality_logger
            elif name == 'equipment':
                return mock_equipment_logger
            else:
                return MagicMock()
        
        mock_get_logger.side_effect = get_logger_side_effect
        
        # Call the setup_logging function
        loggers = setup_logging()
        
        # Check that the component loggers were created and configured
        assert loggers['api'] == mock_api_logger
        assert loggers['database'] == mock_database_logger
        assert loggers['security'] == mock_security_logger
        assert loggers['batch'] == mock_batch_logger
        assert loggers['quality'] == mock_quality_logger
        assert loggers['equipment'] == mock_equipment_logger
        
        # Check that each component logger was configured with the correct level and propagate flag
        for logger in loggers.values():
            logger.setLevel.assert_called()
            assert logger.propagate is True 