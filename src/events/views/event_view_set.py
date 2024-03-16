from django.db.models import QuerySet
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, OpenApiResponse, extend_schema
from rest_framework import mixins, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
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
        queryset = Event.objects.all()
        current_user = self.request.user

        only_mine_param = self.request.query_params.get('only_mine', None)
        if only_mine_param == 'true':
            queryset = queryset.filter(organizer=current_user)

        return queryset

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='only_mine',
                description='Filter only events I organized',
                required=False,
                location=OpenApiParameter.QUERY,
                type=OpenApiTypes.BOOL,
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        """
        Method provides same functionality as inherited.
        Only purpose is to extend the schema of API document.
        """
        return super().list(request, *args, **kwargs)

    @extend_schema(
        request={},
        responses={
            204: OpenApiResponse(description='Successfully registered'),
        },
    )
    @action(detail=True, methods=['post'])
    def register(self, request, pk=None):
        event = self.get_object()
        current_user = request.user

        if current_user not in event.attendees.all():
            event.attendees.add(current_user)

        return Response(status=204)
