import os
import subprocess
import sys
import time
import webbrowser


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
    """Open the browser and return the process (if available on the platform)."""
    url = "http://localhost:8000/api/docs/"
    try:
        webbrowser.open(url, new=1)  # new=1 abre una nueva ventana/pestaña
        return True  # Indica que se intentó abrir
    except Exception as e:
        print(f"Error opening browser: {e}")
        return False


def main():
    server_process = start_django_server()
    if server_process is None:
        print("Django server failed to start. Exiting...")
        return

    try:
        # Esperar a que el servidor se inicie completamente
        time.sleep(3)

        # Abrir navegador en una ventana independiente
        open_browser()
        print("Browser opened. Press Ctrl+C to stop the server...")

        # Leer y mostrar logs del servidor en tiempo real
        while True:
            server_status = server_process.poll()

            if server_status is not None:
                print("\nServer stopped.")
                break

            # Leer salida del servidor en tiempo real
            output = server_process.stdout.readline()
            if output:
                print(output.strip())

    except KeyboardInterrupt:
        print("\nStopping the server...")
        server_process.terminate()

    finally:
        server_process.wait()
        print("Cleanup complete. Exiting.")


if __name__ == "__main__":
    main()
