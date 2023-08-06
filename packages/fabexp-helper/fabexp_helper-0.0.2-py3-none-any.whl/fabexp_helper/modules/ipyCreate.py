import nbformat as nbf, os, shutil, ntpath
from datetime import date
from getpass import getuser


def create_fab_notebook(name, rootdir, from_template):
    # If creating from scratch
    if not from_template:
        # Create new notebook
        nb = nbf.v4.new_notebook()
        # Initialize markdown cells
        text = [
            f"""\
<img src="./include/img/fabric_logo.png" width="500"/>

# {name}
```
Created: {date.today()}
Last Modified: 
{getuser()}
Clemson University
<username>@clemson.edu
```

<div style="page-break-after: always; visibility: hidden"> 
\pagebreak 
</div>""",
        ]
        # Initialize code cells
        code = [
            """\
from fabrictestbed_extensions.fablib.fablib import FablibManager as fablib_manager

try:
    fablib = fablib_manager()
                    
    fablib.show_config()
except Exception as e:
    print(f"Exception: {e}")""",
            """\
# Clean up log directory to avoid large files
import os
for item in os.scandir(os.path.join(os.getcwd(), 'logs')):
    if '.' != item.name[0]:
        os.remove(item.path)""",
        ]
        # Add cells to notebook object
        nb["cells"] = [
            nbf.v4.new_markdown_cell(text[0]),
            nbf.v4.new_code_cell(code[0]),
            nbf.v4.new_code_cell(code[1]),
        ]
        # Create notebook in new project dir
        nbf.write(nb, rootdir + f"/{name.lower()}.ipynb")
        # Skip next part
        return
    # dirname of pip package location's ipycreate.py
    dirname = os.path.dirname(__file__)
    template_path = os.path.join(dirname, f"templates/{from_template}")
    # If from_template specified
    if not os.path.exists(template_path):
        # Check if user entered a full path
        if os.path.exists(from_template):
            from_template = ntpath.basename(from_template)
            shutil.copy(from_template, os.path.join(rootdir, from_template))
        # Check if user entered local path
        elif os.path.exists(path := os.path.join(os.getcwd(), from_template)):
            shutil.copy(path, os.path.join(rootdir, from_template))
        else:
            print("Error: Incorrect usage of -f. Make sure template name is valid.")
        return

    # Iterate through items in case subfolders/more than one file exists
    for item in os.scandir(template_path):
        if os.path.isdir(item.path):
            shutil.copytree(
                item.path, os.path.join(rootdir, item.name), dirs_exist_ok=True
            )
        else:
            shutil.copy(item.path, os.path.join(rootdir, item.name))
