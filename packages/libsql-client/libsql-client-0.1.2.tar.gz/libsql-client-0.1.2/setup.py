# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['libsql_client']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.0,<4.0']

setup_kwargs = {
    'name': 'libsql-client',
    'version': '0.1.2',
    'description': 'sqld client for Python',
    'long_description': '# sqld client for Python\n\nThis is a Python client for [sqld][sqld], the server mode for [libSQL][libsql].\n\n[sqld]: https://github.com/libsql/sqld\n[libsql]: https://libsql.org/\n\n## Getting started\n\nTo get started, you need [`sqld` running somewhere][sqld]. Then you can install this package with:\n\n```\n$ pip install libsql-client\n```\n\nand use it like this:\n\n```python\nimport asyncio\nimport libsql_client\n\nasync def main():\n    url = "http://localhost:8080"\n    async with libsql_client.Client(url) as client:\n        result_set = await client.execute("SELECT * from users")\n        print(len(result_set.rows), "rows")\n        for row in result_set.rows:\n            print(row)\n\nasyncio.run(main())\n```\n\nYou can also connect to a local SQLite database simply by changing the URL:\n\n```python\nurl = "file:example.db"\n```\n\n## Contributing to this package\n\nFirst, please install Python and [Poetry][poetry]. To install all dependencies for local development to a\nvirtual environment, run:\n\n[poetry]: https://python-poetry.org/\n\n```\npoetry install -G dev\n```\n\nTo run the tests, use:\n\n```\npoetry run pytest\n```\n\nTo check types with MyPy, use:\n\n```\npoetry run mypy\n```\n',
    'author': 'Jan Špaček',
    'author_email': 'honza@chiselstrike.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
