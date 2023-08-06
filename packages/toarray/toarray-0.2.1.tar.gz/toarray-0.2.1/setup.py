import pathlib
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()

setup(
    name="toarray",
    version="0.2.1",
    description="Small Python package for converting iterables to arrays.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/eddiethedean/toarray",
    author="Odos Matthews",
    author_email="odosmatthews@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
    ],
    packages=find_packages(),
    include_package_data=True,
    python_requires='>=3.6',
    install_requires=['more_itertools']
)