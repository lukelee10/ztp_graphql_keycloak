import logging
from typing import List

import strawberry.django
from django.db.models import Count, F, Q

from apps.data_tables.models import DataCell, DataColumn, DataRow, DataTable
from apps.data_tables.types import DataCellType, DataRowType, DataTableType
from apps.users.types import UserType
from ztp_browser.utils.ztp_opa_client import OPA

log = logging.getLogger("main")


@strawberry.type
class Query:
    @strawberry.field
    def current_user(self, info) -> UserType:
        return info.context.request.user

    @strawberry.field
    def get_table(self, info, table_id: int) -> DataTableType:
        user = info.context.request.user

        # Filter based on user's clearance level and access attributes
        clearance_level = user.clearance.level if user.clearance else 0
        user_attributes = user.access_attributes.all()

        accessible_tables = (
            DataTable.objects.filter(
                Q(id=table_id),
                Q(classification__level__lte=clearance_level) | Q(classification__isnull=True),
            )
            .annotate(
                num_required_attributes=Count("access_attributes"),
                num_user_attributes=Count("access_attributes", filter=Q(access_attributes__in=user_attributes)),
            )
            .filter(num_required_attributes=F("num_user_attributes"))
            .distinct()
        )

        return accessible_tables.first()

    @strawberry.field
    def search(self, info, search_term: str) -> List[DataCellType]:
        user = info.context.request.user

        # Filter based on user's clearance level and access attributes
        clearance_level = user.clearance.level if user.clearance else 0
        user_attributes = user.access_attributes.all()

        accessible_tables = (
            DataTable.objects.filter(Q(classification__level__lte=clearance_level) | Q(classification__isnull=True))
            .annotate(
                num_required_attributes=Count("access_attributes"),
                num_user_attributes=Count("access_attributes", filter=Q(access_attributes__in=user_attributes)),
            )
            .filter(num_required_attributes=F("num_user_attributes"))
            .distinct()
        )

        accessible_rows = (
            DataRow.objects.filter(
                Q(classification__level__lte=clearance_level) | Q(classification__isnull=True),
                table__in=accessible_tables,
            )
            .annotate(
                num_required_attributes=Count("access_attributes"),
                num_user_attributes=Count("access_attributes", filter=Q(access_attributes__in=user_attributes)),
            )
            .filter(num_required_attributes=F("num_user_attributes"))
            .distinct()
        )

        accessible_columns = (
            DataColumn.objects.filter(
                Q(classification__level__lte=clearance_level) | Q(classification__isnull=True),
                table__in=accessible_tables,
            )
            .annotate(
                num_required_attributes=Count("access_attributes"),
                num_user_attributes=Count("access_attributes", filter=Q(access_attributes__in=user_attributes)),
            )
            .filter(num_required_attributes=F("num_user_attributes"))
            .distinct()
        )

        search_results = (
            DataCell.objects.filter(
                Q(data__icontains=search_term),
                Q(classification__level__lte=clearance_level) | Q(classification__isnull=True),
                row__in=accessible_rows,
                column__in=accessible_columns,
            )
            .annotate(
                num_required_attributes=Count("access_attributes"),
                num_user_attributes=Count("access_attributes", filter=Q(access_attributes__in=user_attributes)),
            )
            .filter(num_required_attributes=F("num_user_attributes"))
        ).distinct()
        return search_results

    @strawberry.field
    def search_opa(self, info, search_term: str) -> List[DataCellType]:
        user = info.context.request.user
        client = OPA()

        # validate user can even access data
        if not client.verify_user_clearance(user.clearance):
            log.critical(
                "Access Denied. Unathorized user attempted to access data. User:{} Clearance:{}".format(
                    user, user.clearance
                )
            )
            # TODO return no data
            return None

        # Filter based on user's clearance level and access attributes
        clearance_level = (
            user.clearance.level if user.clearance else 0
        )  # TODO see why level is 1 level lower than doc class
        user_attributes = user.access_attributes.all()

        accessible_tables = (
            DataTable.objects.filter(Q(classification__level__lte=clearance_level) | Q(classification__isnull=True))
            .annotate(
                num_required_attributes=Count("access_attributes"),
                num_user_attributes=Count("access_attributes", filter=Q(access_attributes__in=user_attributes)),
            )
            .filter(num_required_attributes=F("num_user_attributes"))
            .distinct()
        )

        # table classification verification
        if not (
            client.user_doc_auth(user.clearance, accessible_tables.values_list("classification__level", flat=True))
        ):
            log.critical(
                "Clearance Level Access Denied. User attempted to access data above clearance level. UserID:{} Clearance Level:{} Document Levels: {}".format(
                    user.id,
                    user.clearance.level,
                    list(accessible_tables.values_list("classification__level", flat=True)),
                )
            )
            return None  # maybe send to queue for human review
        # table attr verification
        if not (client.verify_attribute_access(user, accessible_tables.values_list("access_attributes", flat=True))):
            log.critical(
                "Attribute Access Denied. UserID {} with attributes {} not authorized access to document(s) ID(s): {}".format(
                    user.id,
                    list(user_attributes.values_list("name", flat=True)),
                    list(accessible_tables.values_list(flat=True)),
                )
            )
            return None  # maybe send to queue for human review

        accessible_rows = (
            DataRow.objects.filter(
                Q(classification__level__lte=clearance_level) | Q(classification__isnull=True),
                table__in=accessible_tables,
            )
            .annotate(
                num_required_attributes=Count("access_attributes"),
                num_user_attributes=Count("access_attributes", filter=Q(access_attributes__in=user_attributes)),
            )
            .filter(num_required_attributes=F("num_user_attributes"))
            .distinct()
        )

        # row class verification
        if not (client.user_doc_auth(user.clearance, accessible_rows.values_list("classification__level", flat=True))):
            log.critical(
                "Clearance Level Access Denied. User attempted to access data above clearance level. UserID:{} Clearance Level:{} Document Levels: {}".format(
                    user.id, user.clearance.level, list(accessible_rows.values_list("classification__level", flat=True))
                )
            )
            return None  # maybe send to queue for human review

        # row attr verification
        if not (client.verify_attribute_access(user, accessible_rows.values_list("access_attributes", flat=True))):
            log.critical(
                "Attribute Access Denied. UserID {} with attributes {} not authorized access to document attributes {}".format(
                    user.id,
                    list(user_attributes.values_list("id", flat=True)),
                    list(accessible_rows.values_list("access_attributes", flat=True)),
                )
            )
            return None

        accessible_columns = (
            DataColumn.objects.filter(
                Q(classification__level__lte=clearance_level) | Q(classification__isnull=True),
                table__in=accessible_tables,
            )
            .annotate(
                num_required_attributes=Count("access_attributes"),
                num_user_attributes=Count("access_attributes", filter=Q(access_attributes__in=user_attributes)),
            )
            .filter(num_required_attributes=F("num_user_attributes"))
            .distinct()
        )

        # column classification verification
        if not (
            client.user_doc_auth(user.clearance, accessible_columns.values_list("classification__level", flat=True))
        ):
            log.critical(
                "Clearance Level Access Denied. User attempted to access data above clearance level. UserID:{} Clearance Level:{} Document Levels: {}".format(
                    user.id,
                    user.clearance.level,
                    list(accessible_columns.values_list("classification__level", flat=True)),
                )
            )
            return None  # maybe send to queue for human review
        # column attr verification
        # column attr verification
        if not (client.verify_attribute_access(user, accessible_columns.values_list("access_attributes", flat=True))):
            log.critical(
                "Attribute Access Denied. UserID {} with attributes {} not authorized access to document(s) ID(s): {} attributes: {}".format(
                    user.id,
                    list(user_attributes.values_list("name", flat=True)),
                    list(accessible_columns.values_list(flat=True)),
                    list(accessible_columns.values_list("access_attributes", flat=True)),
                )
            )
            return None

        search_results = (
            DataCell.objects.filter(
                Q(data__icontains=search_term),
                Q(classification__level__lte=clearance_level) | Q(classification__isnull=True),
                row__in=accessible_rows,
                column__in=accessible_columns,
            )
            .annotate(
                num_required_attributes=Count("access_attributes"),
                num_user_attributes=Count("access_attributes", filter=Q(access_attributes__in=user_attributes)),
            )
            .filter(num_required_attributes=F("num_user_attributes"))
        ).distinct()

        if not (client.user_doc_auth(user.clearance, search_results.values_list("classification__level", flat=True))):
            log.critical(
                "Clearance Level Access Denied. User attempted to access data above clearance level. UserID:{} Clearance Level:{} Document Levels: {}".format(
                    user.id, user.clearance.level, list(search_results.values_list("classification__level", flat=True))
                )
            )
            return None  # maybe send to queue for human review

        log.debug("CELL Attributes {}".format(search_results.values_list("access_attributes", flat=True)))

        if not (client.verify_attribute_access(user, search_results.values_list("access_attributes", flat=True))):
            log.critical(
                "Attribute Access Denied. UserID {} with attributes {} not authorized access to document(s) ID(s): {}".format(
                    user.id,
                    list(user_attributes.values_list("name", flat=True)),
                    list(search_results.values_list(flat=True)),
                )
            )
            return None  # maybe send to queue for human review
        json_user = {
            "name": user.username,
            "clearance": user.clearance.name,
            "attributes": list(user_attributes.values_list("name", flat=True)),
            "cells": [
                f"CELL(row={cell.row.id},column='{cell.column.name}',table='{cell.row.table.name}')"
                for cell in search_results
            ],
            "access_granted": True,
        }
        import json

        log.info(
            json.dumps(json_user)
            # "UserID %s granted access to the following cells: %s", user.name, search_results.values_list("id", flat=True)
        )

        return search_results


schema = strawberry.Schema(query=Query)
