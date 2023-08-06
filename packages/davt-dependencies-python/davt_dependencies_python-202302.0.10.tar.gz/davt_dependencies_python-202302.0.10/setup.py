# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['davt_dependencies_python']

package_data = \
{'': ['*']}

install_requires = \
['Sphinx>=5.2.1,<6.0.0',
 'adal>=1.2.7,<2.0.0',
 'azure-common>=1.1.28,<2.0.0',
 'azure-identity>=1.10.0,<2.0.0',
 'azure-keyvault-secrets>=4.5.0,<5.0.0',
 'azure-keyvault>=4.2.0,<5.0.0',
 'azure-storage-file-datalake>=12.8.0,<13.0.0',
 'boto3==1.21.18',
 'botocore==1.24.18',
 'chardet>=5.0.0,<6.0.0',
 'docutils==0.17.1',
 'markdown>=3.4.1,<4.0.0',
 'myst-parser>=0.18.0,<0.19.0',
 'nbconvert>=6.5.1,<7.0.0',
 'numpy>=1.23.0,<2.0.0',
 'opencensus-ext-azure>=1.1.7,<2.0.0',
 'opencensus>=0.11.0,<0.12.0',
 'openpyxl>=3.0.4,<4.0.0',
 'pathlib>=1.0.1,<2.0.0',
 'pip-system-certs>=4.0,<5.0',
 'pyarrow>=10.0.1,<11.0.0',
 'pygments>=2.13.0,<3.0.0',
 'pyreadstat>=1.1.9,<2.0.0',
 'pytest-cov>=4.0.0,<5.0.0',
 'pytest>=7.1.2,<8.0.0',
 'python-dateutil>=2.8.2,<3.0.0',
 'python-dotenv>=0.20.0,<0.21.0',
 'requests>=2.28.1,<3.0.0',
 'rsconnect-jupyter>=1.6.0,<2.0.0',
 'setuptools==65.6.3',
 'sphinx-autoapi>=2.0.0,<3.0.0',
 'sphinx-autodoc-typehints>=1.19.5,<2.0.0',
 'sphinx-markdown-builder>=0.5.5,<0.6.0',
 'sphinx-markdown-tables>=0.0.17,<0.0.18',
 'sphinx-rtd-theme>=1.1.1,<2.0.0',
 'sphinx-sitemap>=2.2.0,<3.0.0',
 'sphinx-sql>=1.3.2,<2.0.0',
 'sphinxcontrib-mermaid>=0.7.1,<0.8.0',
 'style>=1.1.6,<2.0.0',
 'testresources>=2.0.1,<3.0.0']

setup_kwargs = {
    'name': 'davt-dependencies-python',
    'version': '202302.0.10',
    'description': 'Data, Analytics and Visualization Templates (DAVT) - Python Dependencies',
    'long_description': '# GIFT/DAVT Project Dependency Documentation\n\n- Point of contact: [John Bowyer](mailto:jcbowyer@hotmail.com)\n- Organizational unit: Pending Public Release\n- Related projects: Pending Public Release\n- Related investments: Pending Public Release\n- Governance status: Pending Public Release\n- Program official: Pending Public Release\n\n',
    'author': 'John Bowyer',
    'author_email': 'zfi4@cdc.gov',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/cdcent/davt',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
