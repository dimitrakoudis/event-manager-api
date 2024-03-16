from django.db.models import QuerySet
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, OpenApiResponse, extend_schema
from rest_framework import mixins, permissions
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from events.models import Event
from events.serializers import EventSerializer


def _validate_event_generic_action(event: Event) -> None:
    """
     Throws DRF validation error in case the event:
        - is past
        - is not published
    """

    if event.timestamp < timezone.now():
        raise ValidationError({'detail': 'ACTION_NOT_ALLOWED_ON_PAST_EVENT'})

    if event.status != Event.Status.PUBLISHED:
        raise ValidationError({'detail': 'ACTION_NOT_ALLOWED_ON_NON_PUBLISHED_EVENT'})


class EventResultsPagination(PageNumberPagination):
    """
    Custom pagination class to be used in Events View set
    """

    page_size = 25
    max_page_size = 100
    page_size_query_param = 'page_size'


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

    pagination_class = EventResultsPagination
    filter_backends = (
        DjangoFilterBackend,
        OrderingFilter,
        SearchFilter,
    )
    ordering_fields = '__all__'
    ordering = ('-timestamp', )

    search_fields = (
        'place',
        'title',
        'description',
    )
    filterset_fields = {
        'status': ('exact', ),
        'organizer': ('exact', ),
        'timestamp': ('exact', 'gte', 'lte', ),
    }

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

        only_future_param = self.request.query_params.get('only_future', None)
        only_past_param = self.request.query_params.get('only_past', None)
        if only_future_param == 'true':
            queryset = queryset.filter(timestamp__gt=timezone.now())
        elif only_past_param == 'true':
            queryset = queryset.filter(timestamp__lte=timezone.now())

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
            OpenApiParameter(
                name='only_future',
                description='Filter only future events (overrides only_past query param)',
                required=False,
                location=OpenApiParameter.QUERY,
                type=OpenApiTypes.BOOL,
            ),
            OpenApiParameter(
                name='only_past',
                description='Filter only past events',
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
        """
        Custom action to register user to event.
        Raises Http Error (400) when:
            - Event timestamp is past
            - Event is not in published status
            - User is already registered to the event
            - Event is full of attendees
        """

        event = self.get_object()
        current_user = request.user

        _validate_event_generic_action(event)

        if current_user in event.attendees.all():
            raise ValidationError({'detail': 'WAS_ALREADY_REGISTERED_TO_THIS_EVENT'})

        if event.capacity and event.attendees_count >= event.capacity:
            raise ValidationError({'detail': 'EVENT_IS_FULL'})

        event.attendees.add(current_user)
        return Response(status=204)

    @extend_schema(
        request={},
        responses={
            204: OpenApiResponse(description='Successfully un-registered'),
        },
    )
    @action(detail=True, url_path='un-register', methods=['post'])
    def un_register(self, request, pk=None):
        """
        Custom action to un-register user to event.
        Raises Http Error (400) when:
            - Event timestamp is past
            - Event is not in published status
            - User was not registered to the event
        """

        event = self.get_object()
        current_user = request.user

        _validate_event_generic_action(event)

        if current_user not in event.attendees.all():
            raise ValidationError({'detail': 'WAS_NOT_REGISTERED_TO_THIS_EVENT'})

        event.attendees.remove(current_user)
        return Response(status=204)
