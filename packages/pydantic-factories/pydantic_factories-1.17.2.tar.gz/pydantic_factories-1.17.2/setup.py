# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pydantic_factories',
 'pydantic_factories.constraints',
 'pydantic_factories.extensions',
 'pydantic_factories.plugins',
 'pydantic_factories.value_generators']

package_data = \
{'': ['*']}

install_requires = \
['faker', 'pydantic>=1.10.0', 'typing-extensions']

setup_kwargs = {
    'name': 'pydantic-factories',
    'version': '1.17.2',
    'description': 'Mock data generation for pydantic based models and python dataclasses',
    'long_description': '<!-- markdownlint-disable -->\n<p align="center">\n  <img src="https://github.com/starlite-api/branding/blob/9ab099a2089219c07727baaa29f67e9474ff93c8/assets/Starlite%20Branding%20-%20SVG%20-%20Transparent/Logo%20-%20Banner%20-%20Inline%20-%20Light.svg#gh-light-mode-only" alt="Starlite Logo - Light" width="100%" height="auto" />\n  <img src="https://github.com/starlite-api/branding/blob/9ab099a2089219c07727baaa29f67e9474ff93c8/assets/Starlite%20Branding%20-%20SVG%20-%20Transparent/Logo%20-%20Banner%20-%20Inline%20-%20Dark.svg#gh-dark-mode-only" alt="Starlite Logo - Dark" width="100%" height="auto" />\n</p>\n<!-- markdownlint-restore -->\n\n<!-- markdownlint-disable -->\n<div align="center">\n\n![PyPI - License](https://img.shields.io/pypi/l/pydantic-factories?color=blue)\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pydantic-factories)\n\n[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=starlite-api_pydantic-factories&metric=coverage)](https://sonarcloud.io/summary/new_code?id=starlite-api_pydantic-factories)\n[![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=starlite-api_pydantic-factories&metric=sqale_rating)](https://sonarcloud.io/summary/new_code?id=starlite-api_pydantic-factories)\n[![Reliability Rating](https://sonarcloud.io/api/project_badges/measure?project=starlite-api_pydantic-factories&metric=reliability_rating)](https://sonarcloud.io/summary/new_code?id=starlite-api_pydantic-factories)\n[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=starlite-api_pydantic-factories&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=starlite-api_pydantic-factories)\n\n[![Discord](https://img.shields.io/discord/919193495116337154?color=202235&label=%20Discord&logo=discord)](https://discord.gg/X3FJqy8d2j) [![Matrix](https://img.shields.io/badge/%5Bm%5D%20Matrix-bridged-blue?color=202235)](https://matrix.to/#/#starlitespace:matrix.org) [![Reddit](https://img.shields.io/reddit/subreddit-subscribers/starlite?label=r%2FStarlite&logo=reddit)](https://reddit.com/r/starlite)\n\n</div>\n<!-- markdownlint-restore -->\n\n# Pydantic-Factories\n\nThis library offers powerful mock data generation capabilities for [pydantic](https://github.com/samuelcolvin/pydantic)\nbased models, `dataclasses` and `TypeDict`s. It can also be used with other libraries that use pydantic as a foundation.\n\nCheck out [the documentation 📚](https://starlite-api.github.io/pydantic-factories/).\n\n## Installation\n\n```shell\npip install pydantic-factories\n```\n\n## Example\n\n```python\nfrom datetime import date, datetime\nfrom typing import List, Union\n\nfrom pydantic import BaseModel, UUID4\n\nfrom pydantic_factories import ModelFactory\n\n\nclass Person(BaseModel):\n    id: UUID4\n    name: str\n    hobbies: List[str]\n    age: Union[float, int]\n    birthday: Union[datetime, date]\n\n\nclass PersonFactory(ModelFactory):\n    __model__ = Person\n\n\nresult = PersonFactory.build()\n```\n\nThat\'s it - with almost no work, we are able to create a mock data object fitting the `Person` class model definition.\n\nThis is possible because of the typing information available on the pydantic model and model-fields, which are used as a\nsource of truth for data generation.\n\nThe factory parses the information stored in the pydantic model and generates a dictionary of kwargs that are passed to\nthe `Person` class\' init method.\n\n## Features\n\n- ✅ supports both built-in and pydantic types\n- ✅ supports pydantic field constraints\n- ✅ supports complex field types\n- ✅ supports custom model fields\n- ✅ supports dataclasses\n- ✅ supports TypedDicts\n\n## Why This Library?\n\n- 💯 powerful\n- 💯 extensible\n- 💯 simple\n- 💯 rigorously tested\n\n## Contributing\n\nThis library is open to contributions - in fact we welcome it. [Please see the contribution guide!](CONTRIBUTING.md)\n',
    'author': "Na'aman Hirschfeld",
    'author_email': 'nhirschfeld@gmail.com',
    'maintainer': "Na'aman Hirschfeld",
    'maintainer_email': 'nhirschfeld@gmail.com',
    'url': 'https://github.com/starlite-api/pydantic-factories',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
