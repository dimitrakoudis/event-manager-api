from django.contrib import admin

from events.models import Event


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'place',
        'timestamp',
        'organizer',
        'status',
        'created_at',
        'updated_at',
    )
    readonly_fields = (
        'created_at',
        'updated_at',
    )

    raw_id_fields = (
        'organizer',
    )
    autocomplete_fields = (
        'attendees',
    )

    search_fields = (
        'title',
        'place',
        'description',
    )
    list_filter = (
        'timestamp',
        'created_at',
        'updated_at',
        'status',
    )
    sortable_by = (
        'timestamp',
        'created_at',
        'updated_at',
    )
