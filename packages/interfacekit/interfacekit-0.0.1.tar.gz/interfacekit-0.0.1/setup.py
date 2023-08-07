# 
#   InterfaceKit
#   Copyright © 2023 NatML Inc. All Rights Reserved.
#

from setuptools import find_packages, setup

# Get readme
with open("README.md", "r") as readme:
    long_description = readme.read()

# Get version
with open("interfacekit/version.py") as version_source:
    gvars = {}
    exec(version_source.read(), gvars)
    version = gvars["__version__"]

# Setup
setup(
    name="interfacekit",
    version=version,
    author="NatML Inc",
    author_email="hi@interfacekit.ai",
    description="🤫",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="Apache License 2.0",
	python_requires=">=3.6",
    install_requires=[
        "numpy",
        "Pillow",
    ],
    url="https://interfacekit.ai",
    packages=find_packages(
        include=["interfacekit", "interfacekit.*"],
        exclude=["test", "examples"]
    ),
    entry_points={
        "console_scripts": [
            "interfacekit=interfacekit.cli:main"
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Image Recognition",
        "Topic :: Software Development :: Libraries",
    ],
    project_urls={
        "Documentation": "https://docs.interfacekit.ai/python",
        "Source": "https://github.com/interface-kit/InterfaceKit-Py"
    },
)