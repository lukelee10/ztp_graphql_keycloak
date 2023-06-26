from django.contrib import admin
from django.contrib.admin.options import InlineModelAdmin, TabularInline
from django.contrib.admin.utils import quote
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.html import format_html

from apps.data_tables.models import (
    AccessAttribute,
    Classification,
    DataCell,
    DataColumn,
    DataRow,
    DataTable,
    DataContent,
)


class TableInline(admin.StackedInline):
    model = DataRow
    extra = 0


@admin.register(Classification)
class ClassificationAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "level")
    search_fields = ("name",)


@admin.register(AccessAttribute)
class AccessAttributeAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
    )
    search_fields = ("name",)


@admin.register(DataTable)
class DataTableAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "classification",
        "name",
    )
    search_fields = ("name",)
    filter_horizontal = ("access_attributes",)

    def get_add_row_url(self, obj):
        return reverse("admin:data_tables_datarow_add") + f"?table={obj.pk}"

    def get_add_column_url(self, obj):
        return reverse("admin:data_tables_datacolumn_add") + f"?table={obj.pk}"

    def get_fieldsets(self, request, obj=None):
        if obj:
            fieldsets = self.fieldsets
            add_row_url = self.get_add_row_url(obj)
            add_column_url = self.get_add_column_url(obj)
            fieldsets[1][1]["description"] = fieldsets[1][1]["description"].format(
                add_row_url=add_row_url, add_column_url=add_column_url
            )
        else:
            fieldsets = self.fieldsets[:1]
        return fieldsets

    def table_display(self, obj):
        columns = DataColumn.objects.filter(table=obj)
        rows = DataRow.objects.filter(table=obj)
        table_html = '<table border="1" class="table">'

        # Table Header
        table_html += "<thead><tr><th>Row ID</th>"
        for column in columns:
            column_url = reverse("admin:data_tables_datacolumn_change", args=[quote(column.pk)])
            table_html += f'<th><a href="{column_url}">{column.name}</a></th>'
        table_html += "<th></th></tr></thead>"

        # Table Rows and Cells
        table_html += "<tbody>"
        for row in rows:
            table_html += f"<tr><td>{row.pk}</td>"
            for column in columns:
                cell = DataCell.objects.filter(row=row, column=column).first()
                if cell:
                    cell_url = reverse("admin:data_tables_datacell_change", args=[quote(cell.pk)])
                    table_html += f'<td><a href="{cell_url}">{cell.data}</a></td>'
                else:
                    table_html += "<td>-</td>"
            table_html += "<td></td></tr>"
        table_html += "</tbody>"

        table_html += "</table>"
        return format_html(table_html)

    table_display.short_description = "Table"

    readonly_fields = ("table_display",)

    fieldsets = (
        (None, {"fields": ("classification", "name", "access_attributes")}),
        (
            "Table",
            {
                "fields": ("table_display",),
                "description": (
                    '<input type="button" value="Add Row" onclick="location.href=\'{add_row_url}\';">'
                    '<input type="button" value="Add Column" onclick="location.href=\'{add_column_url}\';">'
                ),
                "classes": ("wide",),
            },
        ),
    )


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
    list_display = ("id", "classification", "row", "column", "data")
    search_fields = ("data", "row__id", "column__name")
    list_filter = ("row__table", "column__table")
    filter_horizontal = ("access_attributes",)


@admin.register(DataContent)
class TypeDataAdmin(admin.ModelAdmin):
    list_display = ("id", "text_data", "bool_data", "image_data", "float_data", "email_data", "url_data", "decimal_data", "int_data", "date_data", "dollar_data")
    search_fields = ("id", "text_data", "bool_data", "image_data", "float_data", "email_data", "url_data", "decimal_data", "int_data", "date_data", "dollar_data",)
