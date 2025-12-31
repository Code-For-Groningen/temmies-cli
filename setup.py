from setuptools import find_packages, setup

with open("README.md", "r") as f:
    l_description = f.read()

setup(
    name="temmies-cli",
    version="1.0.12",
    packages=find_packages(),
    description="A command-line tool for managing assignments using the Temmies library",
    long_description=l_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Code-For-Groningen/temmies-cli",
    author="Boyan K.",
    author_email="boyan@confest.im",
    license="GPLv3",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    install_requires=[
        "click>=7.0",
        "requests",
        "lxml",
        "beautifulsoup4",
        "keyring",
        "temmies",
        "tqdm"
    ],
    python_requires=">=3.9",
    entry_points={
        "console_scripts": [
            "temmies=temmies_cli.cli:cli",
        ],
    },
)
