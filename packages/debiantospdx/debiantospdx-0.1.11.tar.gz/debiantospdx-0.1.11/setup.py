# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['debiantospdx']

package_data = \
{'': ['*']}

install_requires = \
['scancode-toolkit==31.2.4']

entry_points = \
{'console_scripts': ['debiantospdx = debiantospdx.cli:entry']}

setup_kwargs = {
    'name': 'debiantospdx',
    'version': '0.1.11',
    'description': 'This tool generate SPDX files from your Debian system / packages',
    'long_description': '# debiantospdx\n\n[![Apache2.0 License](https://img.shields.io/badge/License-Apatch2.0-green.svg?style=for-the-badge)](https://choosealicense.com/licenses/apache-2.0/)\n\nシステムに存在するすべてのDebianパッケージのSPDXファイルを生成するコマンドラインツール\n\nパッケージ名・バージョン・ソフトウェアライセンス・コピーライト・パッケージ間の依存関係の解析を行う\n\n## Usage/Examples\n\n```bash\nteplate 1 3 5 -c 22 --both\n```\n\n## Authors\n\n- [@tk-tanab](https://github.com/tk-tanab)\n\n\n## License\n\n- [Apatch2.0](https://choosealicense.com/licenses/apache-2.0/)\n\n',
    'author': 'tk-tanab',
    'author_email': 'tk-tanab@ist.osaka-u.ac.jp',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/tk-tanab/debiantospdx',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
