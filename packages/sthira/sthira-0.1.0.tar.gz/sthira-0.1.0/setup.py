# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['sthira']
setup_kwargs = {
    'name': 'sthira',
    'version': '0.1.0',
    'description': 'The `Constant` class is a metaclass for creating classes with constant attributes',
    'long_description': '# Sthira\n\n> The word for "constant" in Sanskrit can be translated as "स्थिर" (sthira)\n\n\nThe `Constant` class is a metaclass for creating classes with constant attributes. \nOnce set, the attributes of a `Constant` class cannot be changed, and new attributes cannot be added. \nThis allows for creating classes that represent unchangeable values, such as constants, enums, and similar constructs. \nThe Constant class also provides a `__str__`and `__repr__` implementation for convenient representation of the class.\n\n## Usage\n\n```python\nfrom sthira import constant\n\n\n@constant\nclass Mammal:\n\tHUMAN = "human"\n\tTIGER = "tiger"\n\tLION = "lion"\n\nclass Bird:\n\tCROW = "crow"\n\tHAWK = "hawk"\n\nclass Fish:\n\tTUNA = "tuna"\n\n@constant\nclass Animal:\n\tMAMMAL = Mammal\n\tBIRD = Bird\n\tFISH = Fish\n\nprint(f"{Animal.MAMMAL}")\nprint(f"{Animal.MAMMAL.HUMAN}")\nprint(f"{Animal.BIRD.CROW}")\n\n```\n\n> Output\n\n```\nMammal\nhuman\ncrow\n```\n\n## Cannot modify attributes\n\n```python\nAnimal.MAMMAL.HUMAN = "HomoSapiens"\n\n#     raise AttributeError("Cannot set or change the class attributes")\n# AttributeError: Cannot set or change the class attributes\n```\n\n## Unit tests\n\n```python -m unittest test_constant.py```\n\n',
    'author': 'neelabalan',
    'author_email': 'neelabalan.n@outlook.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'py_modules': modules,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
