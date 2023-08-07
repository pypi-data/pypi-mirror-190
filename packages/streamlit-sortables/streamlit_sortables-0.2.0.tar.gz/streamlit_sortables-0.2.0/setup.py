# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['streamlit_sortables']

package_data = \
{'': ['*']}

install_requires = \
['streamlit>=1.0.0']

setup_kwargs = {
    'name': 'streamlit-sortables',
    'version': '0.2.0',
    'description': 'A Streamlit component to provide sortable list.',
    'long_description': "# Streamlit Sortables\n\nA Streamlit component to provide sortable list.\nYou can sort the list of strings on the UI as follows.\n\nhttps://user-images.githubusercontent.com/329750/163662202-ce292fc4-2882-46ac-8c2c-ca4b9df675d2.mp4\n\n\n## Instllation\n\n```python\n$ pip install streamlit-sortables\n```\n\n## Usage\n\nCall `soretd_items` method with a list of string. Return value is the sorted items.\n\n```python\nimport streamlit as st\nfrom streamlit_sortables import sort_items\n\n\noriginal_items = ['A', 'B', 'C']\nsorted_items = sort_items(original_items)\n\nst.write(f'original_items: {original_items}')\nst.write(f'sorted_items: {sorted_items}')\n```\n\nYou can pass list of dicts with `multi_containers=True`.\n\n```python\n\nimport streamlit as st\nfrom streamlit_sortables import sort_items\n\noriginal_items = [\n    {'header': 'first container',  'items': ['A', 'B', 'C']},\n    {'header': 'second container', 'items': ['D', 'E', 'F']}\n]\n\nsorted_items = sort_items(original_items, multiple_contaieners=True)\n\nst.write(f'original_items: {original_items}')\nst.write(f'sorted_items: {sorted_items}')\n```\n",
    'author': 'ohtaman',
    'author_email': 'ohtamans@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/ohtaman/streamlit-sortables',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
