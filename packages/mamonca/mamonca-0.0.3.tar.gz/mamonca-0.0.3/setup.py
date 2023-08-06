from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="mamonca",
    version="0.0.3",
    author="samwaseda",
    author_email="waseda@mpie.de",
    description="Mamonca - interactive Magnetic Monte Carlo code",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/samwaseda/mamonca",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
    license='BSD'
)
