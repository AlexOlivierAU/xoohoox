import subprocess
import sys
import os
from port_check import find_available_port

def start_server(port: int = 8000):
    try:
        available_port = find_available_port(port)
        if available_port != port:
            print(f"Port {port} is in use. Using port {available_port} instead.")
        
        # Get the absolute path to the xoohoox-backend directory
        backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        
        # Add the backend directory to the Python path
        python_path = f"PYTHONPATH={backend_dir}"
        
        # Use the PYTHONPATH environment variable to ensure Python can find the app module
        cmd = f"{python_path} python -m uvicorn app.main:app --reload --port {available_port}"
        subprocess.run(cmd, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error starting server: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    start_server() 