import sys
import os
import time
import subprocess

def start_django_server():
    """Start the Django server using the correct Python interpreter and show logs in real-time."""
    python_exec = sys.executable
    manage_py_path = os.path.abspath("manage.py")

    try:
        return subprocess.Popen(
            [python_exec, manage_py_path, "runserver"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )
    except Exception as e:
        print(f"Error starting Django server: {e}")
        return None

def open_browser():
    """Open the browser in a new window and return the process."""
    url = "http://localhost:8000/api/v1"
    browser_process = None
    
    try:
        if sys.platform.startswith("win"):
            browser_process = subprocess.Popen(["cmd", "/c", "start", "chrome", "--new-window", url])  # Windows (Chrome)
        elif sys.platform.startswith("darwin"):
            browser_process = subprocess.Popen(["open", "-na", "Google Chrome", "--args", "--new-window", url])  # macOS
        else:
            browser_process = subprocess.Popen(["xdg-open", url])  # Linux

        return browser_process
    except Exception as e:
        print(f"Error opening browser: {e}")
        return None

def main():
    server_process = start_django_server()
    if server_process is None:
        print("Django server failed to start. Exiting...")
        return

    try:
        # Esperar a que el servidor se inicie completamente
        time.sleep(3)  

        # Abrir navegador en una ventana independiente
        browser_process = open_browser()
        print("Browser opened, waiting for it to close...")

        # Leer y mostrar logs del servidor en tiempo real
        while True:
            server_status = server_process.poll()
            browser_status = browser_process.poll() if browser_process else None

            if server_status is not None:
                print("\nServer stopped, closing browser...")
                if browser_process:
                    browser_process.terminate()  # Cierra la ventana del navegador
                break

            if browser_status is not None:
                print("\nBrowser closed, stopping server...")
                server_process.terminate()
                break
            
            # Leer salida del servidor en tiempo real
            output = server_process.stdout.readline()
            if output:
                print(output.strip())

    except KeyboardInterrupt:
        print("\nStopping the server and closing browser...")
        if browser_process:
            browser_process.terminate()
        server_process.terminate()

    finally:
        server_process.wait()
        if browser_process:
            browser_process.wait()
        print("Cleanup complete. Exiting.")

if __name__ == "__main__":
    main()
