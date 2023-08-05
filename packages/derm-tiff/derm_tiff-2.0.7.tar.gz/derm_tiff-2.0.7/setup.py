# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['derm_tiff']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=9.4.0,<10.0.0',
 'nptyping>=2.2.0,<3.0.0',
 'numpy>=1.24.2,<2.0.0',
 'opencv-python>=4.7.0,<5.0.0']

setup_kwargs = {
    'name': 'derm-tiff',
    'version': '2.0.7',
    'description': 'Utilities for tiff images created by DermAnnotation',
    'long_description': '# Designed for DermAnnotation\n\nThis is an utility python package to deal with tiff images\ncreated by [DermAnnotation](https://kondoa9.github.io/DermAnnotation/en/).\n\n## Release Note\n\n- 2.0.0: デフォルトの圧縮方式を`tiff_adobe_deflate`に変更\n\n- 1.0.6: 圧縮方式を`tiff_adobe_deflate`から`tiff_lzw`に変更\n- 1.0.5: パッケージ名をDermAnnoからDermTiffに変更',
    'author': 'kawa-yo',
    'author_email': 'yoshito.kawasaki.pub@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
