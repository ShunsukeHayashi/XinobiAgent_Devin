from setuptools import setup, find_packages

setup(
    name="devin_api_integration",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "requests>=2.0.0",
        "pydantic>=2.0.0",
    ],
)
