# version_releaser
This is an experimental project that produces release notes between two tags
based on the commit messages.

#usage
call `main.py` with arguments :
 - `-i` for the relative path of the directory of the git project 
 - `-f` for the from tag (e.g v1.0.0)
 - `-t` for the to tag (e.g v1.2.0)
 - `-o` for the output file name (as a path e.g ../dist/release_notes.html) 
 
