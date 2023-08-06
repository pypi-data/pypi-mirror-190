# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jefferson', 'jefferson.compression', 'jefferson.core']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0', 'cstruct>=5.2,<6.0', 'python-lzo>=1.14,<2.0']

entry_points = \
{'console_scripts': ['jefferson = jefferson.cli:main']}

setup_kwargs = {
    'name': 'jefferson',
    'version': '0.4.2',
    'description': 'JFFS2 filesystem extraction tool.',
    'long_description': '## Jefferson\n\nJFFS2 filesystem extraction tool\n\n### Installation\n\nFollow these steps on Debian based systems (Debian, Ubuntu, Kali, ...) to perform a system-wide installation of jefferon:\n\n```bash\ngit clone https://github.com/sviehb/jefferson.git\ncd jefferson\nsudo apt update\nsudo apt install python3-pip liblzo2-dev\nsudo python3 -m pip install -r requirements.txt\nsudo python3 setup.py install\n```\n\n\n### Features\n\n- big-endian and little-endian support with auto-detection\n- zlib, rtime, LZMA, and LZO compression support\n- CRC checks - for now only enforced on `hdr_crc`\n- extraction of symlinks, directories, files, and device nodes\n- detection/handling of duplicate inode numbers. Occurs if multiple JFFS2 filesystems are found in one file and causes `jefferson` to treat segments as separate filesystems\n\n### Usage\n\n```bash\n$ jefferson filesystem.img -d outdir\n```\n',
    'author': 'ONEKEY',
    'author_email': 'support@onekey.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
