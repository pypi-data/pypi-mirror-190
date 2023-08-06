from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='flask_api_sdk',
    version='0.1.0',
    description='A pip packaged Python SDK for a Flask API',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/<username>/flask_api_sdk',
    author='Author Name',
    author_email='author_email@example.com',
    packages=find_packages(),
    install_requires=[
        'flask',
        'requests',
        # ... other dependencies
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
