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
    'version': '0.1.1.dev1',
    'description': '',
    'long_description': '# scicamera\n\n---\nThis is a drastic refactor of _picamera2_ to a much smaller footprint and\nfeature set that emphasises consistant and reliable imaging performance. \n\n_scicamera_ is predominantly supported on:\n- Raspberry Pi OS Bullseye (or later) images 64-bit.\n- x86 Ubuntu (likely other debian flavors as well)\n\n**Our goals are performance, reliability, brevity, and maintainability.**\n\n## Installation\n\n_scicamera_ is a pure python package, but relies on the python\nc++ wrapper of _libcamera_.\n\n_scicamera_ can be installed simply with:\n```\npip install scicamera\n```\n### Installing libcamera + python bindings\n\nImport and use of the above pacakge requires that `libcamera` to be built\nwith the python package enabled. On rasbian, this is accomplished by \ninstalling the `libcamera` package from apt. In x86 it must be built \nusing something like the following:\n\n```bash\ngit clone https://github.com/Exclosure/libcamera.git\ncd libcamera\ngit checkout v0.0.4\nmeson setup build -D pycamera=enabled\nninja -C build\nsudo ninja -C build install\n```\n\n## Bugs/Contributing\n\n\nOpen an issue/PR to discuss your bug or feature. Once a course of action\nhas been identified, open a PR, discuss the changes. \n\nFeature creep is not of interest, but we would be happy\nto help you build your more complicated project on top of this.\n\nIf we like them, and the tests pass we will merge them. \nCI requires code has been processed `isort` and `black` toolchains.\n\nDoing this is pretty easy:\n```\nisort .\nblack .\n```\n\nGreat work.\n\n## Publishing to PYPI\n\nShould be added to github action later\n\n1. Add your pypi token\n  ```sh\n  $ poetry config pypi-token.pypi my-token\n  ```\n\n2. Cut a new tag\n  ```sh\n  $ git tag -a v0.1.0 -m "Version 0.1.0"\n  $ git push origin v0.1.0\n  ```\n\n3. Publish\n  ```sh\n  $ poetry publish --build\n  ```\n',
    'author': 'Exclosure',
    'author_email': 'info@exclosure.io',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/exclosure/scicamera',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
