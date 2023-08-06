# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['jupyter2hashnode']

package_data = \
{'': ['*'],
 'jupyter2hashnode': ['examples/*', 'nbconvert/templates/hashnode/*']}

install_requires = \
['Pillow>=9.1.0,<10.0.0',
 'nbconvert[all]>=6.4.0,<7.0.0',
 'python-dotenv>=0.15.0,<0.16.0',
 'requests>=2.20.0,<3.0.0',
 'typer[all]>=0.7.0,<0.8.0']

extras_require = \
{'docs': ['Sphinx==5.3.0', 'sphinx-rtd-theme==1.1.1', 'nbsphinx==0.8.12']}

entry_points = \
{'console_scripts': ['rick-portal-gun = jupyter2hashnode.cli:app']}

setup_kwargs = {
    'name': 'jupyter2hashnode',
    'version': '0.1.14',
    'description': 'Export from jupyter notebook into hashnode blog articles',
    'long_description': '# Using `jupyter2hashnode` as a command line tool\n\njupyter2hashnode converts the specified Jupyter Notebook to a Hashnode publication story, \ncompressing images, uploading images to the Hashnode server, and replacing image URLs \nin the markdown file, then published.\n\nIf jwt, token, publication_id arguments not passed then will use environment variables HASHNODE_JWT, HASHNODE_TOKEN, HASHNODE_PUBLICATION_ID. \n\nNotes:\n\nTo obtain JWT: Open https://hashnode.com, account must be logged in, open DevTools of chrome browser (F12), go to Application tab, go to Cookies, find and copy value of "jwt" cookie (245 characters)\n\nTo obtain Hashnode API token: Open https://hashnode.com/settings/developer, click on "Generate New Token" button or use the existing one\n\nTo obtain Publication ID: Go to https://hashnode.com/settings/blogs, click "Dashboard" of the blog you want to upload to, copy the ID, e.g. https://hashnode.com/<id>/dashboard\n\n**Usage**:\n\n```console\n$ jupyter2hashnode [OPTIONS] NOTEBOOK_PATH [OUTPUT_PATH]\n```\n\n**Arguments**:\n\n* `NOTEBOOK_PATH`: notebook file name or complete path  [required]\n* `[OUTPUT_PATH]`: output folder name or complete output path where the files will be written to, if none creates output folder with the same name as the notebook file name\n\n**Options**:\n\n* `-j, --jwt TEXT`: JWT token for authentication at https://hashnode.com/api/upload-image.\n* `-t, --token TEXT`: Token for authentication at https://api.hashnode.com  mutation createPublicationStory endpoint\n* `-p, --publication TEXT`: ID of the Hashnode publication e.g. https://hashnode.com/<id>/dashboard\n* `--title TEXT`: Article title  [required]\n* `--hide-from-feed / --no-hide-from-feed`: Hide this article from Hashnode and display it only on your blog  [default: True]\n* `--delete-files / --no-delete-files`: Delete all files after creating the publication story  [default: True]\n* `--upload / --no-upload`: Upload the publication story to the Hashnode server  [default: True]\n* `-v, --version`: Show the application\'s version and exit.\n* `--install-completion`: Install completion for the current shell.\n* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.\n* `--help`: Show this message and exit.\n\n\n# Using `jupyter2hashnode` as a library\n\nclass Jupyter2Hashnode\n\nThe Jupyter2Hashnode class is used to convert Jupyter Notebooks to Hashnode publication stories by compressing images, uploading images to the Hashnode server, and replacing image URLs in the markdown file.\n\nNotes:\n- To obtain JWT\n    1. Open https://hashnode.com, account must be logged in\n    2. Open DevTools of chrome browser (F12)\n    3. Go to Application tab\n    4. Go to Cookies\n    5. Find and copy value of "jwt" cookie (245 characters)\n- To obtain Hashnode API token\n    1. Open https://hashnode.com/settings/developer\n    2. Click on "Generate New Token" button or use the existing one\n- To obtain Publication ID\n    1. Go to https://hashnode.com/settings/blogs\n    2. Click on "Dashboard" button of the blog you want to upload to\n    3. Copy ID from the URL, e.g. https://hashnode.com/<id>/dashboard\n- \n\nAttributes:\nHASHNODE_JWT (str): JWT token for authentication with the Hashnode image uploader, https://hashnode.com/api/upload-image.\nHASHNODE_TOKEN (str): Token for authentication with the Hashnode server, to use https://api.hashnode.com  mutation createPublicationStory endpoint\nHASHNODE_PUBLICATION_ID (str): ID of the Hashnode publication e.g. https://hashnode.com/<id>/dashboard\nMethods:\ncreate_publication_story(title:str, notebook_path: str, output_path:Optional[str]=None, delete_files:bool=True, upload:bool=True):\nCreates a publication story on the Hashnode blog platform by converting a Jupyter Notebook to a markdown file, compressing images, uploading images to the Hashnode server, and replacing image URLs in the markdown file.\n\n**Usage**:\n\n```console\n$ jupyter2hashnode [OPTIONS] HASHNODE_JWT HASHNODE_TOKEN HASHNODE_PUBLICATION_ID\n```\n\n**Arguments**:\n\n* `HASHNODE_JWT`: [required]\n* `HASHNODE_TOKEN`: [required]\n* `HASHNODE_PUBLICATION_ID`: [required]\n\n**Options**:\n\n* `--install-completion`: Install completion for the current shell.\n* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.\n* `--help`: Show this message and exit.',
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
