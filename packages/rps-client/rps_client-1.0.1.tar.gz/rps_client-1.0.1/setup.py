# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rps_client']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'rps-client',
    'version': '1.0.1',
    'description': 'CUBETIQ RPS Client SDK for Python',
    'long_description': "# RPS Client SDK Python\n\n-   [x] RPS Webhook\n-   [ ] RPS WebSocket\n-   [ ] RPS SendFile\n\n### Install via `pip`\n\n```shell\npip install rps_client\n```\n\n### Usages\n\n```python\nfrom rps_client.models import RpsClientOptions, RpsHookRequest\nfrom rps_client.sdk import RpsClient\n\nAPI_KEY = 'YOUR_API_KEY'\nDATA = RpsHookRequest(\n    data={\n        'mytext': 'my world is here',\n        'bool': True,\n    },\n    type='test',\n    details={\n        'name': 'Hello World',\n        'number': 1000,\n    }\n)\n\nsdk = RpsClient(RpsClientOptions.builder().api_key(TEST_API_KEY).build())\nreponse = sdk.send(DATA)\nprint(response.data)\n```\n\n### Build, Install, and Test from Source\n\n```shell\nmake\n```\n\n### Build and Install from Source\n\n```shell\nmake build install\n```\n\n### Run test\n\n```shell\nmake test\n```\n\n### Publish\n\n-   Set Token\n\n```shell\npoetry config pypi-token.pypi my-token\n```\n\n-   Publish\n\n```shell\nmake publish\n```\n\n### Contributors\n\n-   Sambo Chea <sombochea@cubetiqs.com>\n",
    'author': 'Sambo Chea',
    'author_email': 'sombochea@cubetiqs.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
