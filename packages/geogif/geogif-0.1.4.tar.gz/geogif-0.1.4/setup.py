# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['geogif']

package_data = \
{'': ['*'],
 'geogif': ['.hypothesis/unicode_data/13.0.0/*',
            '.pytest_cache/*',
            '.pytest_cache/v/cache/*']}

install_requires = \
['Pillow>=9.0.1,<10.0.0',
 'dask[delayed]>=2021.4.1',
 'matplotlib>=3.4.1,<4.0.0',
 'numpy>=1.20.2,<2.0.0',
 'xarray>=0.18']

setup_kwargs = {
    'name': 'geogif',
    'version': '0.1.4',
    'description': 'Render xarray timestacks into GIFs',
    'long_description': '# GeoGIF\n[![Documentation Status](https://readthedocs.org/projects/geogif/badge/?version=latest)](https://geogif.readthedocs.io/en/latest/?badge=latest)\n\n\nMake GIFs from time-stacked `xarray.DataArray`s (`time`, [optional `band`], `y`, `x`), dead-simple.\n\n```python\nfrom geogif import gif, dgif\ngif(data_array)\ndgif(dask_data_array).compute()\n```\n\n![Animation of shoreline moving on the coast of Cape Cod](docs/capecod.gif)\n\nThe "geo" part is a lie, actually. The arrays don\'t have to be geospatial in nature. But I called it GeoGIF because:\n\n1. Wanting to animate a time-stack of imagery (like you\'d get from [stackstac](https://stackstac.readthedocs.io/)) is a common task in the earth-observation/geospatial world.\n1. I think `GeoGIF` is a hilarious idea<sup>[1](#geotiff)</sup>.\n\n\n<a name="geotiff">1</a>: To ruin the joke, it sounds like GeoTIFF, a ubiquitous geospatial image format. If you also think this is a funny idea, and believe you\'d have a better use for the name than I do, I\'d happily cede it to you.\n\n## Installation\n\n```bash\npip install geogif\n```\n\n## Documentation\n\nSee https://geogif.readthedocs.io/en/latest/.\n\n## Development\n\nGeoGIF is managed by [Poetry](https://python-poetry.org/), so be sure that\'s installed first. To develop locally, first fork or clone the repo. Then, to set up a virtual environment and install the necessary dependencies:\n\n```bash\ncd geogif\npoetry install\n```\n\n### Running Tests\n\nGeoGIF has some basic end-to-end tests, written with [Hypothesis](https://hypothesis.readthedocs.io/en/latest/index.html). To run:\n\n```bash\npytest\n```\n\nThis will take ~30 seconds (longer the first time), as Hypothesis generates fake data to root out possible errors.\n\n### Code style\n\nGeoGIF is formatted with [shed](https://github.com/Zac-HD/shed), in order to allow for as few opinions as possible.\n',
    'author': 'Gabe Joseph',
    'author_email': 'gjoseph92@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://geogif.readthedocs.io/en/latest/index.html',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
