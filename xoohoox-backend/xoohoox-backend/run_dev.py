#!/usr/bin/env python3
import os
import sys
import subprocess
import time
import signal
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('xoohoox-dev')

def check_venv():
    """Check if virtual environment exists and is activated."""
    if not os.path.exists('venv'):
        logger.info("Creating virtual environment...")
        subprocess.run([sys.executable, '-m', 'venv', 'venv'], check=True)
    
    # Check if we're in a virtual environment
    if not hasattr(sys, 'real_prefix') and not sys.base_prefix != sys.prefix:
        logger.info("Activating virtual environment...")
        if os.name == 'nt':  # Windows
            activate_script = os.path.join('venv', 'Scripts', 'activate.bat')
        else:  # Unix/Linux/MacOS
            activate_script = os.path.join('venv', 'bin', 'activate')
        
        if os.name == 'nt':
            subprocess.run([activate_script], shell=True, check=True)
        else:
            subprocess.run(['source', activate_script], shell=True, check=True)

def install_dependencies():
    """Install required Python packages."""
    logger.info("Installing dependencies...")
    # First try to install from the fixed requirements file
    if os.path.exists('requirements_fixed.txt'):
        logger.info("Using fixed requirements file...")
        subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements_fixed.txt'], check=True)
    else:
        # Fall back to the regular requirements file
        subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'], check=True)

def setup_environment():
    """Set up the development environment."""
    # Create necessary directories
    directories = ['logs', 'app/tests', 'app/api/v1/endpoints']
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        logger.info(f"Created directory: {directory}")
    
    # Copy .env file if it doesn't exist
    if not os.path.exists('.env') and os.path.exists('.env.development'):
        logger.info("Creating .env file from template...")
        with open('.env.development', 'r') as src, open('.env', 'w') as dst:
            dst.write(src.read())

def run_migrations():
    """Run database migrations."""
    logger.info("Running database migrations...")
    try:
        subprocess.run([sys.executable, '-m', 'alembic', 'upgrade', 'head'], check=True)
    except subprocess.CalledProcessError as e:
        logger.error(f"Error running migrations: {e}")
        logger.info("Skipping migrations for now. You may need to run them manually later.")
        return False
    return True

def create_test_user():
    """Create a test user if the script exists."""
    if os.path.exists('create_test_user.py'):
        logger.info("Creating test user...")
        try:
            subprocess.run([sys.executable, 'create_test_user.py'], check=True)
        except subprocess.CalledProcessError as e:
            logger.error(f"Error creating test user: {e}")
            logger.info("Skipping test user creation for now.")
            return False
    return True

def run_tests():
    """Run the test suite."""
    logger.info("Running tests...")
    try:
        subprocess.run([sys.executable, '-m', 'pytest'], check=True)
    except subprocess.CalledProcessError as e:
        logger.error(f"Error running tests: {e}")
        logger.info("Skipping tests for now. You may need to run them manually later.")
        return False
    return True

def start_server():
    """Start the development server."""
    logger.info("Starting development server...")
    try:
        # Start the uvicorn server
        process = subprocess.Popen(
            [sys.executable, '-m', 'uvicorn', 'app.main:app', '--reload', '--host', '0.0.0.0', '--port', '8000'],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True
        )
        
        # Handle graceful shutdown
        def signal_handler(sig, frame):
            logger.info("Shutting down server...")
            process.terminate()
            sys.exit(0)
        
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
        
        # Stream the output
        for line in process.stdout:
            print(line, end='')
        
        process.wait()
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception as e:
        logger.error(f"Error starting server: {e}")
        sys.exit(1)

def main():
    """Main function to set up and run the development environment."""
    try:
        logger.info("Setting up Xoohoox Backend Development Environment...")
        
        # Run setup steps
        check_venv()
        install_dependencies()
        setup_environment()
        
        # Try to run migrations, but continue even if they fail
        migrations_success = run_migrations()
        
        # Try to create test user, but continue even if it fails
        user_creation_success = create_test_user()
        
        # Try to run tests, but continue even if they fail
        tests_success = run_tests()
        
        # If any of the setup steps failed, show a warning
        if not all([migrations_success, user_creation_success, tests_success]):
            logger.warning("Some setup steps failed. The server may not work correctly.")
            logger.warning("Please check the logs for more information.")
        
        # Start the server
        start_server()
    except Exception as e:
        logger.error(f"Error during setup: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 