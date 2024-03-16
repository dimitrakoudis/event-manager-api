from django.db.models import QuerySet
from rest_framework import mixins, permissions
from rest_framework.viewsets import GenericViewSet

from events.models import Event
from events.serializers import EventSerializer


class IsEventOrganizer(permissions.BasePermission):
    """
    Allows access only to organizer of the event
    """

    def has_object_permission(self, request, view, obj):
        return obj.organizer == request.user


class EventViewSet(mixins.ListModelMixin,
                   mixins.CreateModelMixin,
                   mixins.UpdateModelMixin,
                   GenericViewSet):
    """
    View to list/create/update events
    """

    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = EventSerializer

    def get_permissions(self):
        """
        Overriding pre-defined permissions, only in case of update,
        where the requester user should be the event's organizer.
        """

        if self.action == 'update':
            return [*super().get_permissions(), IsEventOrganizer(), ]
        return super().get_permissions()

    def get_queryset(self) -> QuerySet[Event]:
        return Event.objects.all()
