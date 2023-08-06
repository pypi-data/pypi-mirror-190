# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['ecspylibs']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'ecspylibs',
    'version': '1.1.12',
    'description': 'Local python libraries used across multiple programs.',
    'long_description': '# -*- coding: utf-8 -*-\n#\n# Do NOT edit this system file by hand -- use git.\n# See "URL to git source" below.\n#\n# Author:        $Id: Thomas R. Stevenson <aa0026@wayne.edu> $\n#\n# Last Changed:  $Date: Thu Jan 26 11:02:02 2023 -0500 $\n#\n# URL to git source: $URL: git@git.wayne.edu:ECS_Projects/ECSpylibs.git $\n#\n# ECSpylibs\n\n-rw-rw-r--. 1 tom tom 2380 Jan 18 14:55 ecspylibs/buildfunctionlist.py\n-rw-rw-r--. 1 tom tom 7651 Jan 18 14:55 ecspylibs/checkservice.py\n-rw-rw-r--. 1 tom tom 2679 Jan 18 14:55 ecspylibs/cleanuptempdirs.py\n-rwxr-xr-x. 1 tom tom  465 Nov  5  2020 ecspylibs/__init__.py\n-rw-rw-r--. 1 tom tom 3670 Jan 18 14:55 ecspylibs/initsetup.py\n-rw-rw-r--. 1 tom tom 5357 Jan 18 14:55 ecspylibs/parseemail.py\n-rw-rw-r--. 1 tom tom 3264 Jan 18 14:55 ecspylibs/parsexml.py\n-rw-rw-r--. 1 tom tom 3644 Jan 18 14:55 ecspylibs/password.py\n-rw-rw-r--. 1 tom tom 1751 Jan 18 14:55 ecspylibs/reapchildren.py\n-rw-rw-r--. 1 tom tom 3250 Jan 18 14:55 ecspylibs/sendemail.py\n\nThe GIT Home can be found [Here][ECSPYLIBS].\nThe README file can be found [Here][README].\nThe LICENSE file can be found [Here][LICENSE].\nThe ChangeLog file can be found [Here][CHANGELOG].\nThe pyproject.toml file can be found [Here][PYPROJECT].\nMy contact information can be found [Here][About Me].\n\n[ECSPYLIBS]: https://git.wayne.edu/aa0026/ecspylibs\n[README]: https://git.wayne.edu/aa0026/ecspylibs/-/blob/master/README.md\n[LICENSE]: https://git.wayne.edu/aa0026/ecspylibs/-/blob/master/LICENSE.txt\n[CHANGELOG]: https://git.wayne.edu/aa0026/ecspylibs/-/blob/master/ChangeLog\n[PYPROJECT]: https://git.wayne.edu/aa0026/ecspylibs/-/blob/master/pyproject.toml\n[About Me]: https://About.Me/Thomas.R.Stevenson\n',
    'author': 'Thomas R. Stevenson',
    'author_email': 'aa0026@wayne.edu',
    'maintainer': 'Thomas R. Stevenson',
    'maintainer_email': 'aa0026@wayne.edu',
    'url': 'https://git.wayne.edu/ECS_Projects/ECSpylibs.git',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
