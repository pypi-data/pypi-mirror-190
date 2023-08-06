# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pywarsaw']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp-client-cache>=0.8.1,<0.9.0',
 'aiohttp>=3.8.3,<4.0.0',
 'aiosqlite>=0.18.0,<0.19.0',
 'attrs>=22.2.0,<23.0.0']

setup_kwargs = {
    'name': 'pywarsaw',
    'version': '0.1.0',
    'description': 'An unofficial asynchronous API wrapper for Warsaw Open Data - https://api.um.warszawa.pl/',
    'long_description': '# pywarsaw\n![actions](https://github.com/BrozenSenpai/pywarsaw/actions/workflows/python-package.yml/badge.svg)[![Project Status: WIP – Initial development is in progress, but there has not yet been a stable, usable release suitable for the public.](https://www.repostatus.org/badges/latest/wip.svg)](https://www.repostatus.org/#wip)\n\nAn unofficial asynchronous API wrapper for [Warsaw Open Data](https://api.um.warszawa.pl/).\n\nCreated mainly for learning purposes.\n\nPackage is still in progress, check the work status in the *currently covered* section.\n\n## Features\n- **Asynchronous**: designed to work with asyncio\n- **Extensive**: cover as many endpoints as possible\n- **Approachable**: all polish fields translated to english\n- **Responsible**: minimize the load on the API server\n    - implemented caching\n- **Simple**: easy to use and customize:\n    - object-oriented design\n    - use of data transfer objects\n    - type hinting\n    - convert adequate fields from strings to the more suitable types\n- **Lightweight**: minimal usage of the third-party packages\n\n## Installation\n```\npip install pywarsaw\n```\n\n## Getting started\nThe package goal is to be straightforward to use. For example, you can obtain a list of objects with information about current air quality in Warsaw, with caching enabled like this:\n```python\nimport asyncio\nimport pywarsaw\n\nasync def main():\n    client = pywarsaw.Mermaid(api_key="YOUR_API_KEY")\n    await client.cache_enable()\n\n    result = await client.get_air_quality()\n    \n    await client.close()\n\nasyncio.run(main())\n```\nOr with the context manager:\n```python\nasync with pywarsaw.Mermaid(api_key="YOUR_API_KEY") as client:\n    await client.cache_enable()\n    \n    result = await client.get_air_quality()\n```\nCaching can be disabled with:\n```python\nawait client.cache_disable()\n```\nEvery object from the obtained list an be converted to the simpler structures:\n```python\n# convert object to the dictionary\nresult_dict = result[0].to_dict()\n\n# convert object to the tuple\nresult_tuple = result[0].to_tuple()\n\n# convert object to the flat dict - useful for creating Pandas dataframes\nresult_flat = result[0].to_flat_dict()\n\n# convert object to the json string\nresult_json = result[0].to_json()\n```\n\n## Currently covered\nWarsaw Open Data has a lot of different endpoints and data categories to cover.\n\nThe current status of work is:\n\n**Culture**\n* culture (vector maps):\n    * theathers :heavy_check_mark:\n\n**Public transport**\n* ZTM timetables:\n    * stops :heavy_check_mark:\n    * lines :heavy_check_mark:\n    * timetables :heavy_check_mark:\n* transport (vector maps):\n    * cycle stations :heavy_check_mark:\n    * cycle tracks :heavy_check_mark:\n    * parking lots :heavy_check_mark:\n    * subway entrances :heavy_check_mark:\n* stops information:\n    * coordinates :heavy_check_mark:\n    * current day coordinates :heavy_check_mark:\n\n**Education**\n* computers and internet access:\n    * internet access :heavy_check_mark:\n    * computers purpose :heavy_check_mark:\n* statics about schools :x:\n* education - rooms :x:\n* schools :x:\n\n**Ecology**\n* shrubs:\n    * shrubs :heavy_check_mark:\n    * groups of shrubs :heavy_check_mark:\n* forests:\n    * forests :heavy_check_mark:\n* trees:\n    * groups of trees :heavy_check_mark:\n    * trees :heavy_check_mark:\n* munincipal waste:\n    * waste segregation :heavy_check_mark:\n* air quality:\n    * air quality :heavy_check_mark:\n\n**Online data**\n* trams and buses:\n    * trams and buses :heavy_check_mark:\n* queuing systems :x:\n* road works :x:\n\n**Spatial data**\n* ATMs :x:\n* names of urban objects :x:\n* health :x:\n* bikes :x:\n* sport :x:\n* accommodation :x:\n\n**Safety**\n* defibrillators:\n    * defibrillators :heavy_check_mark:\n* safety (vector maps) :x:\n\n**Official data**\n* administration (vector maps) :x:\n* 19115 :x:\n* sport :x:\n* events :x:\n\n## Terms of data usage\nTranslated from [here](https://api.um.warszawa.pl/#).\n\nPublic data available on the service are official materials and as such are not protected by copyright law. You may use this data freely but must comply with the conditions for reusing public information outlined in the law on the reuse of public sector information of 25th February 2016.\n\nWhen using public information made available on the Open Data After Warsaw service, you must:\n* Include information about the source of the data, including the name: Capital City of Warsaw, and the URL of the Open Data After Warsaw service: http://api.um.warszawa.pl (if possible)\n* Provide the date of creation and acquisition of public information\n\nReusing public sector information available on the service is done at your own risk. The Capital City of Warsaw assumes no responsibility for any damage resulting from your or other users\' reuse of this information. Some of the information processed by third parties that you may reuse may be outdated or contain errors, and the Capital City of Warsaw reserves the right to this possibility.\n\n## Documentation\nThe documentation is hosted on [ReadTheDocs.io](https://pywarsaw.readthedocs.io/en/latest/)\n\n## Help, questions, and contributing\nAll contributors are very welcome. If you have any questions or a bug to report feel free to open an issue.\n\n## External packages\nPywarsaw depends on these third-party packages:\n\n\n* [attrs](https://www.attrs.org/en/stable/)\n* [aiohttp](https://docs.aiohttp.org/en/stable/)\n* [aiohttp-client-cache](https://pypi.org/project/aiohttp-client-cache/)\n* [aiosqlite](https://github.com/omnilib/aiosqlite)',
    'author': 'brozen',
    'author_email': 'szymon.mazurkievicz@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/BrozenSenpai/pywarsaw',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
