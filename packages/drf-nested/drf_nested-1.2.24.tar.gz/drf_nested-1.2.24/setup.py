# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['drf_nested', 'drf_nested.mixins', 'drf_nested.utils']

package_data = \
{'': ['*']}

install_requires = \
['django>=2.0', 'djangorestframework>=3.8.0']

setup_kwargs = {
    'name': 'drf-nested',
    'version': '1.2.24',
    'description': '',
    'long_description': '## DRF Nested Utils\n\n[![pypi package](https://img.shields.io/pypi/v/drf-nested.svg)](https://pypi.org/project/drf-nested/)\n\nThis package provides a set of utils to help developers implement nested data handling for Django Rest Framework.\n\nThis package adds support for:\n* Direct relation handling (`ForeignKey`)\n* Reverse relation handling (i.e. allows working with models that have current as `ForeignKey`)\n* Direct and reverse `ManyToMany`, with special flow for the m2m relationships with custom `through` models\n* `GenericRelation` with special mixins\n\nIt also provides mixins for handling `Unique` and `UniqueTogether` validators.\n\n## Mixins\n\n### Nested Serializer Mixins\n\n#### `BaseNestedMixin`\n\nBase mixin that contains the methods for retrieval of all related fields of the serializer model. \nIt also provides all the `update_or_create` methods for each type of fields \n(`direct relation`, `reverse relation`, `many-to-many relation` and `generic relation`).\n\n#### `CreateNestedMixin`\n\nMixin that allows creation of the nested models on serializer `create` call. \nYou can provide a list of fields that should be forbidden on create, \nthe list of fields should be placed into the `forbidden_on_create` \nfield on serializer `Meta` class.\nMixin uses `BaseNestedMixin` properties and `update_and_create` methods to create nested fields.\n\n#### `UpdateNestedMixin`\n\nMixin that allows modification of the nested models on serializer `update` call.\nMixin uses `BaseNestedMixin` properties and `update_and_create` methods to update nested fields.\n\n### Validator Mixins\n\n#### `UniqueFieldMixin`\n\nMixin that allows usage of the `unique` fields with nested mixins. \nThis mixin moves the validation process from `is_valid` to `create/update` call. \nThis is done because the fields that should be used in the `unique` validation may not be \nset on the initial `is_valid` call and are set just before the nested `create/update` call. \n\n#### `UniqueTogetherMixin`\n\nMixin that allows usage of the `unique_together` fields with nested mixins. \nThis mixin moves the validation process from `is_valid` to `create/update` call. \nThis is done because the fields that should be used in the `unique_together` validation may not be \nset on the initial `is_valid` call and are set just before the nested `create/update` call.\n\n### Helper Mixins\n\n#### `NestableMixin`\n\nMixin that allows to specify the name of the nested field by setting `write_source` if the initial `source` of the field is different \nfrom the field name or the initial `source` is not writable (a property, for example).\n\n#### `ThroughMixin`\n\nMixin that allows to specify if `through` model should be connected to current model after the `through` model `create/update` call.\n\n#### `GenericRelationMixin`\n\nMixin that should be used on serializers that represent connected by `GenericRelation` models.\n\n## Examples\n\nYou can see an example project in `examples/` directory.\n\n## Notes\n\n> If you are using a Many-to-Many field with `source` property or you have a `through` model on your serializer, \nyou should add a `NestableMixin` to the target serializer and add a `write_source` field when you initialize that serializer.\n\n> In case of the `source` property you should add an actual model field that would allow you to properly connect your model with related ones. \n\n> In case of the `through` model you should have it set to the `related_name` of the connected `through` model\n\n> You can also use `ThroughMixin` and set `connect_to_model` to False if you want to have the ability to keep the `through` model connection in case the `through` model ForeignKey should be different from the current model.',
    'author': 'Artur Veres',
    'author_email': 'artur8118@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
