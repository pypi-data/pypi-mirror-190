# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nnext',
 'nnext.conversions',
 'nnext.grpc',
 'nnext.http',
 'nnext.http.api',
 'nnext.http.models',
 'nnext.uploader']

package_data = \
{'': ['*']}

install_requires = \
['betterproto==2.0.0b4',
 'grpcio>=1.46.0,<2.0.0',
 'httpx[http2]>=0.23.0,<0.24.0',
 'loguru>=0.5.3,<0.6.0',
 'nest-asyncio>=1.5.5,<2.0.0',
 'numpy>=1.21,<2.0',
 'pydantic>=1.8,<2.0',
 'tqdm>=4.56.0,<5.0.0',
 'typing-extensions>=4.0.0,<5.0.0']

setup_kwargs = {
    'name': 'nnext',
    'version': '0.0.42',
    'description': 'Client library for the NNext Neural search engine',
    'long_description': '# <a href="https://nnext.ai/"><img src="https://d3g1vr8yw3euzd.cloudfront.net/nnext-ultra-wide-tingle.png" alt="NNext Python Client"></a>\n\n## About\n\nThe NNext Python Client.\n\nNNext is a\n\n* ⚡ blazingly fast\n* 🔍 nearest-neighbors vector search engine\n\n<a href="https://twitter.com/intent/follow?screen_name=nnextai"><img src="https://img.shields.io/badge/Follow-nnextai-blue.svg?style=flat&logo=twitter"></a>\n\n[Installation](#installation) |  [Quick Start](#quick-start) | [Documentation](#documentation)\n\n## Installation\n\nTo install the pynnext client, activate a virtual environment, and install via pip:\n\n```zsh\npip install nnext\n```\n\n## Quick Start\n\nHere\'s a quick example showcasing how you can create an index, insert vectors/documents and search among them via NNext.\n\nLet\'s begin by installing the NNext server.\n\n```zsh\nnnclient = nnext.NNextClient(api_key="NNEXT_API_KEY")\n```\n\n## Documentation\n\nMore documentation is available here:\n\n<a href="https://nnext.ai/docs" target="_blank" rel="noopener noreferrer"><img src="https://d3g1vr8yw3euzd.cloudfront.net/3.png" height="100"></a>\n',
    'author': 'NNext Team',
    'author_email': 'team@nnext.ai',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://nnext.io/docs/Python-22a9be22c5cf4869bda849e3f06c0993',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
