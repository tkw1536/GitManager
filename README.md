# GitManager

A script that can handle multiple Git repositories locally. 

## Installation

Make sure python is installed, then run

```bash
python setup.py install
```
to install the package. This will make it available by running ```git-manager``` or ```git manager```. 

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
    Groups completly support nesting. A sub-groups path and pattern for origin are relative to 
    the parent group. To create a sub-group, add another ">" character in front of the line. 


An example configuration file can be found in the file [config_example](config_example). 

## Usage

TODO: Document this

## License

TODO: Document this