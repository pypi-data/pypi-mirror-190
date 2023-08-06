# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['scicamera', 'scicamera.previews']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.23.5,<2.0.0', 'pillow>=9.3.0,<10.0.0']

setup_kwargs = {
    'name': 'scicamera',
    'version': '0.1.0.post1',
    'description': '',
    'long_description': '# scicamera\n\n---\nThis is a drastic refactor of _picamera2_ to a much smaller footprint and\nfeature set that emphasises consistant, reliable, imaging performance. \nAdditonally, we use modern dev practices, established tools for test/lint.\n\n## Installation\n\n_scicamera_ is predominantly supported on Raspberry Pi OS Bullseye (or later) images, both 32 and 64-bit. Limited support is available on Ubuntu and other\ndebian flavors, but will require `libcamera` to be built with the python\npackage enabled.\n\n\n## Contributing\n\nOpen a PR, discuss the changes. Our goals are performance, brevity, maintainability, and reliability. \n\nFeature creep is not of interest, but we would be happy\nto help you build your more complicated project on top of this.\n\nIf we like them, and the tests pass we will merge them. \nCI requires code has been processed `isort` and `black` toolchains.\n\nDoing this is pretty easy:\n```\nisort .\nblack .\n```\n\nGreat work.\n\n## Publishing to PYPI\n\nShould be added to github action later\n\n1. Add your pypi token\n  ```sh\n  $ poetry config pypi-token.pypi my-token\n  ```\n\n2. Cut a new tag\n    ```sh\n    $ git tag -a v0.1.0 -m "Version 0.1.0"\n    $ git push origin v0.1.0\n    ```\n\n3. Publish\n  ```sh\n  $ poetry publish --build\n  ```\n',
    'author': 'Exclosure',
    'author_email': 'info@exclosure.io',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
