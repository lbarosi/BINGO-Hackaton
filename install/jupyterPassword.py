#!/usr/bin/env python
from notebook.auth import passwd
input = 'c.NotebookApp.password = u'+"\'" + passwd('cosmos') + "\'"
print(input)
with open('/home/cosmos/.jupyter/jupyter_notebook_config.py', 'a') as file:
    file.write(input)
