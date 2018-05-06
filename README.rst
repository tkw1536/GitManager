GitManager
==========

|Build Status| |PyPI version|

A script that can handle multiple Git repositories locally. Written in
Python, supports version 3.5 and upwards.

Installation
------------

Make sure python is installed, then run

.. code:: bash

    # install from a clone of the repository
    python setup.py install

or

.. code:: bash
    
    # install from PyPi
    pip install git_manager

to install the package. This will make it available by running
:code:`git-manager` (or :code:`git manager`).

Configuration
-------------

Git Manager can be configured through its configuration file. In order,
it looks for the configuration file in the following locations:

1. :code:`$GIT_MANAGER_CONFIG` (if set)
2. :code:`~/.config/.gitmanager/config` (or
   :code:`$XDG_CONFIG_HOME/.gitmanager/config` if set)
3. :code:`~/.gitmanager`

The configuration file is parsed line-by-line and declares which
repositories are under GitManager control. It consists of three
different types of directives:

1. **Root Line** Configure the root folder to clone repositories to
   automatically. Starts with two hashes, then sets the folder relative
   to the users home directory. For example:

   .. code:: text

       ## /opt/repositories

2. **Comments** Anything starting with a “#” will be treated as a
   comment. The same goes for empty (or whitespace-only) lines.
3. **Repository instruction** To declare a repository write
   :code:`REPOSITORY_URL  [FOLDER]`. This declares that the repository
   from `REPOSITORY_URL` should be cloned into the folder `FOLDER`.
   In case the folder is omitted, the ‘humanish’ part of the URI will be
   taken automatically. All folder paths by default are relative to the
   users home folder, but this can be changed with the instruction
   below. Example:

   .. code:: text

      # makes the git/git repository available locally
      # in the folder ~/Projects/git
      https://github.com/git/git Projects/git

      # makes the GitManager repository available
      # in the folder ~/GitManager
      https://github.com/tkw1536/GitManager

4. **Group Instruction** In the case where multiple repositories should
   be cloned into the same folder, it is inconvenient to always give the
   full path to that folder in the configuration file. For this reason
   GitManager supports the concept of a group. A group can be started by
   prefixing a line with the “>” character. A group takes one argument.
   A path to a folder all repositories should be cloned into. This is
   best illustrated in the form of an example:

   .. code:: text

      # We can create a group to store all our atom-related projects.
      # All repositories are automatically available in the ~/AtomProjects
      # folder.
      > AtomProjects
        https://github.com/atom/atom
        https://github.com/atom/markdown-preview

      # makes the GitManager repository available
      # in the folder ~/GitManager
      https://github.com/tkw1536/GitManager

   Groups completely support nesting. A sub-groups path and
   pattern for origin are relative to the parent group. To create a
   sub-group, add another “>” character in front of the line.

An example configuration file can be found in the file
`config_example <config_example>`__.

Installing Repositories Locally
-------------------------------

Setup
~~~~~

.. image:: examples/setup.gif

Use :code:`git-manager setup [pattern]` to clone repositories in the config file to the local disk. 
Use the optional pattern argument to restrict the reposiories to install. 

Clone
~~~~~

.. image:: examples/clone.gif

Use :code:`git-manager clone [--save] url` to automatically clone a repository into a location determined by the URL. 
Use the :code:`--save` flag to automatically update the config file. 


Reconfigure
~~~~~~~~~~~

.. image:: examples/reconfigure.gif

Use :code:`git-manager reconfigure` to automatically add repositories found in folder and it's subdirectories to the configuration file. 


Viewing Local Repositories
--------------------------

List
~~~~

.. image:: examples/ls.gif

Use :code:`git-manager ls [pattern]` to list local repositories. 
Use the optional pattern argument to restrict the repositories to list. 

Status
~~~~~~

.. image:: examples/status.gif

Use :code:`git-manager status [pattern]` to show the status of local repositories.  
Use the optional pattern argument to restrict the repositories to check. 

State
~~~~~~

.. image:: examples/state.gif

Use :code:`git-manager state [pattern]` to compare local repositories with their remote counterpart. 
Use the optional pattern argument to restrict the repositories to check. 

Updating Local Repositories
---------------------------

Pull
~~~~

.. image:: examples/pull.gif

Use :code:`git-manager pull [pattern]` to run :code:`git pull` on all repositories installed locally. 
Use the optional pattern argument to restrict the repositories to pull. 

Fetch
~~~~~

Use :code:`git-manager fetch [pattern] [args...]` to run :code:`git fetch` on all repositories installed locally. 
Use the optional pattern argument to restrict the repositories to fetch. 
Use the optional remaining arguments to pass further arguments to the fetch command. 

Push
~~~~

Use :code:`git-manager push [pattern]` to run :code:`git push` on all repositories installed locally. 
Use the optional pattern argument to restrict the repositories to pull. 

GC
~~~

Use :code:`git-manager gc [pattern] [args...]` to run :code:`git gc` on all repositories installed locally. 
Use the optional pattern argument to restrict the repositories to garbage collect. 
Use the optional remaining arguments to pass further arguments to the gc command. 

Repository Patterns
-------------------

Some commands optionally accept the :code:`pattern` argument. This can be
used to filter repository by their name.

Repository patterns are simple `glob-like` pattern matches on
standardized remote URLs. They can also be normal glob patterns on full
URLs.

For example:

+--------------------------+------------------------------------------+
| Pattern                  | Examples                                 |
+==========================+==========================================+
| :code:`world`            | :code:`git@github.com:hello/world.git`,  |
|                          | :code:`https://github.com/hello/world`   |
+--------------------------+------------------------------------------+
| :code:`hello/*`          | :code:`git@github.com:hello/earth.git`,  |
|                          | :code:`git@github.com:hello/mars.git`    |
+--------------------------+------------------------------------------+
| :code:`hello/m*`         | :code:`git@github.com:hello/mars.git`,   |
|                          | :code:`git@github.com:hello/mercury.git` |
+--------------------------+------------------------------------------+
| :code:`github.com/*/*`   | :code:`git@github.com:hello/world.git`,  |
|                          | :code:`git@github.com:bye/world.git`     |
+--------------------------+------------------------------------------+
| :code:`github.com/hello` | :code:`git@github.com:hello/world.git`,  |
|                          | :code:`git@github.com:hello/mars.git`    |
+--------------------------+------------------------------------------+

Development and Testing
-----------------------

This project is unit tested with a high coverage rate. The tests can be
run with:

.. code:: bash

    nosetests --with-coverage --cover-package GitManager

Tests are automatically run on Travis CI after every commit.

License
-------

::

    The MIT License (MIT)

    Copyright (c) 2016-18 Tom Wiesing

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

.. |Build Status| image:: https://travis-ci.org/tkw1536/GitManager.svg?branch=master
   :target: https://travis-ci.org/tkw1536/GitManager
.. |PyPI version| image:: https://badge.fury.io/py/git_manager.svg
   :target: https://pypi.python.org/pypi/git_manager
