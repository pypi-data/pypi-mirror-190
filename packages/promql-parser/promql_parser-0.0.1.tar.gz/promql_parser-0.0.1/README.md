# py-promql-parser

![CI](https://github.com/messense/promql-parser/workflows/CI/badge.svg)
[![PyPI](https://img.shields.io/pypi/v/promql-parser.svg)](https://pypi.org/project/promql-parser)

[ammonia](https://github.com/rust-ammonia/ammonia) Python binding.

## Installation

```bash
pip install promql-parser
```

## Usage

```python
import promql_parser

ast = promql_parser.parse("")
print(ast)
```

## License

This work is released under the MIT license. A copy of the license is provided in the [LICENSE](./LICENSE) file.
