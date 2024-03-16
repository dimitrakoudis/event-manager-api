from django.db import models


class Category(models.Model):
    name = models.CharField('title', max_length=255, null=False, blank=False)

    created_at = models.DateTimeField('created_at', blank=True, null=True, auto_now_add=True)
    updated_at = models.DateTimeField('updated_at', blank=True, null=True, auto_now=True)

    def __str__(self) -> str:
        return f'{self.name}'

    class Meta:
        ordering = ('-id', )
        verbose_name_plural = 'categories'
