import copy
from typing import Any, List

from django_filters import OrderingFilter
from rest_framework.response import Response

SchemaDict = dict[str, Any]


class ListSchemaMixin:
    """Mixin to simplify getting schema for list APIs."""

    def list(self, request, *args, **kwargs):
        """Returns list of items or schema for it."""
        if request.GET.get("schema") is not None:
            return self._list_schema()

        return super().list(request, *args, **kwargs)  # type: ignore

    def _get_filter_fields(self) -> List[str]:
        filterset_class = self.filterset_class  # type: ignore
        filters = filterset_class.get_filters()

        for filter_field in filters.values():
            if isinstance(filter_field, OrderingFilter):
                sortable_fields = filter_field.param_map.keys()
                break
        else:
            raise AttributeError
        return sortable_fields

    def _add_sortable_to_schema(self, data: SchemaDict) -> SchemaDict:
        if not hasattr(self, "filterset_class"):
            return data

        try:
            sortable_fields = self._get_filter_fields()
        except AttributeError:
            return data

        result_data = copy.deepcopy(data)
        for sortable_field in sortable_fields:
            if sortable_field in result_data:
                result_data[sortable_field]["sortable"] = True
        return result_data

    def _list_schema(self) -> Response:
        data = self._get_schema_dict()
        return Response(data)

    def _get_schema_dict(self) -> SchemaDict:
        meta = self.metadata_class()  # type: ignore
        serializer = self.get_serializer()  # type: ignore
        schema = meta.get_serializer_info(serializer)
        return self._add_sortable_to_schema(schema)
