from typing import List

import strawberry.django
from django.db.models import Q

from apps.data_tables.models import DataCell, DataColumn, DataRow, DataTable
from apps.data_tables.types import DataCellType


@strawberry.type
class Query:
    @strawberry.field
    def search(self, info, search_term: str) -> List[DataCellType]:
        user = info.context.request.user

        # Filter based on user's clearance level and access attributes
        clearance_level = user.clearance.level if user.clearance else 0
        user_attributes = user.access_attributes.all()

        accessible_tables = DataTable.objects.filter(
            Q(classification__level__lte=clearance_level),
            Q(access_attributes__isnull=True) | Q(access_attributes__in=user_attributes),
        ).distinct()

        accessible_rows = DataRow.objects.filter(
            Q(classification__level__lte=clearance_level) | Q(classification__isnull=True),
            Q(access_attributes__isnull=True) | Q(access_attributes__in=user_attributes),
            table__in=accessible_tables,
        ).distinct()

        accessible_columns = DataColumn.objects.filter(
            Q(classification__level__lte=clearance_level) | Q(classification__isnull=True),
            Q(access_attributes__isnull=True) | Q(access_attributes__in=user_attributes),
            table__in=accessible_tables,
        ).distinct()

        # Perform search based on the search_term
        search_results = DataCell.objects.filter(
            Q(data__icontains=search_term),
            Q(classification__level__lte=clearance_level) | Q(classification__isnull=True),
            Q(access_attributes__isnull=True) | Q(access_attributes__in=user_attributes),
            row__in=accessible_rows,
            column__in=accessible_columns,
        )

        return search_results


schema = strawberry.Schema(query=Query)
