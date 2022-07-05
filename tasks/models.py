from django.db import models
from users.models import User
from statuses.models import Status

TASKS_NAME = 'tasks'


class Task(models.Model):
    name = models.CharField(max_length=200, null=False)
    description = models.TextField(null=False)
    status = models.ForeignKey(
        Status,
        null=True,
        on_delete=models.PROTECT,
        related_name=TASKS_NAME,
    )
    author = models.ForeignKey(
        User,
        null=False,
        on_delete=models.PROTECT,
        related_name=TASKS_NAME,
    )
    executor = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        null=True,
        related_name="objectives",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
