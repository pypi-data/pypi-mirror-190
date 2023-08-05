from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="fastapi_allauth",
    version="0.1.1",
    author="villain",
    author_email="sehwa98@icloud.com",
    description="the simplest fastapi oauth package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/K-villain/fastapi-allauth",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    install_requires=[
        "fastapi>=0.88.0",
        "pydantic>=1.8.2",
        "starlette>=0.14.2",
        "PyJWT>=2.6.0"
    ],
    packages=find_packages(),
)
