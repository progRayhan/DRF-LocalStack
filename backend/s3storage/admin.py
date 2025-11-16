from django.contrib import admin
from .models import Document


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ("original_name", "file_size", "content_type", "created_at")
    list_filter = ("content_type", "created_at")
    search_fields = ("original_name",)
    
    readonly_fields = ("original_name", "file_size", "content_type", "created_at")

    fieldsets = (
        ("File", {
            "fields": ("file",)
        }),
        ("Metadata", {
            "fields": ("original_name", "file_size", "content_type")
        }),
        ("Timestamps", {
            "fields": ("created_at",)
        }),
    )
