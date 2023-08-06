# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['djangocms_blog_highlight_posts', 'djangocms_blog_highlight_posts.migrations']

package_data = \
{'': ['*'],
 'djangocms_blog_highlight_posts': ['locale/en/LC_MESSAGES/*',
                                    'locale/fr/LC_MESSAGES/*']}

install_requires = \
['Django>=3.2', 'djangocms-blog>=1.2.3']

setup_kwargs = {
    'name': 'djangocms-blog-highlight-posts',
    'version': '0.0.2',
    'description': 'A djangocms-blog extension allowing to highlight posts',
    'long_description': 'A djangocms-blog extension allowing to mark some posts as highlight and sort queryset to display them first on the posts list\n\n----\n\n## Install\n\n* Install the package\n    ```bash\n    python3 -m pip install djangocms-blog-highlight-posts\n    ```\n\n* Add it in your `INSTALLED_APPS`:\n    ```python\n\n        "djangocms_blog_highlight_posts",\n    ```\n\n* Override blog url conf (in project settings):\n    ```python\n\n        BLOG_URLCONF = "djangocms_blog_highlight_posts.urls"\n    ```\n\n* Run the migration:\n    ```sh\n    python3 manage.py migrate djangocms_blog_highlight_posts\n    ```\n\n\n',
    'author': 'KAPT dev team',
    'author_email': 'dev@kapt.mobi',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
