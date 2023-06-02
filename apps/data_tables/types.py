from typing import List

import strawberry.django
from django.db.models import Count, F, Q
from strawberry import auto

from apps.data_tables import models


@strawberry.django.type(models.Classification)
class ClassificationType:
    id: auto
    name: auto
    level: auto


@strawberry.django.type(models.AccessAttribute)
class AccessAttributeType:
    id: auto
    name: auto


@strawberry.django.type(models.DataTable)
class DataTableType:
    id: auto
    name: auto
    classification: ClassificationType
    access_attributes: List[AccessAttributeType] = strawberry.django.field()

    @strawberry.field
    def rows(self, info) -> List["DataRowType"]:
        user = info.context.request.user
        clearance_level = user.clearance.level if user.clearance else 0
        user_attributes = user.access_attributes.all()
        accessible_rows = (
            models.DataRow.objects.filter(
                Q(table__id=self.id),
                Q(classification__level__lte=clearance_level) | Q(classification__isnull=True),
            )
            .annotate(
                num_required_attributes=Count("access_attributes"),
                num_user_attributes=Count("access_attributes", filter=Q(access_attributes__in=user_attributes)),
            )
            .filter(num_required_attributes=F("num_user_attributes"))
            .distinct()
        )
        return accessible_rows

    @strawberry.field
    def columns(self, info) -> List["DataColumnType"]:
        user = info.context.request.user
        clearance_level = user.clearance.level if user.clearance else 0
        user_attributes = user.access_attributes.all()
        accessible_columns = (
            models.DataColumn.objects.filter(
                Q(table__id=self.id),
                Q(classification__level__lte=clearance_level) | Q(classification__isnull=True),
            )
            .annotate(
                num_required_attributes=Count("access_attributes"),
                num_user_attributes=Count("access_attributes", filter=Q(access_attributes__in=user_attributes)),
            )
            .filter(num_required_attributes=F("num_user_attributes"))
            .distinct()
        )
        return accessible_columns


@strawberry.django.type(models.DataRow)
class DataRowType:
    id: auto
    classification: ClassificationType
    access_attributes: List[AccessAttributeType] = strawberry.django.field()
    table: DataTableType = strawberry.django.field()

    @strawberry.field
    def cells(self, info) -> List["DataCellType"]:
        user = info.context.request.user
        clearance_level = user.clearance.level if user.clearance else 0
        user_attributes = user.access_attributes.all()
        accessible_columns = DataTableType.columns(self.table, info)

        accessible_cells = (
            models.DataCell.objects.filter(
                Q(row__id=self.id),
                Q(column__in=accessible_columns),
                Q(classification__level__lte=clearance_level) | Q(classification__isnull=True),
            )
            .annotate(
                num_required_attributes=Count("access_attributes"),
                num_user_attributes=Count("access_attributes", filter=Q(access_attributes__in=user_attributes)),
            )
            .filter(num_required_attributes=F("num_user_attributes"))
            .distinct()
        )
        return accessible_cells


@strawberry.django.type(models.DataColumn)
class DataColumnType:
    id: auto
    name: auto
    classification: ClassificationType
    access_attributes: List[AccessAttributeType] = strawberry.django.field()


@strawberry.django.type(models.DataCell)
class DataCellType:
    id: auto
    data: auto
    classification: ClassificationType
    access_attributes: List[AccessAttributeType] = strawberry.django.field()
    row: DataRowType = strawberry.django.field()
    column: DataColumnType = strawberry.django.field()
