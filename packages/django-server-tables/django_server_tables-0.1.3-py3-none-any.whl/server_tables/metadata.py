from collections import OrderedDict
from typing import Any

from rest_framework import serializers
from rest_framework.metadata import SimpleMetadata

from server_tables.fields import TableColumnInfo

_CUSTOM_WORD_LABEL_LIST_ = [
    ("Id", "ID"),
    ("Agro.club", "Agro.Club"),
]

SchemaDict = dict[str, Any]
FieldExtraInfo = dict[str, Any]


def _capitalize_label(label: str) -> str:
    if not label:
        return label

    if len(label) > 3:
        label = " ".join(w.capitalize() for w in label.split())
        for word in _CUSTOM_WORD_LABEL_LIST_:
            label = label.replace(word[0], word[1])
        return label
    else:
        return label.upper()


class DefaultMetaData(SimpleMetadata):
    """Custom class to get metadata for API.

    You can add or overwrite field data by adding
    `serializer_extra_metadata_fields_info` e.g.
    ```
    serializer_extra_metadata_fields_info = {
        "field_name": {
            "attr": "value",
        }
    }
    ```
    """

    exclude_fields = ("id", "has_unseen_events")
    serializer_extra_metadata_fields_info: dict[str, FieldExtraInfo | TableColumnInfo]

    def get_field_info(self, field) -> dict[str, Any]:
        """Capitalizes each word in field's label."""
        info = super().get_field_info(field)

        label = info.get("label")
        if label:
            info["label"] = _capitalize_label(label)

        extra_info = self._get_field_extra_info(field.field_name)
        if isinstance(extra_info, TableColumnInfo):
            extra_info = extra_info.to_dict()
        info.update(extra_info)

        return info

    def get_serializer_info(self, serializer):
        """Returns a dictionary of metadata about serializers fields.

        Copy-paste from rest_framework.metadata.SimpleMetadata
        with custom `_should_include_field` method.
        """
        self._set_serializer_extra_metadata_fields_info(serializer)

        if hasattr(serializer, "child"):
            # If this is a `ListSerializer` then we want to examine the
            # underlying child serializer instance instead.
            serializer = serializer.child
        return OrderedDict(
            [
                (field_name, self.get_field_info(field))
                for field_name, field in serializer.fields.items()
                if self._should_include_field(field)
            ],
        )

    def _should_include_field(self, field) -> bool:
        """Determines if field should be included in metadata."""
        if isinstance(field, serializers.HiddenField):
            return False

        return field.field_name not in self.exclude_fields

    def _set_serializer_extra_metadata_fields_info(self, serializer) -> None:
        """Takes extra field info from serializer and sets it as a class var."""
        self.serializer_extra_metadata_fields_info = getattr(
            serializer.Meta,
            "extra_metadata_fields_info",
            {},
        )

    def _get_field_extra_info(
        self,
        field_name: str,
    ) -> FieldExtraInfo | TableColumnInfo:
        return self.serializer_extra_metadata_fields_info.get(field_name, {})
