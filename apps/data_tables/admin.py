from django.contrib import admin

from apps.data_tables.models import (
    AccessAttribute,
    Classification,
    DataCell,
    DataColumn,
    DataRow,
    DataTable,
)


@admin.register(Classification)
class ClassificationAdmin(admin.ModelAdmin):
    list_display = ("name", "level")
    search_fields = ("name",)


@admin.register(AccessAttribute)
class AccessAttributeAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(DataTable)
class DataTableAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    filter_horizontal = ("access_attributes",)


@admin.register(DataRow)
class DataRowAdmin(admin.ModelAdmin):
    list_display = ("id", "table")
    search_fields = ("table__name",)
    list_filter = ("table",)
    filter_horizontal = ("access_attributes",)


@admin.register(DataColumn)
class DataColumnAdmin(admin.ModelAdmin):
    list_display = ("name", "table")
    search_fields = ("name", "table__name")
    list_filter = ("table",)
    filter_horizontal = ("access_attributes",)


@admin.register(DataCell)
class DataCellAdmin(admin.ModelAdmin):
    list_display = ("id", "row", "column", "data")
    search_fields = ("data", "row__id", "column__name")
    list_filter = ("row__table", "column__table")
    filter_horizontal = ("access_attributes",)


# class PortionInline(admin.StackedInline):
#     model = Portion
#     extra = 0


# @admin.register(Classification)
# class ClassificationAdmin(admin.ModelAdmin):
#     list_display = ("name", "created_at", "updated_at")
#     search_fields = ("name",)


# @admin.register(Document)
# class DocumentAdmin(admin.ModelAdmin):
#     list_display = ("title", "classification", "created_at", "updated_at")
#     search_fields = ("name",)
#     inlines = [PortionInline]
