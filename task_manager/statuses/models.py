from django.db import models

from .translations import STATUSES_TITLE


class Status(models.Model):
    name = models.CharField(max_length=255, null=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = STATUSES_TITLE
