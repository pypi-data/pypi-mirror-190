# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bindpy']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'bindpy',
    'version': '0.1.0',
    'description': 'The bindpy package allows for partial application of arguments to a function, making it easy to create specialized versions of the function with some arguments pre-filled.',
    'long_description': '# bindpy\n\nThe bindpy package allows for partial application of arguments to a function, making it easy to create specialized versions of the function with some arguments pre-filled.\nIt is a better version of the Python\'s standard `partial` function from the `functools` package inspired by C++\'s `std::bind`.\n\n## Install\n\nExpect gracefully crafted support for any version of Python 3+, but confidently tested in version 3.7 and higher.\n\n```\npip install bindpy\n```\n\n## Usage\n\n\n```python\nfrom bindpy import *\n```\n\n### `bind` function\n\nThe `show` function takes three arguments, `a1`, `a2` and `a3`, and returns a string composed of their values separated by spaces. The `show_10` function is a partially applied version of `show`, with `a2` bound to `_1`, `a1` bound to `_2` and `a3` bound to `10`.\n\nBind support placeholders : `_1`, `_2`, ... `_10`. The placeholders allow you to partially apply a function and leave certain arguments to be filled in later. This allows you to reuse the partially applied function and pass different values for the placeholder argument.\n\nOverall, `bind` and placeholders make it easier to create reusable and composable functions by allowing you to fix certain arguments and create new functions that take fewer arguments.\n\n```python\ndef show(a1, a2, a3):\n    return " ".join(map(str, [a1, a2, a3]))\n    \nshow_10 = bind(show, _2, _1, a3=10)\n\nprint(show_10(20, 30)) # output: 30 20 10\n```\n\n***Convenient to use with functional style.***  \n\nIf you find lambda expressions unappealing, you can use bind for a more convenient and aesthetically pleasing experience with functional programming.\n\n```python\ndef add(a, b, c):\n  return a + b * c\n  \nnumbers = [1, 2, 3, 4]\nprint(list(map(bind(add, _1, 10, 2), numbers))) # output 21 22 23 24\n# same code with lambda\nprint(list(map(lambda x: add(x, 10, 2), numbers)))\n```\n\n```python\nimport os # used for example\n\nfiles = [\'a.txt\', \'b.json\']\nmy_join = bind(os.path.join, \'.\', \'data\')\nprint(list(map(my_join, files))) # output [\'./data/a.txt\', \'./data/b.json\']\n```\n### `bind_front` function\n\n`bind_front` pre-specifies function arguments like `functools.partial`. It takes a function and values, returns new function with values bound to front. When called with remaining args, values passed to `bind_front` are automatically inserted in front.\n\n```python\ndef add(a, b, c=0):\n    return a + b + c\n\n\nadd_10 = bind_front(add, 10)\nresult = add_10(20, c=30)\nprint(result)  # 60\n\nadd_20_30 = bind_front(add, 20, 30)\nresult = add_20_30() # call add(20, 30)\nprint(result)  # 50\n```\n\n### `bind_back` function\n\n`bind_back` also pre-specifies function arguments but with values bound to end of arg list after all others. It takes a function and key-value pairs, returns new function with values bound to end. When called with remaining args, values passed to `bind_back` are automatically inserted at end.\n\n```python\nadd_30 = bind_back(add, c=30)\nresult = add_30(10, 20)\nprint(result)  # 60\n\nadd_40 = bind_back(add, 40)\nresult = add_40(10, 20) # call add(10, 20, 40)\nprint(result)  # 70\n\nadd_10 = bind_back(add, 10)\nresult = add_10(12)  # call add(10, 12), c=0 by  default\nprint(result)  # 22\n```\n\n### sequential binding\n\nYou can combine `bind_front` and `bind_back` to create a function that has arguments pre-specified at both the front and end of the argument list. \nFor example, the code:\n```python\ndef func(p1, p2, p3, p4, p5):\n    return " ".join(map(str, [p1, p2, p3, p4, p5]))\n    \nb_func = bind_front(bind_back(func, 4, 5), 1, 2)\nprint(bfunc(3)) # 1 2 3 4 5\n```\n\ncan be replaced with:\n\n```python\nb_func_v2 = bind(1, 2, _1, 4, 5) # using placeholder *_1*\nprint(bfunc(3)) # 1 2 3 4 5\n```\n\n----\n\nWe hope this information helps you effectively use the bind functions in your project. If you have any questions or feedback, please reach out to us. Happy coding!\n\n----\n\n## Acknowledgements\n\nWe would like to express our sincere gratitude to all the individuals who have made this project a reality. Their contributions, guidance, and support have been invaluable. Thank you to everyone who has played a part in bringing this project to life.\n\n* [Daniil Dudkin](https://github.com/unterumarmung)\n* ChatGPT\n',
    'author': 'Nikita Avdosev',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.0',
}


setup(**setup_kwargs)
