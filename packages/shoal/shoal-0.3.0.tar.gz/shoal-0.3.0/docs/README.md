# shoal

Python function and shell command task runner. Alternative to `make`, [`just`](https://github.com/casey/just), [`doit`](https://github.com/pydoit/doit), and [`invoke`](https://pypi.org/project/invoke). Used in [`calcipy`](https://pypi.org/project/calcipy)

## Installation

`poetry add shoal`

## Usage

There are two ways to use `shoal`, either as a way to organize a set of local tasks or to distribute with a package.

For more example code, see the [scripts] directory or the [tests].

### Local Runner

Create a `shoals.py` file with:

```py
from shoal import shoalling

shoalling()
```

Then run the file with:

```sh
poetry run python shoals.py --task-help
```

Add additional tasks or import tasks from a third party package (such as [`calcipy`](https://pypi.org/project/calcipy))

### Package

Create a `<package>/shoals.py` file with:

```py
from shoal import shoalling  # noqa: F401
```

Add the file to your `pyproject.toml` scripts:

```toml
[tool.poetry.scripts]
shoal = "shoal:shoalling"
```

Then test with:

```sh
poetry run shoal --task-help
```

## Project Status

See the `Open Issues` and/or the [CODE_TAG_SUMMARY]. For release history, see the [CHANGELOG].

## Contributing

We welcome pull requests! For your pull request to be accepted smoothly, we suggest that you first open a GitHub issue to discuss your idea. For resources on getting started with the code base, see the below documentation:

- [DEVELOPER_GUIDE]
- [STYLE_GUIDE]

## Code of Conduct

We follow the [Contributor Covenant Code of Conduct][contributor-covenant].

### Open Source Status

We try to reasonably meet most aspects of the "OpenSSF scorecard" from [Open Source Insights](https://deps.dev/pypi/shoal)

## Responsible Disclosure

If you have any security issue to report, please contact the project maintainers privately. You can reach us at [dev.act.kyle@gmail.com](mailto:dev.act.kyle@gmail.com).

## License

[LICENSE]

[changelog]: ./docs/CHANGELOG.md
[code_tag_summary]: ./docs/CODE_TAG_SUMMARY.md
[contributor-covenant]: https://www.contributor-covenant.org
[developer_guide]: ./docs/DEVELOPER_GUIDE.md
[license]: https://github.com/kyleking/shoal/LICENSE
[scripts]: https://github.com/kyleking/shoal/scripts
[style_guide]: ./docs/STYLE_GUIDE.md
[tests]: https://github.com/kyleking/shoal/tests
