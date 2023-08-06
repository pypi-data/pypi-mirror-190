# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['boxobj']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'boxobj',
    'version': '0.1.0',
    'description': 'A simple library to making working with regions of an image (OCR, CV, etc) easier to work with',
    'long_description': '# boxo\n`boxo` is a simple library that makes working with computer vision, OCR, and other tools that interact with regions \nof an image or document, simpler and more predictable. \n\n## Box\nThe core class in this library is `Box`. It handles many of the common approaches that different \nlibraries use to reference the region containing the returned results including:\n\n* **coordinates**: `[x1, y1, x2, y2]`\n* a dict containing the **position** defined by `top`, `left`, `width`, `height`\n* ***relative* coordinates** or **position** defined as a percentage of the size of the source: `[0.2, 0.5, 0.3, 0.8]`\n\nIn addition, it supports conversion from *bottom indexed* boxes like those used in older file types and libraries\nsuch as PDFs.\n\nBox internally represents its coordinates in pixels that are measured from the top-left, but it can return results\nusing other approaches as needed.\n\n```python\nfrom boxo import Box\n\n\ntlwh = { \'top\': 10, \'left\': 10, \'width\': 30, \'height\': 30 }\ncoords = [10, 10, 40, 40]\ncoords_ratio = [0.1, 0.1, 0.4, 0.4]\nobj = {\n    \'coordinates\': [10, 10, 40, 40],\n    \'label\': \'green\',\n    \'name\': \'my box\'\n}\n\nbox = Box.from_position(tlwh)\nbox = Box.from_coords(coords)\nbox = Box.from_position_percentage(coords_ratio, width=100, height=100)\nbox = Box.from_position_percentage(coords_ratio, top_origin=False, size=(100,100))\nbox = Box.from_dict(obj)\n```\n\nThe Box object supports a range of pythonic interactions including sort, addition, subtraction, multiplication, \ndivision and area calculations.\n\n```python\nfrom boxo import Box\n\n\nbox_a = Box([10, 10, 40, 40])\nbox_b = Box([15, 10, 30, 50])\nboxes = [box_b, box_a]\n\n# sort the boxes vertically\nboxes.sort()\n# sort the boxes horizontally\nboxes.sort(key=lambda x: x.left)\n\n# shift the position of a box\nbox_a_shifted_down = box_a + [0, 10] # [10, 20, 40, 50]\nbox_a_shifted_left = box_a - [5, 0] # [5, 10, 35, 40]\n\n# scale up the size of a box\nbox_a_bigger = box_a * 2 # [20, 20, 80, 80]\nbox_a_smaller = box_a / 3 # [3.333333, 3.333333, 13.333333, 13.333333]\nbox_a_smaller = round(box_a_smaller) # [3.3, 3.3, 13.3, 13.3]\nbox_a_smaller_floor = box_a // 3 # [3, 3, 13, 13]\n\n# Combine two boxes (union)\nbox_c = box_a + box_b # [10, 10, 40, 50]\n\n# Get the intersection of two boxes\nbox_i = box_a & box_b # [15, 10, 30, 40]\n\n# Get the area of a box\nbox_a_area = abs(box_a) # 900\nbox_b_area = box_a.area # 600\n```\n\nNote that to avoid the excessive precision that frequently makes its way into Boxes as they are moved and scaled, the\nrepr of a Box object limits the output to six digits after the decimal.\n\nOf course, these operands can be combined to perform common operations such as the common *intersection over union*\ncalculation used to evaluate agreement between two models.\n\n```python\niou = abs(box_a & box_b) / abs(box_a + box_b) # 0.375\n```\n\n### Attributes\nThe `Box` object also supports assigning attributes such as a `label` or `text` to the object to associate it with\na set of values. \n\n```python\nfrom boxo import Box\n\ncv_box = Box([10, 10, 30, 50], {"label": "cat", "confidence": 0.84})\ncv_box_2 = Box({"coordinates": [10, 10, 30, 50], "label": "cat", "confidence": 0.84})\nocr_box = Box([3, 4, 67, 10], text="Boxo is great for working with boxes")\n```\n\nAs you can see, there are a variety of options for creating a `Box` object from whatever source system produced it. \nHere the `cv_box` value is created by passing the coordinates first, then a dict containing the associated attributes.\n`cv_box_2` is the same value, but here the coordinates and attributes are contained in a single dict object. Finally,\nthe `ocr_box` is created by passing coordinates and using keyword arguments to assign attributes. This flexibility is\nintentional to make it easier to handle the varying approaches different tools use to represent data.\n\nInternally the `boxo` classes keep the attributes and coordinate values separate to make them easier to work with.\nThis shows up in how the objects are represented when printed or displayed in the output. The following is the\nrepresentation of the objects above.\n\n```\nBox([10, 10, 30, 50], {\'label\': \'cat\', \'confidence\': 0.84})\nBox([10, 10, 30, 50], {\'label\': \'cat\', \'confidence\': 0.84})\nBox([3, 4, 67, 10], {\'text\': \'Boxo is great for working with boxes\'})\n```\n\ndata and serialization\n\npage\npages\npage indices\n',
    'author': 'dschultz0',
    'author_email': 'dave@daveschultzconsulting.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
