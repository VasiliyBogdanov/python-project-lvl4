from django.db import models
from task_manager.users.models import User
from task_manager.statuses.models import Status
from task_manager.labels.models import Label

TASKS_NAME = 'tasks'
ID = 'id'
NAME = 'name'


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
    labels = models.ManyToManyField(Label, related_name='tasks', blank=True)

    def __str__(self):
        return self.name
