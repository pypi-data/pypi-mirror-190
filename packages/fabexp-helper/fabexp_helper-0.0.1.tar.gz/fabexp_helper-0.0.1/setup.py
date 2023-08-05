# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['fabexp_helper', 'fabexp_helper.modules']

package_data = \
{'': ['*'],
 'fabexp_helper.modules': ['img/*',
                           'templates/accessing_ipv4_services_from_ipv6_nodes/*',
                           'templates/accessing_ipv4_services_from_ipv6_nodes/upload/*',
                           'templates/basic_gpu_devices/*',
                           'templates/basic_nvme_devices/*',
                           'templates/benchmarking_storage/*',
                           'templates/create_l2network_basic/*',
                           'templates/create_l2network_wide_area/*',
                           'templates/create_l3network_fabnet_ipv4/*',
                           'templates/create_l3network_fabnet_ipv6/*',
                           'templates/create_slice/*',
                           'templates/customizing_nodes/*',
                           'templates/delete_slice/*',
                           'templates/fablib_common/*',
                           'templates/facility_port/*',
                           'templates/get_nodes/*',
                           'templates/hello_fabric/*',
                           'templates/hello_fabric/include/figs/*',
                           'templates/parallel_config/*',
                           'templates/persistent_storage/*',
                           'templates/renew_slice/*',
                           'templates/save_and_load/*',
                           'templates/sites_and_resources/*',
                           'templates/slices/*',
                           'templates/ssh_to_nodes/*',
                           'templates/upload_and_execute/*',
                           'templates/upload_and_execute/upload/*']}

install_requires = \
['click>=8.1.3,<9.0.0', 'nbformat>=5.7.3,<6.0.0']

entry_points = \
{'console_scripts': ['fabexp = fabexp_helper.fabexp:create_project']}

setup_kwargs = {
    'name': 'fabexp-helper',
    'version': '0.0.1',
    'description': 'A tool to help create and manage fabric experiments',
    'long_description': '# fabexp-helper\nA CLI to help create new fabric project templates in an effort to standardize experiment structure.\n\n## Usage\n`fabexp --add (-a) --name (-n) <fabric project name> --local (-l) --from-template (-f) TEMPLATE_NAME`\n- Replace <fabric project name> with a desired name\n- `--add`: required to add project\n- `--name`: optional, default: myFabricExperiment\n- `--local`: add folder for executing local scripts, default: False\n- `--from_template`: create project from template. Names are any valid jupyter example name.\n    * Find project name from folder of jupyter examples\n    * Examples: hello_fabric, create_l2network_basic\n    * Only including examples from **fablib_api** folder for now.\nOnce you run the above command, you should see a new set of folders that serve as a template\nfor your fabric project.',
    'author': 'Devin Lane',
    'author_email': 'silvertenor@icloud.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
