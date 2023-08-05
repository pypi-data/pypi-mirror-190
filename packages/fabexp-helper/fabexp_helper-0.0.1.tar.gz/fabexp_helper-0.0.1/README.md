# fabexp-helper
A CLI to help create new fabric project templates in an effort to standardize experiment structure.

## Usage
`fabexp --add (-a) --name (-n) <fabric project name> --local (-l) --from-template (-f) TEMPLATE_NAME`
- Replace <fabric project name> with a desired name
- `--add`: required to add project
- `--name`: optional, default: myFabricExperiment
- `--local`: add folder for executing local scripts, default: False
- `--from_template`: create project from template. Names are any valid jupyter example name.
    * Find project name from folder of jupyter examples
    * Examples: hello_fabric, create_l2network_basic
    * Only including examples from **fablib_api** folder for now.
Once you run the above command, you should see a new set of folders that serve as a template
for your fabric project.