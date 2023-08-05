# django-server-tables
Django server tables is a library for generating json schema for (DRF)[https://www.django-rest-framework.org] list view serializer. This library provides the capability to control various attributes of a front-end table, such as column width and data type, from the back-end.

## Installation
1. Use the following pip command to install the package:
    ```bash
    pip install django-server-tables
    ```
2. Add the following line to your REST_FRAMEWORK configuration:
    ```python
    REST_FRAMEWORK = {
         ...
         'DEFAULT_METADATA_CLASS': 'server_tables.DefaultMetaData',
     }
    ```

## Usage
1. Add the `ListSchemaMixin` to your ModelViewSet:
   ```python
   from server_tables import ListSchemaMixin
   
   class MyViewSet(ListSchemaMixin, viewsets.ModelViewSet):
       """View set with schema endpoint."""
   ```
2. Your ViewSet will now have an additional endpoint at the URL `GET viewset_base_url/?schema`, with a response like the following:
   ```json
   {
      "field": {
         "type": "string",
         "required": true,
         "read_only": false,
         "label": "Field"
      }
   }
   ```

3. You can add additional data to the schema using the `extra_metadata_fields_info attribute` in your list serializer:
   ```python
   class MySerializer(serializers.ModelSerializer):    
       Meta:
           model = MyModel
           fields = [
               'field',
           ]
           extra_metadata_fields_info = {
               'field': {'width': 10}
           }
   ```
   Now your schema will look like this:
   ```json
   {
      "field": {
         "type": "string",
         "required": true,
         "read_only": false,
         "label": "Field",
         "width": 10
      }
   }
   ```

4. Alternatively, you can use default fields info:
   ```python
   from server_tables import DefaultTableColumnTypes
   
   class MySerializer(serializers.ModelSerializer):    
       Meta:
           model = MyModel
           fields = [
               'field',
           ]
           extra_metadata_fields_info = {
               'field': DefaultTableColumnTypes.NAME,
           }
   ```


## License
The library is licensed under the MIT License.