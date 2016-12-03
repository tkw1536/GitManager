import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name="git_manager",
    version="0.0.2",

    url="https://github.com/tkw1536/GitManager",
    author="Tom Wiesing",
    author_email="tkw01536@gmail.com",

    py_modules=['GitManager', 'GitManager.config', 'GitManager.format', 'GitManager.main', 'GitManager.vcs'],
    scripts=['git-manager'],

    description=("A script that can handle multiple Git repositories locally. "),
    long_description=read('README.md'),

    license="MIT",

    classifiers=[
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",

        "License :: OSI Approved :: MIT License",

        "Intended Audience :: Developers",
        "Topic :: Utilities",
    ]
)
