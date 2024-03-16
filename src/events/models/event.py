from django.contrib.auth.models import User
from django.db import models


class Event(models.Model):
    class Status(models.TextChoices):
        PUBLISHED = 'PUBLISHED', 'Published'
        HIDDEN = 'HIDDEN', 'Hidden'

    title = models.CharField('title', max_length=255, null=False, blank=False)
    organizer = models.ForeignKey(
        User,
        verbose_name='organizer',
        null=True,
        blank=False,
        on_delete=models.PROTECT,
        db_index=True,
    )
    status = models.CharField(
        'status',
        max_length=9,
        null=False,
        blank=False,
        choices=Status.choices,
        default=Status.PUBLISHED,
    )
    place = models.CharField('place', max_length=255, null=False, blank=False)
    timestamp = models.DateTimeField('timestamp', null=False, blank=False)
    description = models.TextField('description', null=False, blank=True, default='')

    attendees = models.ManyToManyField(User, related_name='events', blank=True)

    created_at = models.DateTimeField('created_at', blank=True, null=True, auto_now_add=True)
    updated_at = models.DateTimeField('updated_at', blank=True, null=True, auto_now=True)

    def __str__(self) -> str:
        return f'{self.title}'

    class Meta:
        ordering = ('-timestamp', )
