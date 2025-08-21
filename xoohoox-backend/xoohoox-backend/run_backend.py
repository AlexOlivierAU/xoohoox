#!/usr/bin/env python3
import os
import subprocess
import sys

def run_backend():
    try:
        # Get the absolute path to the xoohoox-backend directory
        backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'xoohoox-backend'))
        
        # Change to the backend directory
        os.chdir(backend_dir)
        
        # Add the backend directory to the Python path
        python_path = f"PYTHONPATH={backend_dir}"
        
        # Run the start_server.py script
        cmd = f"{python_path} python scripts/start_server.py"
        subprocess.run(cmd, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error starting server: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run_backend() 