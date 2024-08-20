import argparse


def entry():
    parser = argparse.ArgumentParser(description="Automate creation of django projects with react")

    parser.add_argument("name", type=str, help="Name of the project")
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
    parser.add_argument(
        "-jwt",
        action="store_true",
        help="Includes JWT token setup",
    )

    args = parser.parse_args()

    print(args.name, args.typescript, args.cors, args.jwt)
