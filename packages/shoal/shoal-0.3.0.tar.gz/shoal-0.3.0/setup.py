# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['shoal']

package_data = \
{'': ['*']}

install_requires = \
['beartype>=0.12.0', 'pydantic>=1.10.4', 'rich>=13.3.1']

setup_kwargs = {
    'name': 'shoal',
    'version': '0.3.0',
    'description': 'Lazy, Python-first, alternative to make, just, doit, and invoke',
    'long_description': '# shoal\n\nPython function and shell command task runner. Alternative to `make`, [`just`](https://github.com/casey/just), [`doit`](https://github.com/pydoit/doit), and [`invoke`](https://pypi.org/project/invoke). Used in [`calcipy`](https://pypi.org/project/calcipy)\n\n## Installation\n\n`poetry add shoal`\n\n## Usage\n\nThere are two ways to use `shoal`, either as a way to organize a set of local tasks or to distribute with a package.\n\nFor more example code, see the [scripts] directory or the [tests].\n\n### Local Runner\n\nCreate a `shoals.py` file with:\n\n```py\nfrom shoal import shoalling\n\nshoalling()\n```\n\nThen run the file with:\n\n```sh\npoetry run python shoals.py --task-help\n```\n\nAdd additional tasks or import tasks from a third party package (such as [`calcipy`](https://pypi.org/project/calcipy))\n\n### Package\n\nCreate a `<package>/shoals.py` file with:\n\n```py\nfrom shoal import shoalling  # noqa: F401\n```\n\nAdd the file to your `pyproject.toml` scripts:\n\n```toml\n[tool.poetry.scripts]\nshoal = "shoal:shoalling"\n```\n\nThen test with:\n\n```sh\npoetry run shoal --task-help\n```\n\n## Project Status\n\nSee the `Open Issues` and/or the [CODE_TAG_SUMMARY]. For release history, see the [CHANGELOG].\n\n## Contributing\n\nWe welcome pull requests! For your pull request to be accepted smoothly, we suggest that you first open a GitHub issue to discuss your idea. For resources on getting started with the code base, see the below documentation:\n\n- [DEVELOPER_GUIDE]\n- [STYLE_GUIDE]\n\n## Code of Conduct\n\nWe follow the [Contributor Covenant Code of Conduct][contributor-covenant].\n\n### Open Source Status\n\nWe try to reasonably meet most aspects of the "OpenSSF scorecard" from [Open Source Insights](https://deps.dev/pypi/shoal)\n\n## Responsible Disclosure\n\nIf you have any security issue to report, please contact the project maintainers privately. You can reach us at [dev.act.kyle@gmail.com](mailto:dev.act.kyle@gmail.com).\n\n## License\n\n[LICENSE]\n\n[changelog]: ./docs/CHANGELOG.md\n[code_tag_summary]: ./docs/CODE_TAG_SUMMARY.md\n[contributor-covenant]: https://www.contributor-covenant.org\n[developer_guide]: ./docs/DEVELOPER_GUIDE.md\n[license]: https://github.com/kyleking/shoal/LICENSE\n[scripts]: https://github.com/kyleking/shoal/scripts\n[style_guide]: ./docs/STYLE_GUIDE.md\n[tests]: https://github.com/kyleking/shoal/tests\n',
    'author': 'Kyle King',
    'author_email': 'dev.act.kyle@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/kyleking/shoal',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.12,<4.0.0',
}


setup(**setup_kwargs)
