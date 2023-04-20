from django.contrib import admin

from apps.documents.models import Classification, Document, Portion


class PortionInline(admin.StackedInline):
    model = Portion
    extra = 0


@admin.register(Classification)
class ClassificationAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at", "updated_at")
    search_fields = ("name",)


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ("title", "classification", "created_at", "updated_at")
    search_fields = ("name",)
    inlines = [PortionInline]
