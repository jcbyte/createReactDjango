import argparse
import sys

from start_react_django.start_react_django import create_project


def abort(message, exit_code=1):
    print(f"Error: {message}")
    sys.exit(exit_code)


def entry():
    parser = argparse.ArgumentParser(description="Automate creation of django projects with react")

    # Define arguments for CLI
    parser.add_argument(
        "name",
        type=str,
        help="Name of the project",
    )
    parser.add_argument(
        "-env",
        type=str,
        metavar="NAME",
        default=".venv",
        help="Specify the environment name",
    )
    parser.add_argument(
        "-ts",
        "--typescript",
        action="store_true",
        help="Initialises the frontend with Typescript instead of Javascript",
    )
    parser.add_argument(
        "-cors",
        action="store_true",
        help="Enable CORS on the server",
    )

    args = parser.parse_args()

    # Create the project with arguments given
    try:
        create_project(args)
    except Exception as e:
        abort(str(e))
