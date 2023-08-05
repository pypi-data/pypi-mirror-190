# fabexp.py
import click, os, sys, shutil

# get path of package file
dirname = os.path.dirname(__file__)
sys.path.append(dirname)
import modules.ipyCreate as ipyCreate

# get dir of where script is being run (user side)
cwd = os.getcwd()


@click.command()
@click.option("--add", "-a", is_flag=True, help="Creates a new project")
@click.option(
    "--name",
    "-n",
    default="myFabricExperiment",
    show_default=True,
    help="Name of your fabric project",
)
@click.option(
    "--local",
    "-l",
    is_flag=True,
    show_default=True,
    help="Include folder to store local machine scripts",
)
@click.option(
    "--from-template",
    "-f",
    default=None,
    show_default=True,
    help="Template to base your project on",
)


# main program - runs when script is called
def create_project(add, name, local, from_template):
    """
    This tool will help you create new fabric project templates, including
    directory structure. Can also specify to build off a template
    """
    # If -a flag passed
    if add:
        confirmation = input(
            f"Do you want to add a new project titled {name} in the current directory? (yes/no) "
        )
        if confirmation == "yes":
            # Get root directory of PROJECT called name
            rootdir = os.path.join(cwd, name)
            # Create directories - these are default
            os.makedirs(rootdir)
            os.makedirs(os.path.join(rootdir, "upload"))
            os.makedirs(os.path.join(rootdir, "download"))
            os.makedirs(os.path.join(rootdir, "include/img"))
            os.makedirs(os.path.join(rootdir, "logs"))
            # Only create if user wants to run local scripts
            if local:
                os.makedirs(os.path.join(rootdir, "local"))
            # Copy the fabric logo from the package to the new project
            shutil.copy(
                os.path.join(dirname, "modules/img/fabric_logo.png"),
                os.path.join(rootdir, "include/img/fabric_logo.png"),
            )
            # Create the experiment notebook (either from template or from scratch)
            ipyCreate.create_fab_notebook(name, rootdir, from_template)


# Entrypoint
if __name__ == "__main__":
    create_project()
