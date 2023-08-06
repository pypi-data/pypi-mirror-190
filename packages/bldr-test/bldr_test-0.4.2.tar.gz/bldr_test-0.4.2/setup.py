# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['bldr_test']

package_data = \
{'': ['*']}

install_requires = \
['typer[all]>=0.7.0,<0.8.0']

entry_points = \
{'console_scripts': ['bldrtst = bldr_test.main:app']}

setup_kwargs = {
    'name': 'bldr-test',
    'version': '0.4.2',
    'description': '',
    'long_description': '\n![tests_badge](https://github.com/ethanmsl/bldr_test/actions/workflows/test-poet.yml/badge.svg)\n\n\nThis is the `README.md`.  It is being pulled into the markdown files by pdoc.  \n[This is a link to the GitHub Pages site](https://ethanmsl.github.io/bldr_test/bldr_test.html) hosting the auto-generated documentation.\n\n**bold**  \n*italic*  \n~~strikethrough~~  \n\n# Header\n\nLink: [bldr-test on TestPyPi](https://test.pypi.org/project/bldr-test/)\n\nuse, install:\n```zsh\npip3 list\necho\npip3 install -i https://test.pypi.org/simple/ bldr-test\necho\npip3 list\n```\n\nuse, run:\n```zsh\npython3 -m bldr_test\n```\n\nuse, uninstall:\n```zsh\npip3 list\necho\npip3 uninstall bldr-test\necho\npip3 list\n```\n\n(Note: `-` vs. `_` above intended.  Also note: the `echo` commands are merely for more legible output)\n',
    'author': 'Ethan Skowronski-Lutz',
    'author_email': '33399972+ethanmsl@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
