import socket
import sys

def is_port_in_use(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind(('localhost', port))
            return False
        except socket.error:
            return True

def find_available_port(start_port: int, max_attempts: int = 10) -> int:
    port = start_port
    for _ in range(max_attempts):
        if not is_port_in_use(port):
            return port
        port += 1
    raise RuntimeError(f"Could not find an available port after {max_attempts} attempts")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python port_check.py <start_port>")
        sys.exit(1)
    
    try:
        start_port = int(sys.argv[1])
        available_port = find_available_port(start_port)
        print(available_port)
    except ValueError:
        print("Error: Port must be a number")
        sys.exit(1)
    except RuntimeError as e:
        print(f"Error: {e}")
        sys.exit(1) 