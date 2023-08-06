from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.0'
DESCRIPTION = ''
LONG_DESCRIPTION = ''

# Setting up
setup(
    name="DIVY_DATA_SET",
    version=VERSION,
    author="DIVYANSH",
    author_email="shukladivyansh953@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=["chatbot"],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)