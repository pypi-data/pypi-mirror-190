# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['copernic360_cli']

package_data = \
{'': ['*']}

install_requires = \
['click>=8,<9', 'requests>=2.25.1,<3.0.0']

entry_points = \
{'console_scripts': ['copernic360 = copernic360_cli.__main__:cli']}

setup_kwargs = {
    'name': 'copernic360-cli',
    'version': '1.2.7',
    'description': "Command-line script for Kagenova's Copernic360 API",
    'long_description': "# Copernic360\n\n## Overwiew\n\n[Copernic360][product] enables 6 degree-of-freedom (6DOF) motion in standard\n360° VR content to allow users to move freely in scenes.  It consists of two\ncomponents: a Unity plugin; and a [Cloud API][apidoc].\n\nEvery piece of content is different, which is why the Copernic360 Unity plugin\nrequires configuration files with metadata for your content in order to enable\n6DOF support. Copernic360 provides a [Cloud API][apidocs] to preprocess your\ncontent, providing a configuration file that is used by the Unity plugin at\nruntime.\n\n## Command-line tool\n\nThe copernic360 command-line wraps [Kagenova][kagenova]'s Copernic360 [Cloud\nAPI][apidocs].  In short, it allows users to post 360 images and videos and get\nCopernic360 configuration files back.\n\nUsers first need an account with Kagenova's [Copernic360][product]. After\ninstalling the tool via [pip][pip], users can interact with the Copernic360 API\nas follows:\n\n```bash\n# get help\ncopernic360 --help\n# check user login\ncopernic350 check-login\n# check user's credits\ncopernic350 check-credit\n# upload image.jpg and get its configution back (config.6dof)\ncopernic360 process-content image.jpg config.6dof\n# list currently uploaded contents\ncopernic360 contents\n```\n\nSee the command-line help for futher functionality and parameters.\n\n[apidocs]: https://api.copernic360.ai/apidocs\n[kagenova]: https://kagenova.com/\n[product]: https://kagenova.com/products/copernic360/\n[pip]: https://pip.pypa.io/en/stable/\n\nNote that passwords and usernames can be either given on the command-line or in\nthe environment variables:\n\n- `COPERNIC360_USER`\n- `COPERNIC360_PASSWORD`",
    'author': 'Kagenova',
    'author_email': 'None',
    'maintainer': "Mayeul d'Avezac",
    'maintainer_email': 'mayeul.davezac@kagenova.com',
    'url': 'https://kagenova.com/products/copernic360/',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7.1,<4',
}


setup(**setup_kwargs)
