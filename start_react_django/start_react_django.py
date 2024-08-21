import json
import shutil
import subprocess
from pathlib import Path


def create_project(args):

    this_path = Path(__file__).resolve().parent
    cmd_path = Path.cwd()

    # If a folder already exists where we want to place our project then throw an error
    project_path = cmd_path / args.name
    if project_path.exists():
        shutil.rmtree(project_path)  # ! THIS IS FOR TESTING AND SHOULD BE REMOVED
        # raise FileExistsError(f'A folder with name "{args.name}" already exists, at "{project_path}".')

    # Create folder for our project
    project_path.mkdir()

    # Create python environment
    subprocess.run(["python", "-m", "venv", project_path / args.env], check=True)
    project_py = project_path / args.env / "Scripts" / "python"

    # Get the python requirements
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
    subprocess.run([project_py, "-m", "pip", "install", "-r", project_path / "requirements.txt"], check=True)

    # Create Django project
    subprocess.run([project_py, "-m", "django", "startproject", args.name], cwd=project_path, check=True)
    django_project_path = project_path / args.name

    # Create the api django app
    subprocess.run([project_py, "-m", "django", "startapp", "api"], cwd=django_project_path, check=True)

    # TODO copy api template files

    # Create the frontend django app
    subprocess.run([project_py, "-m", "django", "startapp", "frontend"], cwd=django_project_path, check=True)
    frontend_app_path = django_project_path / "frontend"

    # Initialise node in frontend
    subprocess.run(["npm", "init", "-y"], cwd=frontend_app_path, shell=True, check=True)

    # Get the node dependencies
    with open(this_path / "node_dependencies.json", "r") as f:
        dependencies_data = json.load(f)

    dependencies_list = dependencies_data["always"]

    if args.typescript:
        dependencies_list.extend(dependencies_data["typescript"])

    # Install these dependencies
    subprocess.run(["npm", "install", *dependencies_list], cwd=frontend_app_path, shell=True, check=True)

    # TODO copy frontend template files

    # TODO configure django project

    # TODO configure cors (should this be done in api)

    # TODO configure jwt (should this be done in api)

    # TODO initialise database


if __name__ == "__main__":
    import argparse

    # When debugging, then emulate running the script with these args
    create_project(
        argparse.Namespace(
            **{
                "name": "testproj",
                "cors": False,
                "jwt": False,
                "typescript": False,
                "env": ".venv",
            }
        )
    )
