# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['theine']

package_data = \
{'': ['*']}

install_requires = \
['theine-core>=0.1.3,<0.2.0', 'typing-extensions>=4.4.0,<5.0.0']

setup_kwargs = {
    'name': 'theine',
    'version': '0.1.1',
    'description': 'high performance in-memory cache',
    'long_description': '# theine\nhigh performance in-memory cache\n\n## Requirements\nPython 3.7+\n\n## Installation\n```\npip install theine\n```\n\n## API\n\n```Python\nfrom theine import Cache\nfrom datetime import timedelta\n\ncache = Cache("tlfu", 10000)\n# without default, return None on miss\nv = cache.get("key")\n\n# with default, return default on miss\nsentinel = object()\nv = cache.get(key, sentinel)\n\n# set with ttl\ncache.set("key", {"foo": "bar"}, timedelta(seconds=100))\n\n# delete from cache\ncache.delete("key")\n```\n',
    'author': 'Yiling-J',
    'author_email': 'njjyl723@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
