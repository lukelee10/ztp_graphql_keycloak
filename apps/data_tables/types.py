from typing import List

import strawberry.django
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


@strawberry.django.type(models.DataRow)
class DataRowType:
    id: auto
    table: DataTableType
    classification: ClassificationType
    access_attributes: List[AccessAttributeType] = strawberry.django.field()


@strawberry.django.type(models.DataColumn)
class DataColumnType:
    id: auto
    table: DataTableType
    name: auto
    classification: ClassificationType
    access_attributes: List[AccessAttributeType] = strawberry.django.field()


@strawberry.django.type(models.DataCell)
class DataCellType:
    id: auto
    row: DataRowType
    column: DataColumnType
    data: auto
    classification: ClassificationType
    access_attributes: List[AccessAttributeType] = strawberry.django.field()
