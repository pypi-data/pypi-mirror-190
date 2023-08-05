# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['splatnet3_scraper',
 'splatnet3_scraper.base',
 'splatnet3_scraper.base.tokens',
 'splatnet3_scraper.scraper']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.28.1,<3.0.0']

extras_require = \
{'examples': ['pandas[examples]>=1.5.3,<2.0.0',
              'sqlalchemy[examples]>=2.0.1,<3.0.0',
              'psycopg2[examples]>=2.9.5,<3.0.0'],
 'parquet': ['pyarrow[parquet]>=10.0.1,<11.0.0']}

setup_kwargs = {
    'name': 'splatnet3-scraper',
    'version': '0.4.2',
    'description': 'Scraper for SplatNet 3 for Splatoon 3',
    'long_description': '# SplatNet 3 Scraper\n\n[![Tests Status](./reports/junit/tests-badge.svg?dummy=8484744)](https://htmlpreview.github.io/?https://github.com/cesaregarza/SplatNet3_Scraper/blob/main/reports/junit/report.html) ![Coverage Status](./reports/coverage/coverage-badge.svg?dummy=8484744) ![Flake8 Status](./reports/flake8/flake8-badge.svg?dummy=8484744) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\n**SplatNet 3 Scraper** is a Python library for scraping data from the Splatoon 3 SplatNet 3 API. It is designed to be as lightweight as possible, with minimal dependencies to make it easy to integrate into other projects.\n\n**SplatNet 3 Scraper** started as a fork of **[s3s](https://github.com/frozenpandaman/s3s)**, but has since been rewritten from scratch while incorporating much of the login flow logic of s3s. As a result, I am deeply indebted to the authors of s3s for their work. This project would not have been possible without their efforts.\n\n## Features\n\n* Lightweight and minimal dependencies. Only requires the `requests` library. Requires Python 3.10 or later.\n* The `scraper` module provides a high level API that enables a quick and easy way to get data from the SplatNet 3 API, only requiring the user to provide their session token.\n* The `base` module provides a low level API that allows for more fine-grained control over the scraping process. It is designed to be used by the scraper module, but is designed to be flexible enough to be used by other projects as well.\n* Configuration file support is compatible with the configuration file format used by `s3s`.\n* Responses from the SplatNet 3 API can be saved and loaded from disk, currently supporting the following formats:\n  * JSON\n  * gzip-compressed JSON\n  * csv\n  * parquet (by installing `splatnet3_scraper[parquet]` or the `pyarrow` library)\n\n## Installation\n\n**SplatNet3_Scraper** is currently under active development and is not yet available on PyPI. No wheels are currently available. If you would like to use this early version, you can install it from source by cloning this repository and running `pip install .` in the root directory.\n\n## Usage\n\nThere are two ways to use **SplatNet3_Scraper**. The first is to use the `scraper` module, which provides a high level API that greatly simplifies the process of retrieving data from SplatNet 3. The second is to use the `base` module, which provides a low level API that allows for much more fine-grained control over the scraping process. Either way, both modules require a session token to be provided.\n\n### Using the `scraper` module\n\nThe `scraper` module is a batteries-included module that allows queries to be made to the SplatNet 3 API with minimal effort. It is designed to be used by the end user, and as such it is the easiest and recommended way to get started with **SplatNet3_Scraper**. The `scraper` module provides the `SplatNet3_Scraper` class, which is used to make queries to the SplatNet 3 API. The `SplatNet3_Scraper` class can be instantiated in one of a few ways: by providing a session token, by providing the path to a configuration file, or by loading environment variables.\n\n#### Instantiating the `SplatNet3_Scraper` class by providing a session token\n\n```python\nfrom splatnet3_scraper import SplatNet3_Scraper\nscraper =SplatNet3_Scraper.from_session_token("session_token")\nscraper.query("StageScheduleQuery")\n```\n\n#### Instantiating the `SplatNet3_Scraper` class by providing the path to a configuration file\n\n```python\nfrom splatnet3_scraper import SplatNet3_Scraper\nscraper = SplatNet3_Scraper.from_config_file(".splatnet3_scraper")\nscraper.query("StageScheduleQuery")\n```\n\n#### Instantiating the `SplatNet3_Scraper` class by loading environment variables\n\nThe following environment variables are supported:\n\n* `SN3S_SESSION_TOKEN`\n* `SN3S_GTOKEN`\n* `SN3S_BULLET_TOKEN`\n\n```python\nfrom splatnet3_scraper import SplatNet3_Scraper\nscraper = SplatNet3_Scraper.from_env()\nscraper.query("StageScheduleQuery")\n```\n\n#### Querying the SplatNet 3 API\n\nThe `SplatNet3_Scraper` class provides a `query` method that can be used to make queries to the SplatNet 3 API. The `query` method takes a single argument, which is the name of the query to make. The `query` method returns a `QueryResponse` object, which contains the response data from the SplatNet 3 API. The `QueryResponse` object provides a `data` property that can be used to access the response data. The `QueryResponse` module also supports numpy-style indexing, which can be used to quickly and clearly access specific parts of the response data. For example, the following code will print the game mode name of the the current stage rotation schedule:\n\n```python\nfrom splatnet3_scraper import SplatNet3_Scraper\nscraper = SplatNet3_Scraper.from_env()\nresponse = scraper.query("StageScheduleQuery")\nprint(response["xSchedules", "nodes", 0, "vsRule", "name"])\n```\n\n#### Saving and loading responses\n\nThe `QueryResponse` class provides a `parsed_json` method that can be used to generate a `JSONParser` object from the response data. The `JSONParser` class provides multiple ways of interacting with the given data, including the ability to save the data to disk in a variety of formats. There are currently four different formats that are supported and can be used by passing the desired format to a `to_*` method such as `to_json`. The following formats are supported:\n\n* JSON\n* gzip-compressed JSON\n* csv\n* parquet (by installing `splatnet3_scraper[parquet]` or the `pyarrow` library)\n\nNote: csv and parquet formats work by converting the response data from a nested dictionary to a columnar format. This is not recommended for single queries, but can be useful for interacting with large amounts of data as it deduplicates the JSON structure and allows for more efficient storage and querying.\n\nThe following code will save the response data to a file named `response.json` in the current directory:\n\n```python\nfrom splatnet3_scraper import SplatNet3_Scraper\nscraper = SplatNet3_Scraper.from_env()\nresponse = scraper.query("StageScheduleQuery")\nresponse.parsed_json().to_json("response.json")\n```\n\nAdditionally, the `JSONParser` class provides a `from_*` method that can be used to load data from a file. The following code will load the response data from the file `response.json` in the current directory:\n\n```python\nfrom splatnet3_scraper import JSONParser\nparser = JSONParser.from_json("response.json")\n```\n\n## Symbols\n\n| Symbol | Meaning |\n| ------ | ------- |\n| :white_check_mark: | Implemented |\n| :construction: | In progress |\n| :world_map: | Planned |\n| :x: | Not planned |\n\n## Roadmap\n\n| Feature | Status |\n| ------- | ------ |\n| Support for the SplatNet 3 API | :white_check_mark: |\n| Full support for the SplatNet 3 API | :world_map: |\n| Support for the SplatNet 2 API | :x: |\n| Obtaining session tokens | :white_check_mark: |\n| Full documentation | :world_map: |\n| Full unit test coverage | :white_check_mark: |\n| Columnar data format support | :construction: |\n| CLI interface | :x: |\n| Integration with stats.ink | :x: |\n| PyPI package | :world_map: |\n| Docker image | :world_map: |\n| Executable binary | :x: |\n\n## Docker Note\n\nThis project currently uses the standard library heavily, and as such it is not compatible with the `python:alpine` Docker image. I have no plans to change this. Use the `python:slim` image instead.\n\nSplatNet3_Scraper is licensed under the GPLv3. See the LICENSE file for more details.\n',
    'author': 'Cesar E Garza',
    'author_email': 'cesar@cegarza.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
