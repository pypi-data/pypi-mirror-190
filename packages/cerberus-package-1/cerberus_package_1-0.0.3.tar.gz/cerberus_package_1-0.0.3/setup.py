#!/usr/bin/env python
import os
from setuptools import find_packages, setup



def readme():
    with open("README.md", encoding='utf-8') as f:
        content = f.read()
    return content
def requirements():
    with open('requirements.txt') as f:
        required = f.read().splitlines()
    return required

setup(
    name="cerberus_package_1",
    version='0.0.3',
    description="first version of package scrfd",
    long_description=readme(),
    author="HoangLM",
    author_email="lhoang17062000@gmail.com",
    classifiers=[  # Optional
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        "Development Status :: 3 - Alpha",
        # Indicate who your project is intended for
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        # Pick your license as you wish
        "License :: OSI Approved :: MIT License",
        # Specify the Python versions you support here. In particular, ensure
        # that you indicate you support Python 3. These classifiers are *not*
        # checked by 'pip install'. See instead 'python_requires' below.
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3 :: Only",
    ],
    packages=find_packages(),
    url= "https://github.com/itachi176/cerberus-face-recognition",
    # requires= requirements()
    install_requires=['numpy', 'onnx', 'onnxruntime', 'opencv-python'],
)

