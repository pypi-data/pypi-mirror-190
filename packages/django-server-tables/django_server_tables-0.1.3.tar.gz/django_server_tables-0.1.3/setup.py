# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['server_tables']

package_data = \
{'': ['*']}

install_requires = \
['django-filter>=22.1,<23.0', 'djangorestframework>=3.14.0,<4.0.0']

setup_kwargs = {
    'name': 'django-server-tables',
    'version': '0.1.3',
    'description': 'Utils to configure tables data on the server.',
    'long_description': '# django-server-tables\nDjango server tables is a library for generating json schema for (DRF)[https://www.django-rest-framework.org] list view serializer. This library provides the capability to control various attributes of a front-end table, such as column width and data type, from the back-end.\n\n## Installation\n1. Use the following pip command to install the package:\n    ```bash\n    pip install django-server-tables\n    ```\n2. Add the following line to your REST_FRAMEWORK configuration:\n    ```python\n    REST_FRAMEWORK = {\n         ...\n         \'DEFAULT_METADATA_CLASS\': \'server_tables.DefaultMetaData\',\n     }\n    ```\n\n## Usage\n1. Add the `ListSchemaMixin` to your ModelViewSet:\n   ```python\n   from server_tables import ListSchemaMixin\n   \n   class MyViewSet(ListSchemaMixin, viewsets.ModelViewSet):\n       """View set with schema endpoint."""\n   ```\n2. Your ViewSet will now have an additional endpoint at the URL `GET viewset_base_url/?schema`, with a response like the following:\n   ```json\n   {\n      "field": {\n         "type": "string",\n         "required": true,\n         "read_only": false,\n         "label": "Field"\n      }\n   }\n   ```\n\n3. You can add additional data to the schema using the `extra_metadata_fields_info attribute` in your list serializer:\n   ```python\n   class MySerializer(serializers.ModelSerializer):    \n       Meta:\n           model = MyModel\n           fields = [\n               \'field\',\n           ]\n           extra_metadata_fields_info = {\n               \'field\': {\'width\': 10}\n           }\n   ```\n   Now your schema will look like this:\n   ```json\n   {\n      "field": {\n         "type": "string",\n         "required": true,\n         "read_only": false,\n         "label": "Field",\n         "width": 10\n      }\n   }\n   ```\n\n4. Alternatively, you can use default fields info:\n   ```python\n   from server_tables import DefaultTableColumnTypes\n   \n   class MySerializer(serializers.ModelSerializer):    \n       Meta:\n           model = MyModel\n           fields = [\n               \'field\',\n           ]\n           extra_metadata_fields_info = {\n               \'field\': DefaultTableColumnTypes.NAME,\n           }\n   ```\n\n\n## License\nThe library is licensed under the MIT License.',
    'author': 'egrvdaniil',
    'author_email': 'd.egorov@agro.club',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/Agro-Club/django-server-tables',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
