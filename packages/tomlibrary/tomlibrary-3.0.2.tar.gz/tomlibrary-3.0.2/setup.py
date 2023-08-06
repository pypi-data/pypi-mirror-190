from setuptools import setup, find_packages

import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tomlibrary",
    version="3.0.2",
    author="Schooldevops",
    author_email="schooldevops@gmail.com",
    description="schooldevops sample lib",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/schooldevops/python-tutorials",
    project_urls={
        "Bug Tracker": "https://github.com/schooldevops/python-tutorials/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    entry_points={
        'console_scripts': [
            'func = func:add',
        ],
    },

)
