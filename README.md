# GitManager

[![Build Status](https://travis-ci.org/tkw1536/GitManager.svg?branch=master)](https://travis-ci.org/tkw1536/GitManager)

A script that can handle multiple Git repositories locally.
Written in Python, supports version 3.5 and upwards.

## Installation

Make sure python is installed, then run

```bash
python setup.py install
```
to install the package. This will make it available by running ```git-manager``` (or ```git manager```). 

## Usage

Git-Manager has different commands it provides:

1. ```git-manager setup``` -- Sets up all repositories as configured in the Configuration file.
2. ```git-manager fetch``` -- Updates all local repositories by fetching all
 data from the remotes.
3. ```git-manager pull``` -- Updates all local repositories by pulling all
repositories.
4. ```git-manager ls``` -- Lists all locally available repositories.
5. ```git-manager status``` -- Shows all repositories that do not have a
clean working tree, i.e. those where ```git status``` shows a message.
5. ```git-manager state``` -- Shows all repositories for which the local
branch is not equal to the remote branch.

## Configuration

Git Manager can be configured through its configuration file. 
In order, it looks for the configuration file in the following locations: 

1. ```$GIT_MANAGER_CONFIG``` (if set)
2. ```~/.config/.gitmanager/config``` (or ```$XDG_CONFIG_HOME/.gitmanager/config``` if set)
3. ```~/.gitmanager```

The configuration file is parsed line-by-line and declares which repositories are under
GitManager control. It consists of three different types of directives: 

1. **Comments**. 
    Anything starting with a "#" will be treated as a comment. The same goes for empty (or whitespace-only)
    lines. 
2. **Repository instruction**
    To declare a repository write ```REPOSITORY_URL  \[FOLDER\]```. This declares that the repository
    from ```REPOSITORY_URL``` should be cloned into the folder ```FOLDER```. In case the folder is omitted,
    the 'humanish' part of the URI will be taken automatically. All folder paths by default are relative to 
    the users home folder, but this can be changed with the instruction below. Example:
    ```
    # makes the git/git repository available locally in the folder ~/Projects/git
    https://github.com/git/git Projects/git
    
    # makes the  GitManager repository available in the ~/GitManager repository
    https://github.com/tkw1536/GitManager
    ```
3. **Group Instruction**. 
    In the case where multiple repositories should be cloned into the same folder, it is inconvenient to
    always give the full path to that folder in the configuration file. For this reason GitManager supports
    the concept of a group. A group can be started by prefixing a line with the ">" character. A group takes
    two arguments: A path to a folder all repositories should be cloned into, and a pattern to be used for
    repository origins. The second argument is optional. This is best illustrated in the form of an example: 
     ```
    # We can create a group to store all our atom-related projects. 
    # All repositories are automatically available in the ~/AtomProjects folder. 
    > AtomProjects
       https://github.com/atom/atom
       https://github.com/atom/markdown-preview
       # ...
    
    # Sometimes we are cloning from a very similar URL, say all of them from the same github user. 
    # In this case we could also replace the example above with_
    
    > AtomProjects https://github.com/atom/%s
       atom
       markdown-preview
       # ...
     ```
    Groups completely support nesting. A sub-groups path and pattern for origin are relative to
    the parent group. To create a sub-group, add another ">" character in front of the line. 


An example configuration file can be found in the file [config_example](config_example).

## Development and Testing

This project is unit tested with a high coverage rate.
The tests can be run with:

```bash
    nosetests --with-coverage --cover-package GitManager
```

Tests are automatically run on Travis CI after every commit.

## License

```
The MIT License (MIT)

Copyright (c) 2016-17 Tom Wiesing

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```