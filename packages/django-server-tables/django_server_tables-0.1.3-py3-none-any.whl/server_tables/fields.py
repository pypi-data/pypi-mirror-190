from dataclasses import asdict, dataclass, replace
from typing import Any


@dataclass
class TableColumnInfo:
    """Additional field info for frontend."""

    width: int
    type: str | None = "string"  # noqa: VNE003, CCE001

    class Meta:
        rewrite_type = True

    def to_dict(self) -> dict[str, Any]:
        """Create dict of info."""
        data_dict = asdict(self)
        if self.Meta.rewrite_type is False or self.type is None:
            data_dict.pop("type")
        return data_dict

    def __get__(self, instance, owner):
        """Change rewrite_type attr to owners value."""
        if (
            owner is None
            or not hasattr(owner, "Meta")
            or not hasattr(owner.Meta, "rewrite_type")
        ):
            return self
        if owner.Meta.rewrite_type is False and self.Meta.rewrite_type is True:
            obj = replace(self)
            obj.type = None
            return obj
        return self


class DefaultTableColumnTypes:
    """Types of additional field info."""

    ID = TableColumnInfo(width=200, type="id")
    NUMBER = TableColumnInfo(width=160, type="number")
    NAME = TableColumnInfo(width=150, type="name")
    ADDRESS = TableColumnInfo(width=250, type="address")
    SHORT_DESCRIPTION = TableColumnInfo(width=200, type="short_description")
    PRICE = TableColumnInfo(width=140, type="price")
    DATE = TableColumnInfo(width=140, type="date")
    STATUS = TableColumnInfo(width=110, type="status")  # noqa: CCE001

    class Meta:
        rewrite_type = True
