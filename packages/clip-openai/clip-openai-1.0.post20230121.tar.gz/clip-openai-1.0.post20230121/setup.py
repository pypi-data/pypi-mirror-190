import os

import pkg_resources
from setuptools import setup, find_packages

setup(
    name="clip-openai",
    py_modules=["clip"],
    version="1.0.post20230121",
    url="https://github.com/openai/CLIP",
    description="CLIP package of OpenAI",
    long_description="## CLIP python package of OpenAI.\n\n"
                     "Note: This is unofficial. I change setup.py a little to publish this package including "
                     "add commit date to version and etc.",
    long_description_content_type="text/markdown",
    author="OpenAI",
    packages=find_packages(exclude=["tests*"]),
    install_requires=[
        str(r)
        for r in pkg_resources.parse_requirements(
            open(os.path.join(os.path.dirname(__file__), "requirements.txt"))
        )
    ],
    include_package_data=True,
    extras_require={'dev': ['pytest']},
)
