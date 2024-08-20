import subprocess
from pathlib import Path


def create_project(args):
    cmd_path = Path.cwd()

    # If a folder already exists where we want to place our project then throw an error
    project_path = cmd_path / args.name
    if project_path.exists():
        raise FileExistsError(f'A folder with name "{args.name}" already exists, at "{project_path}".')

    # Create folder for our project
    project_path.mkdir()

    # Create python environment
    # TODO the virtual environment name could be an argument
    subprocess.run(["python", "-m", "venv", project_path / ".venv"])
