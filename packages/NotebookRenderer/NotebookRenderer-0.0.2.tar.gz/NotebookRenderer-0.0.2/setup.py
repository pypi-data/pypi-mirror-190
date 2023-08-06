from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    LONG_DESCRIPTION = f.read()

REPO_NAME = "NotebookRenderer"
AUTHOR_NAME = "Subhasish-Saha" 
AUTHOR_EMAIL = "subhasishsaha007@gmail.com"

setup(
    name = REPO_NAME,
    version = "0.0.2",
    author = AUTHOR_NAME,
    author_email = AUTHOR_EMAIL,
    description = "A small python package",
    long_description = LONG_DESCRIPTION,
    url = f"https://github.com/{AUTHOR_NAME}/{REPO_NAME}",
    project_urls = {
        "Bug Tracker": f"https://github.com/{AUTHOR_NAME}/{REPO_NAME}/issues"
    },
    package_dir = {"": "src"},
    packages = find_packages(where="src")
)
