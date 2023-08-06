from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="mohcli",
    version="0.0.0",
    author="Ken Aremoh",
    author_email="Kenneth.aremoh@gmail.com",
    description="A CLI tool for generating a bare-bone FastAPI project",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kenmoh/moh_cli",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=["typer", "rich"],
    entry_points={
        "console_scripts": [
            "mohcli = mohcli.main",
        ],
    },
)
