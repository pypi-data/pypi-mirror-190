from setuptools import setup, find_packages

VERSION = "0.0.0.16"

setup(
    name="blazetest-beta",
    version=VERSION,
    author="Abrorjon Ruziboev",
    author_email="abror.ruzibayev@gmail.com",
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    package_data={
        "blazetest": [
            ".dockerignore",
            "Dockerfile",
            "template.yaml",
            "scripts/install_chromedriver.sh",
            "deployment/aws/__main__.py",
            "deployment/aws/.envignore",
            "deployment/aws/requirements.txt",
        ],
    },
    install_requires=[
        "click",
        "pytest",
        "PyYAML",
        "dacite",
        "boto3",
        "licensing",
        "pyopenssl>=23.0.0; python_version >= '3.7'",
        "python-logging-loki",
    ],
    entry_points={
        "console_scripts": [
            "blazetest=blazetest.runner:run_tests",
        ],
    },
)
