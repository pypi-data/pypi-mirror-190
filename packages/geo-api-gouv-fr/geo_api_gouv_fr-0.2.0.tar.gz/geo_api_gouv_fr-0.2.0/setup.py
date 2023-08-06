# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['geo_api_gouv_fr',
 'geo_api_gouv_fr.adress',
 'geo_api_gouv_fr.department',
 'geo_api_gouv_fr.region',
 'geo_api_gouv_fr.tests']

package_data = \
{'': ['*']}

install_requires = \
['pydantic[email]>=1.10.4,<2.0.0', 'requests>=2.28.2,<3.0.0']

setup_kwargs = {
    'name': 'geo-api-gouv-fr',
    'version': '0.2.0',
    'description': 'Python package to use geoapi.gouv.fr api',
    'long_description': '# GeoApi for data.gouv - Python Package\n\n## About\n\nThis package was intended to use the [geo.api.gouv.fr](https://geo.api.gouv.fr/) api.\n## How tos\n\n### Tests\n\n``` bash\nmake test\n```\n\n### Documentation\n\nThe documentation is based on [mkdocs](https://www.mkdocs.org/)\n\nTo open the docs:\n\n``` bash\nmake help\n```\n\nIt will be accessible [here](http://127.0.0.1:9999/)\n',
    'author': 'La Bonne Boite',
    'author_email': 'labonneboite@pole-emploi.fr',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/StartupsPoleEmploi/geo-api-gouv-fr',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
