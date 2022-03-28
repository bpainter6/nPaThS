from os.path import join
from glob import glob

import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="nPaThS",
    version="0.0.1",
    author="Bailey Painter",
    author_email="bpainter6@gatech.edu",
    description="An 'n-channel, Pandas-based, Thermohydraulic Solver' (nPaThS) \
    for solving flow conditions and temperatures in LWR cores",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bpainter6/nPaThs",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    packages=['npaths','examples','tests','npaths.checkerrors','npaths.functions',
              'npaths.objects'],
)
