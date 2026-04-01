import os
import subprocess
import venv
from pathlib import Path

VENV_DIR = Path(".venv")
REQUIREMENTS = Path("requirements.txt")


def create_venv():
    print("\nCreating virtual environment (.venv)...")
    venv.create(VENV_DIR, with_pip=True)


def get_venv_python():
    if os.name == "nt":
        return VENV_DIR / "Scripts" / "python.exe"
    return VENV_DIR / "bin" / "python"


def install_requirements(python_path):
    print("\nFirst run detected.")
    print("Installing dependencies (this may take several minutes)...\n")

    subprocess.check_call([python_path, "-m", "pip", "install", "--upgrade", "pip"])
    subprocess.check_call([python_path, "-m", "pip", "install", "-r", str(REQUIREMENTS)])


def dependencies_installed(python_path):
    try:
        subprocess.check_call(
            [python_path, "-c", "import uvicorn"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        return True
    except subprocess.CalledProcessError:
        return False


def start_server(python_path):
    print("\nStarting Cognix server...\n")

    subprocess.call([
        python_path,
        "-m",
        "uvicorn",
        "backend.app:app",
        "--host",
        "0.0.0.0",
        "--port",
        "8000"
    ])


def main():
    if not VENV_DIR.exists():
        create_venv()

    python_path = get_venv_python()

    if not dependencies_installed(python_path):
        install_requirements(python_path)

    start_server(python_path)


if __name__ == "__main__":
    main()