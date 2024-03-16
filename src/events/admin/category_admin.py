from django.contrib import admin

from events.models import Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'created_at',
        'updated_at',
    )
    readonly_fields = (
        'created_at',
        'updated_at',
    )

    search_fields = (
        'name',
    )
    list_filter = (
        'created_at',
        'updated_at',
    )
    sortable_by = (
        'name',
        'created_at',
        'updated_at',
    )
