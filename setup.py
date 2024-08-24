# TODO This should be upgraded to a toml

from distutils.core import setup

import setuptools

setup(
    name="start-react-django",
    version="0.1.0",
    description="Automate creation of django projects with react",
    author="Joel Cutler",
    packages=["start_react_django"],
    entry_points={
        "console_scripts": ["start-react-django=start_react_django.entry:entry"],
    },
    install_requires=["astor"],
)
