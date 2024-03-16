from rest_framework import serializers

from events.models import Event


class EventSerializer(serializers.ModelSerializer):
    """
    Main model serializer for events
    """

    class Meta:
        model = Event
        fields = '__all__'
        read_only_fields = (
            'id',
            'organizer',
            'attendees',
            'created_at',
            'updated_at',
        )
