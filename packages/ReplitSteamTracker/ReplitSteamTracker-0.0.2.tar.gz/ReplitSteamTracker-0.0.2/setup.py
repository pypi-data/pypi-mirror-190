from setuptools import setup, find_packages
import codecs
import os
from pathlib import Path

VERSION = '0.0.2'
DESCRIPTION = 'Checks Steam Game Pricing'
LONG_DESCRIPTION = 'A package that allows to build simple streams of video, audio and camera data.'

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

# Setting up
setup(
    name="ReplitSteamTracker",
    version=VERSION,
    author="Follen",
    author_email="<binor15175@brandoza.com>",
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'video', 'stream', 'video stream', 'camera stream', 'sockets'],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)