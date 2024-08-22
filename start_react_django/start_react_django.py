import json
import os
import shutil
import subprocess
from pathlib import Path

from start_react_django.file_editors.json_editor import JSONEditor
from start_react_django.file_editors.python_editor import PythonEditor


# Copy files from a folder into a new folder replacing any existing at the same path
def copy_files(src: Path, dst: Path):
    # Ensure the destination directory exists
    if not dst.is_dir():
        dst.mkdir()

    # Iterate over all files and subdirectories in the source directory
    for item in os.listdir(src):
        src_path = src / item
        dst_path = dst / item

        # If it is a directory then copy this directory
        if src_path.is_dir():
            copy_files(src_path, dst_path)

        # If it is a file then copy the file replacing the file if it already existed
        else:
            shutil.copy2(src_path, dst_path)


def create_project(args):

    this_path = Path(__file__).resolve().parent
    cmd_path = Path.cwd()

    templates_path = this_path / "templates"

    # Get config file for future processes
    with open(this_path / "config.json", "r") as f:
        config_data = json.load(f)

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
    requirements_data = config_data["python_requirements"]
    scripts_list = requirements_data["always"]
    if args.cors:
        scripts_list.extend(requirements_data["cors"])

    # Write to the requirements file in the new project
    with open(project_path / "requirements.txt", "w") as f:
        f.write("\n".join(scripts_list))

    # Install the requirements
    subprocess.run([project_py, "-m", "pip", "install", "-r", project_path / "requirements.txt"], check=True)

    # Create Django project
    subprocess.run([project_py, "-m", "django", "startproject", args.name], cwd=project_path, check=True)
    django_project_path = project_path / args.name
    django_project_main_path = django_project_path / args.name
    django_project_manage_script = django_project_path / "manage.py"

    # Create the api django app
    subprocess.run([project_py, django_project_manage_script, "startapp", "api"], cwd=django_project_path, check=True)
    django_api_app_path = django_project_path / "api"

    # Copy the template files into the API app
    api_files_data = config_data["api_files"]
    api_files_list = api_files_data["always"]

    for api_files in api_files_list:
        copy_files(templates_path / api_files, django_api_app_path)

    # Create the frontend django app
    subprocess.run([project_py, django_project_manage_script, "startapp", "frontend"], cwd=django_project_path, check=True)
    django_frontend_app_path = django_project_path / "frontend"

    # Initialise node in frontend
    subprocess.run(["npm", "init", "-y"], cwd=django_frontend_app_path, shell=True, check=True)

    # Get the node dependencies
    dependencies_data = config_data["node_dependencies"]
    dependencies_list = dependencies_data["always"]
    if args.typescript:
        dependencies_list.extend(dependencies_data["typescript"])

    # Install these dependencies
    subprocess.run(["npm", "install", *dependencies_list], cwd=django_frontend_app_path, shell=True, check=True)

    # Copy the template files into the frontend app
    frontend_files_data = config_data["frontend_files"]
    frontend_files_list = frontend_files_data["always"]
    if args.typescript:
        frontend_files_list.extend(frontend_files_data["typescript"])
    else:
        frontend_files_list.extend(frontend_files_data["no-typescript"])

    for frontend_files in frontend_files_list:
        copy_files(templates_path / frontend_files, django_frontend_app_path)

    # Add the node CLI scripts
    scripts_data = config_data["node_scripts"]
    scripts_list = scripts_data["always"]

    with JSONEditor(django_frontend_app_path / "package.json") as package_data:
        package_data["scripts"] = scripts_list

    # Configure the django project urls
    urls_data = config_data["django_urls"]
    urls_list = urls_data["always"]

    with PythonEditor(django_project_main_path / "urls.py") as pcm:
        pcm.add_code(["from django.urls import include"], end=False)
        pcm.modify_array("urlpatterns", urls_list, extend=True)

    # Configure the django project settings
    settings_data = config_data["django_settings"]
    settings_list = settings_data["always"]
    if args.cors:
        settings_list.extend(settings_data["cors"])

    middleware_data = config_data["django_middleware"]
    middleware_list = middleware_data["always"]
    if args.cors:
        middleware_list.extend(middleware_data["cors"])

    with PythonEditor(django_project_main_path / "settings.py") as pcm:
        pcm.modify_array("INSTALLED_APPS", settings_list, extend=True)
        pcm.modify_array("MIDDLEWARE", middleware_list, extend=True)

    # Initialise database
    subprocess.run([project_py, django_project_manage_script, "makemigrations"], cwd=django_project_path, check=True)
    subprocess.run([project_py, django_project_manage_script, "migrate"], cwd=django_project_path, check=True)
