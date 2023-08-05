# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['jupyter2hashnode']

package_data = \
{'': ['*'], 'jupyter2hashnode': ['nbconvert/templates/hashnode/*']}

install_requires = \
['Pillow>=9.1.0,<10.0.0',
 'nbconvert[all]>=6.4.0,<7.0.0',
 'python-dotenv>=0.15.0,<0.16.0',
 'requests>=2.20.0,<3.0.0',
 'typer[all]>=0.7.0,<0.8.0']

extras_require = \
{'docs': ['Sphinx==5.3.0',
          'sphinx-rtd-theme>=1.1.1,<2.0.0',
          'nbsphinx>=0.8.12,<0.9.0']}

entry_points = \
{'console_scripts': ['rick-portal-gun = jupyter2hashnode.cli:app']}

setup_kwargs = {
    'name': 'jupyter2hashnode',
    'version': '0.1.14a4',
    'description': 'Export from jupyter notebook into hashnode blog articles',
    'long_description': '# jupyter2hashnode package\nPackage to export from jupyter notebook into a hashnode blog\n\n\nResources:\n\nPython package that wrappes HASHNODE API\nhttps://github.com/JosiasAurel/python-hashnode/blob/master/hashnode/hashnode.py\nhttps://www.realpythonproject.com/how-to-use-python-to-post-on-popular-blogging-websites/\n\nExample to call HASHNODE image uploader API\nhttps://github.com/Strajk/setup/blob/master/programs/hashnode-md-uploader.mjs\n\nMarkdownExporter example to export notebook to markdown\nhttps://gist.github.com/connerxyz/df8e1a2d3915aade869c968725c15cf3\n\nFor Documentation\nhttps://gist.github.com/GLMeece/222624fc495caf6f3c010a8e26577d31',
    'author': 'Tiago Patricio Santos',
    'author_email': 'tiagopatriciosantos@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/tiagopatriciosantos/jupyter2hashnode',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
