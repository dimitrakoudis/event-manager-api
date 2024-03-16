from django.db.models import QuerySet
from rest_framework import mixins, permissions
from rest_framework.viewsets import GenericViewSet

from events.models import Event
from events.serializers import EventSerializer


class EventViewSet(mixins.ListModelMixin,
                   mixins.CreateModelMixin,
                   GenericViewSet):
    """
    View to list/create events
    """

    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = EventSerializer

    def get_queryset(self) -> QuerySet[Event]:
        return Event.objects.all()
