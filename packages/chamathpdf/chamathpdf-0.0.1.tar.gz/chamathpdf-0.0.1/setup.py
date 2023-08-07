import setuptools
from pathlib import Path

setuptools.setup(
    name="chamathpdf",
    version="0.0.1",
    author="Chamath",
    author_email="anpch@example.com",
    description="A simple python package to generate PDFs from Chamath",
    long_description=Path("README.md").read_text(),
    long_description_content_type="text/markdown",
    url="https://github.com/chamath/chamathpdf",
    packages=setuptools.find_packages(exclude=["tests", "data"])

)