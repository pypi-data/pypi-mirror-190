# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['meilisearch_python_async', 'meilisearch_python_async.models']

package_data = \
{'': ['*']}

install_requires = \
['PyJWT>=2.3.0',
 'aiofiles>=0.7',
 'camel-converter>=1.0.0',
 'httpx>=0.17',
 'pydantic>=1.8']

setup_kwargs = {
    'name': 'meilisearch-python-async',
    'version': '1.0.0',
    'description': 'A Python async client for the Meilisearch API',
    'long_description': '# Meilisearch Python Async\n\n[![Tests Status](https://github.com/sanders41/meilisearch-python-async/workflows/Testing/badge.svg?branch=main&event=push)](https://github.com/sanders41/meilisearch-python-async/actions?query=workflow%3ATesting+branch%3Amain+event%3Apush)\n[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/sanders41/meilisearch-python-async/main.svg)](https://results.pre-commit.ci/latest/github/sanders41/meilisearch-python-async/main)\n[![Coverage](https://codecov.io/github/sanders41/meilisearch-python-async/coverage.svg?branch=main)](https://codecov.io/gh/sanders41/meilisearch-python-async)\n[![PyPI version](https://badge.fury.io/py/meilisearch-python-async.svg)](https://badge.fury.io/py/meilisearch-python-async)\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/meilisearch-python-async?color=5cc141)](https://github.com/sanders41/meilisearch-python-async)\n\nMeilisearch Python Async is a Python async client for the [Meilisearch](https://github.com/meilisearch/meilisearch) API. Meilisearch also has an official [Python client](https://github.com/meilisearch/meilisearch-python).\n\nWhich of the two clients to use comes down to your particular use case. The purpose for this async client is to allow for non-blocking calls when working in async frameworks such as [FastAPI](https://fastapi.tiangolo.com/), or if your own code base you are working in is async. If this does not match your use case then the official client will be a better choice.\n\n## Installation\n\nUsing a virtual environmnet is recommended for installing this package. Once the virtual environment is created and activated install the package with:\n\n```sh\npip install meilisearch-python-async\n```\n\n## Run Meilisearch\n\nThere are several ways to [run Meilisearch](https://docs.meilisearch.com/reference/features/installation.html#download-and-launch).\nPick the one that works best for your use case and then start the server.\n\nAs as example to use Docker:\n\n```sh\ndocker pull getmeili/meilisearch:latest\ndocker run -it --rm -p 7700:7700 getmeili/meilisearch:latest ./meilisearch --master-key=masterKey\n```\n\n## Useage\n\n### Add Documents\n\n- Note: `client.index("books") creates an instance of an Index object but does not make a network call to send the data yet so it does not need to be awaited.\n\n```py\nfrom meilisearch_python_async import Client\n\nasync with Client(\'http://127.0.0.1:7700\', \'masterKey\') as client:\n    index = client.index("books")\n\n    documents = [\n        {"id": 1, "title": "Ready Player One"},\n        {"id": 42, "title": "The Hitchhiker\'s Guide to the Galaxy"},\n    ]\n\n    await index.add_documents(documents)\n```\n\nThe server will return an update id that can be used to [get the status](https://docs.meilisearch.com/reference/api/updates.html#get-an-update-status)\nof the updates. To do this you would save the result response from adding the documets to a variable,\nthis will be a UpdateId object, and use it to check the status of the updates.\n\n```py\nupdate = await index.add_documents(documents)\nstatus = await client.index(\'books\').get_update_status(update.update_id)\n```\n\n### Basic Searching\n\n```py\nsearch_result = await index.search("ready player")\n```\n\n### Base Search Results: SearchResults object with values\n\n```py\nSearchResults(\n    hits = [\n        {\n            "id": 1,\n            "title": "Ready Player One",\n        },\n    ],\n    offset = 0,\n    limit = 20,\n    nb_hits = 1,\n    exhaustive_nb_hits = bool,\n    facets_distributionn = None,\n    processing_time_ms = 1,\n    query = "ready player",\n)\n```\n\n### Custom Search\n\nInformation about the parameters can be found in the [search parameters](https://docs.meilisearch.com/reference/features/search_parameters.html) section of the documentation.\n\n```py\nindex.search(\n    "guide",\n    attributes_to_highlight=["title"],\n    filters="book_id > 10"\n)\n```\n\n### Custom Search Results: SearchResults object with values\n\n```py\nSearchResults(\n    hits = [\n        {\n            "id": 42,\n            "title": "The Hitchhiker\'s Guide to the Galaxy",\n            "_formatted": {\n                "id": 42,\n                "title": "The Hitchhiker\'s Guide to the <em>Galaxy</em>"\n            }\n        },\n    ],\n    offset = 0,\n    limit = 20,\n    nb_hits = 1,\n    exhaustive_nb_hits = bool,\n    facets_distributionn = None,\n    processing_time_ms = 5,\n    query = "galaxy",\n)\n```\n\n## Documentation\n\nSee our [docs](https://meilisearch-python-async.paulsanders.dev) for the full documentation.\n\n## Contributing\n\nContributions to this project are welcome. If you are interesting in contributing please see our [contributing guide](CONTRIBUTING.md)\n',
    'author': 'Paul Sanders',
    'author_email': 'psanders1@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/sanders41/meilisearch-python-async',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
