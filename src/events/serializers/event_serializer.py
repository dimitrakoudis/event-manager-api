from rest_framework import serializers

from events.models import Event


class EventSerializer(serializers.ModelSerializer):
    """
    Main model serializer for list/create events
    """

    def create(self, validated_data) -> Event:
        """
        Overriding create method, setting requester user as the organizer.
        """

        current_user_id = self.context['request'].user.id
        instance = Event.objects.create(**validated_data, organizer_id=current_user_id)
        return instance

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
