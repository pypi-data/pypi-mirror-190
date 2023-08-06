# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['citrus']

package_data = \
{'': ['*']}

install_requires = \
['pulp>=2.0,<3.0']

setup_kwargs = {
    'name': 'citrus',
    'version': '0.0.5',
    'description': 'A more convenient interface to doing Binary Linear Programming with PuLP',
    'long_description': "# Citrus\n\nIntended to work like [PuLP](https://github.com/coin-or/pulp), but with a few convenience functions thrown in.\n\n```bash\npip install citrus\n```\n\n# Comparisons\n\n## ANDing two variables\n\n```python\n# without citrus\nimport pulp\np = pulp.LpProblem('and example', pulp.LpMinimize)\n\nx = pulp.LpVariable('x', cat=pulp.LpBinary)\ny = pulp.LpVariable('y', cat=pulp.LpBinary)\nx_and_y = pulp.LpVariable('x_and_y', cat=pulp.LpBinary)\nmodel.addConstraint(x_and_y >= x + y - 1)\nmodel.addConstraint(x_and_y <= x)\nmodel.addConstraint(x_and_y <= y)\n```\n\n```python\n# with citrus\nimport citrus\np = citrus.Problem('and example', pulp.LpMinimize)\n\nx = p.make_var('x', cat=pulp.LpBinary)\ny = p.make_var('y', cat=pulp.LpBinary)\nx_and_y = x & y\n# alternatively, x_and_y = citrus.logical_and(x, y)\n```\n\n## ORing two variables\n\n```python\n# without citrus\nimport pulp\np = pulp.LpProblem('or example', pulp.LpMinimize)\n\nx = pulp.LpVariable('x', cat=pulp.LpBinary)\ny = pulp.LpVariable('y', cat=pulp.LpBinary)\nx_or_y = pulp.LpVariable('x_or_y', cat=pulp.LpBinary)\nmodel.addConstraint(x_or_y <= x + y)\nmodel.addConstraint(x_or_y >= x)\nmodel.addConstraint(x_or_y >= y)\n```\n\n```python\n# with citrus\nimport citrus\np = citrus.Problem('or example', pulp.LpMinimize)\n\nx = p.make_var('x', cat=pulp.LpBinary)\ny = p.make_var('y', cat=pulp.LpBinary)\nx_or_y = x | y\n# alternatively, x_or_y = citrus.logical_or(x, y)\n```\n\n## Negating a variable\n\n```python\n# without citrus\np = pulp.LpProblem('negation test', pulp.LpMinimize)\n\nx = pulp.LpVariable('x', cat=pulp.LpBinary)\nnot_x = pulp.LpVariable('not_x', cat=pulp.LpBinary)\np.addConstraint(not_x == 1 - x)\n```\n\n```python\n# With citrus\nimport citrus\np = citrus.Problem('negation test', pulp.LpMinimize)\n\nx = p.make_var('x', cat=pulp.LpBinary)\nnot_x = citrus.negate(x)\n```\n\n# Tips & Tricks\n\nSometimes, you'll have many variables that you want to AND or OR together:\n\n```python\np = citrus.Problem('vacation at some point', pulp.Maximize)\n\nvacation_in_x_month = [\n  p.make_var('vacation in ' + month, cat=pulp.LpBinary)\n  for month in MONTHS\n]\n\ntake_a_vacation = reduce(citrus.logical_or, vacation_in_x_month)\np.addConstraint(take_a_vacation)\n```\n\n# API\n\n## Classes\n\n- `Variable` is a subclass of `pulp.LpVariable`. It adds the following methods:\n\n  - (classmethod) `from_lp_var`. Upgrade a `pulp.LpVariable` to a Variable.\n  - `__or__(self, other)` Compute the `logical_or` of two binary `Variable`s\n  - `__and__(self, other)` Compute the `logical_and` of two binary `Variable`s\n  - `__and__(self, other)` Compute the `logical_and` of two binary `Variable`s\n  - `__abs__(self)` Create a new Variable restricted to the absolute value of this one.\n\n- `Problem` A subclass of `pulp.LpProblem`. It adds the following method\n  - `make_var()` accepts the same arguments as `pulp.LpVariable`, but produces a `Variable`\n\n## Functions\n\n- `negate(x: Variable)` Produce a new `Variable` with the opposite value of `x`.\n- `logical_and(x: Variable, y: Variable)` Produce a new `Variable` constrained to take on the AND of `x` and `y`.\n- `logical_or(x: Variable, y: Variable)` Produce a new `Variable` constrained to take on the OR of `x` and `y`.\n- `logical_xor(x: Variable, y: Variable)` Produce a new `Variable` constrained to take on the XOR of `x` and `y`.\n- `implies(x: Variable, y: Variable)` Produce a new variable constrained to take on the value of `x => y`\n- `minimum(*xs)` Produce a new `Variable` that can be no larger than the smallest in `xs`\n- `maximum(*xy)` Produce a new `Variable` that can be no smaller than the largest in `xs`\n",
    'author': 'Brian Schiller',
    'author_email': 'bgschiller@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/bgschiller/citrus',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
