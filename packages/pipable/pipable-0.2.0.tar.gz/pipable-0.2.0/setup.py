# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pipable']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['pump = pump:main']}

setup_kwargs = {
    'name': 'pipable',
    'version': '0.2.0',
    'description': 'pseudo pipe operation in python',
    'long_description': '# pipable\n\n> pseudo pipe operation in python\n\n[![ci-badge]][ci-url] [![coverage-badge]][coverage-url] [![pypi-badge]][pypi-url] [![py-version]][py-url] [![MIT-badge]][MIT-url] [![black-badge]][black-url]\n\n🔗 [source code](https://github.com/hoishing/pipable)\n\n## Quick Start\n\n### Create the Pipe Object\n\n- instantiate with the `Pipe` class\n\n```python\nfrom pipable import Pipe\n\nlist_ = Pipe(list)\n"abc" | list_    # ["a", "b", "c"]\n```\n\n#### Pipe Object is Partial with Infix Operator\n\n- at the core Pipe create partial function while overriding it\'s `|` operator\n- instantiate Pipe object like the built-in `functools.partial`\n- preceding output will be assigned to the last positional argument of the Pipe object\n\n```python\nsquare = Pipe(pow, exp=2)\n3 | square    # 9\n```\n\nSince that Pipe appends preceding output to the last positional argument,\nassigning 1st argument with keyword will raise exception.\nThis behave the same as `functools.partial`\n\n```python\nbase2 = Pipe(pow, 2)  # positional arg ok\n3 | base2    # 8\n\nbase2 = Pipe(pow, base=2)  # keyword arg don\'t\n3 | base2    # raise!!\n```\n\n### Using Decorator\n\n- `@Pipe` decorator can transform function into Pipe object\n- preceding output will be assigned to the last positional argument\n- instantiate Pipe decorated function similar to creating partial\n\n```python\n# only one argument\n@Pipe\ndef hi(name: str) -> str:\n  return f"hi {name}"\n\n"May" | hi    # "hi May"\n\n\n# multiple arguments\n@Pipe\ndef power(base: int, exp: int) -> int:\n  return a ** b\n\n# instantiate Pipe obj by partially calling the function\n2 | power(3)        # 9, note we need to use positional argument here\n2 | power(exp=3)    # 8, subsequent arguments can use keyword\n\n# assign the 1st argument with keyword will raise exception\n2 | power(base=3)    # raise !!\n```\n\n## Motivation\n\nPipe operation is a handy feature in functional programming. It allows us to:\n\n- write more succinct and readable code\n- create less variables\n- easily create new function by chaining other functions\n\nHowever it\'s still a missing feature in Python as of 2023. This package try to mimic pipe operation by overriding the bitwise-or operator, and turn any function into pipable partial.\n\nThere are packages, such as [Pipe][pipe] take the similar approach. It works great with iterables, and create pipe as iterator, ie. open pipe). However, I simply want to take preceding expression as an input argument of the current function then execute it, ie. close pipe. It leads to the creation of this package.\n\n## FAQ\n\nHow can I assign value to the first argument?\n  \nAssign it within a wrapper function\n\n```python\nsquare = Pipe(lambda x: pow(x, 2))\n3 | square  # 9\n```\n\n---\n\nCan I create open pipe?\n\n`Pipe` only create closed pipe, ie. execute the function after piping with the `|` operator. You may consider other solutions such as:\n\n- [pipe][pipe], which create open pipe for iterators\n- [Coconut][coconut], a python variant that embrace functional programming\n\n---\n\nCan I append the preceding output at the beginning of the argument list?\n\nPut the preceding output as the 1st argument of a wrapper function\n\n```python\n# prepend is the default behaviour\ndef kebab(*args):\n  return "-".join(*args)\n\n\'a\' | Pipe(kebab, \'b\', \'c\')  # \'b c a\'\n\n@Pipe\ndef wrapper(first, others):\n  return kebab(first, *others)\n\n\'a\' | wrapper(others=[\'b\', \'c\'])  # \'a b c\'\n```\n\n## Need Help?\n\nOpen a [github issue](https://github.com/hoishing/pipable/issues) or ping me on [Twitter](https://twitter.com/hoishing) ![](https://api.iconify.design/logos/twitter.svg?width=20)\n\n[ci-badge]: https://github.com/hoishing/pipable/actions/workflows/ci.yml/badge.svg\n[ci-url]: https://github.com/hoishing/pipable/actions/workflows/ci.yml\n[coverage-badge]: https://hoishing.github.io/pipable/assets/coverage-badge.svg\n[coverage-url]: https://hoishing.github.io/pipable/assets/coverage/\n[MIT-badge]: https://img.shields.io/github/license/hoishing/pipable\n[MIT-url]: https://opensource.org/licenses/MIT\n[pypi-badge]: https://img.shields.io/pypi/v/pipable\n[pypi-url]: https://pypi.org/project/pipable/\n[black-badge]: https://img.shields.io/badge/code%20style-black-000000.svg\n[black-url]: https://github.com/psf/black\n[py-version]: https://img.shields.io/pypi/pyversions/pipable\n[py-url]: https://python.org\n[pipe]: https://pypi.org/project/pipe\n[coconut]: https://github.com/evhub/coconut\n',
    'author': 'Kelvin Ng',
    'author_email': 'hoishing@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://hoishing.github.io/pipable',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
