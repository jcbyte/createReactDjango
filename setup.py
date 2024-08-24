# TODO This should be upgraded to a toml

from setuptools import find_packages, setup

setup(
    name="start-react-django",
    version="0.1.0",
    description="Automate creation of django projects with react",
    author="Joel Cutler",
    packages=find_packages(),
    entry_points={
        "console_scripts": ["start-react-django=start_react_django.entry:entry"],
    },
    install_requires=["astor"],
)
