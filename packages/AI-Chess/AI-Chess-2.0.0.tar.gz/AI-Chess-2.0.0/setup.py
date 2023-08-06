from setuptools import setup, find_packages
import codecs
import os

VERSION = '2.0.0'
DESCRIPTION = 'Basic chess features that includes an AI for decision making'

# Setting up
setup(
    name="AI-Chess",
    version=VERSION,
    author="mtootoonchi (Matthew Faraz Tootoonchi)",
    author_email="<mftootoonchi@gmail.com>",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=['chess'],
    keywords=['python', 'chess', 'AI', 'Artificial Intelligence', 'game', 'puzzle'],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.7",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)