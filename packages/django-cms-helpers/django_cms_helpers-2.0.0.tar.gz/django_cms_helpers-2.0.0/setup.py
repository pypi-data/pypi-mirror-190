# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cms_helpers', 'cms_helpers.templatetags']

package_data = \
{'': ['*']}

install_requires = \
['Django>=3.2', 'django-cms>=3.9']

extras_require = \
{'docs': ['Sphinx>=5.1', 'django-anylink>=2.0', 'django-filer>=2.2']}

setup_kwargs = {
    'name': 'django-cms-helpers',
    'version': '2.0.0',
    'description': 'django-cms-helpers is a collection of helpers when working with django-cms.',
    'long_description': "django-cms-helpers\n==================\n\n.. image:: https://img.shields.io/pypi/v/django-cms-helpers.svg\n   :target: https://pypi.org/project/django-cms-helpers/\n   :alt: Latest Version\n\n.. image:: https://github.com/stephrdev/django-cms-helpers/workflows/Test/badge.svg?branch=master\n   :target: https://github.com/stephrdev/django-cms-helpers/actions?workflow=Test\n   :alt: CI Status\n\n.. image:: https://codecov.io/gh/stephrdev/django-cms-helpers/branch/master/graph/badge.svg\n   :target: https://codecov.io/gh/stephrdev/django-cms-helpers\n   :alt: Coverage Status\n\n.. image:: https://readthedocs.org/projects/django-cms-helpers/badge/?version=latest\n   :target: https://django-cms-helpers.readthedocs.io/en/stable/?badge=latest\n   :alt: Documentation Status\n\n\ndjango-cms-helpers is a collection of helpers when working with django-cms.\n\n\nFeatures\n--------\n\n* templatetag for getting title extension object.\n* anylink extension for cms pages.\n* boilerplate code for ExtensionToolbar.\n* FilerFileField extension to validate file extension and make default_alt_text required.\n\nRequirements\n------------\n\ndjango-cms-helpers supports Python 3 only and requires at least Django 3.2 and django-cms 3.9.\n\n\nPrepare for development\n-----------------------\n\nA Python 3.8+ interpreter is required in addition to poetry.\n\n.. code-block:: shell\n\n    $ poetry install\n\n\nNow you're ready to run the tests:\n\n.. code-block:: shell\n\n    $ poetry run py.test\n\n\nResources\n---------\n\n* `Documentation <https://django-cms-helpers.readthedocs.io>`_\n* `Bug Tracker <https://github.com/stephrdev/django-cms-helpers/issues>`_\n* `Code <https://github.com/stephrdev/django-cms-helpers/>`_\n",
    'author': 'Stephan Jaekel',
    'author_email': 'steph@rdev.info',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/stephrdev/django-cms-helpers',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4',
}


setup(**setup_kwargs)
