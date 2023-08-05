# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mure']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp[speedups]>=3.8.3,<4.0.0', 'orjson>=3.8.5,<4.0.0']

setup_kwargs = {
    'name': 'mure',
    'version': '0.4.0',
    'description': 'Perform multiple HTTP requests in parallel – without writing boilerplate code or worrying about async functions.',
    'long_description': '# mure\n\n[![downloads](https://static.pepy.tech/personalized-badge/mure?period=total&units=international_system&left_color=black&right_color=black&left_text=downloads)](https://pepy.tech/project/mure)\n[![downloads/month](https://static.pepy.tech/personalized-badge/mure?period=month&units=abbreviation&left_color=black&right_color=black&left_text=downloads/month)](https://pepy.tech/project/mure)\n[![downloads/week](https://static.pepy.tech/personalized-badge/mure?period=week&units=abbreviation&left_color=black&right_color=black&left_text=downloads/week)](https://pepy.tech/project/mure)\n\nThis is a thin layer on top of [`aiohttp`](https://docs.aiohttp.org/en/stable/) to perform multiple HTTP requests in parallel – without writing boilerplate code or worrying about `async` functions.\n\n> `mure` means **mu**ltiple **re**quests, but is also the German term for a form of mass wasting involving fast-moving flow of debris and dirt that has become liquified by the addition of water.\n\nInstall the latest stable version from [PyPI](https://pypi.org/project/mure):\n\n```\npip install mure\n```\n\n## Usage\n\nPass an iterable of dictionaries with at least a value for `url` and get `ResponseIterator` with the responses:\n\n```python\n>>> import mure\n>>> resources = [\n...     {"url": "https://httpbin.org/get"},\n...     {"url": "https://httpbin.org/get", "params": {"foo": "bar"}},\n...     {"url": "invalid"},\n... ]\n>>> responses = mure.get(resources, batch_size=2)\n>>> responses\n<ResponseIterator: 3 pending>\n>>> for resource, response in zip(resources, responses):\n...     print(resource, "status code:", response.status)\n...\n{\'url\': \'https://httpbin.org/get\'} status code: 200\n{\'url\': \'https://httpbin.org/get\', \'params\': {\'foo\': \'bar\'}} status code: 200\n{\'url\': \'invalid\'} status code: 0\n```\n\nThe keyword argument `batch_size` defines the number of requests to perform in parallel (don\'t be too greedy).\n\nThere is also a convenience function for POST requests:\n\n```python\n>>> resources = [\n...     {"url": "https://httpbin.org/post"},\n...     {"url": "https://httpbin.org/post", "json": {"foo": "bar"}},\n...     {"url": "invalid"},\n... ]\n>>> responses = mure.post(resources)\n```\n\nYou can even mix HTTP methods in the list of resources (but have to specify the method for each resource):\n\n```python\n>>> resources = [\n...     {"method": "GET", "url": "https://httpbin.org/get"},\n...     {"method": "GET", "url": "https://httpbin.org/get", "params": {"foo": "bar"}},\n...     {"method": "POST", "url": "https://httpbin.org/post"},\n...     {"method": "POST", "url": "https://httpbin.org/post", "json": {"foo": "bar"}},\n...     {"method": "GET", "url": "invalid"},\n... ]\n>>> responses = mure.request(resources)\n```\n',
    'author': 'Severin Simmler',
    'author_email': 's.simmler@snapaddy.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
