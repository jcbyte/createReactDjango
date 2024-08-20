import json
import shutil
import subprocess
from pathlib import Path


def create_project(args):

    this_path = Path(__file__).resolve().parent
    cmd_path = Path.cwd()

    # If a folder already exists where we want to place our project then throw an error
    project_path = cmd_path / args.name
    shutil.rmtree(project_path)  # ! THIS IS FOR TESTING AND SHOULD BE REMOVED
    if project_path.exists():
        raise FileExistsError(f'A folder with name "{args.name}" already exists, at "{project_path}".')

    # Create folder for our project
    project_path.mkdir()

    # Create python environment
    subprocess.run(["python", "-m", "venv", project_path / args.env])
    project_venv = project_path / args.env / "Scripts"

    # Generate the requirements file
    with open(this_path / "python_requirements.json", "r") as f:
        requirements_data = json.load(f)

    requirements_list = requirements_data["always"]

    if args.cors:
        requirements_list.extend(requirements_data["cors"])
    if args.jwt:
        requirements_list.extend(requirements_data["jwt"])

    # Write to the requirements file in the new project
    with open(project_path / "requirements.txt", "w") as f:
        f.write("\n".join(requirements_list))

    # Install the requirements
    subprocess.run([project_venv / "pip", "install", "-r", project_path / "requirements.txt"])
