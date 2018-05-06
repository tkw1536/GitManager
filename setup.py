import os
from setuptools import setup, find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name="git_manager",
    version="0.2.0",

    url="https://github.com/tkw1536/GitManager",
    author="Tom Wiesing",
    author_email="tkw01536@gmail.com",


    packages=find_packages(),
    scripts=['git-manager'],

    description="Manages multiple git repositories",
    long_description=read('README.rst'),

    license="MIT",

    classifiers=[
        "Programming Language :: Python :: 3",

        "License :: OSI Approved :: MIT License",

        "Intended Audience :: Developers",
        "Topic :: Utilities",
    ]
)
