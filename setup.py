#!/usr/bin/env python3
"""
Setup script for the video subtitling tool.
"""

from setuptools import setup, find_packages
import os
import re

# Read version from __init__.py
with open(os.path.join("subtitler", "__init__.py"), "r") as f:
    version_match = re.search(r'__version__ = "(.*?)"', f.read())
    version = version_match.group(1) if version_match else "0.1.0"

# Read long description from README.md if it exists
long_description = ""
if os.path.exists("README.md"):
    with open("README.md", "r") as f:
        long_description = f.read()

setup(
    name="subtitler",
    version=version,
    description="A CLI tool to add English subtitles to videos with non-English audio in various languages",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="silvanm",
    author_email="",
    url="https://github.com/silvanm/subtitler",
    license="MIT",
    keywords=["subtitles", "video", "translation", "whisper", "ffmpeg", "cli"],
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "subtitler=subtitler.main:main",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Multimedia :: Video",
    ],
    python_requires=">=3.6",
    install_requires=[
        # No direct Python dependencies as ffmpeg and whisper are external tools
    ],
    extras_require={
        "dev": [
            "pytest>=6.0.0",
            "black>=21.5b2",
            "isort>=5.9.1",
            "flake8>=3.9.2",
        ],
    },
)
