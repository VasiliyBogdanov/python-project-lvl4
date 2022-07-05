from django.test import TestCase
from .models import Task
from users.models import User
from statuses.models import Status
from django.urls import reverse
from .translations import (TASK_CREATED, TASK_UPDATED, TASK_DELETED, BY_AUTHOR)

NAME = 'name'
DESCRIPTION = 'description'
STATUS = 'status'
AUTHOR = 'author'
EXECUTOR = 'executor'
TASKS_LIST = 'tasks:tasks_list'
STATUS_200 = 200
TASKS_PATH = '/tasks/'


class TestTasks(TestCase):
    fixtures = ["tasks.json", "statuses.json", "users.json"]

    def setUp(self):
        self.task1 = Task.objects.get(pk=1)
        self.task2 = Task.objects.get(pk=2)

        self.user1 = User.objects.get(pk=1)
        self.user2 = User.objects.get(pk=2)

        self.status1 = Status.objects.get(pk=1)
        self.status2 = Status.objects.get(pk=2)
        self.task = {
            NAME: "task3",
            DESCRIPTION: "description3",
            STATUS: 1,
            AUTHOR: 1,
            EXECUTOR: 2
        }

    def test_tasks_list(self):
        self.client.force_login(self.user1)
        response = self.client.get(reverse(TASKS_LIST))
        tasks_list = list(response.context['tasks'])

        self.assertEqual(response.status_code, STATUS_200)
        self.assertQuerysetEqual(tasks_list, [self.task1, self.task2])

    def test_create_task(self):
        self.client.force_login(self.user1)
        response = self.client.post(
            reverse('tasks:create'),
            self.task,
            follow=True,
        )
        created_task = Task.objects.get(name=self.task[NAME])

        self.assertRedirects(response, TASKS_PATH)
        self.assertContains(response, TASK_CREATED)
        self.assertEquals(created_task.name, "task3")

    def test_update_task(self):
        self.client.force_login(self.user1)
        url = reverse('tasks:update', args=(self.task1.pk,))
        changed_task = {
            NAME: "changed name",
            DESCRIPTION: "changed description",
            STATUS: 1,
            AUTHOR: 1,
            EXECUTOR: 2,
        }
        response = self.client.post(url, changed_task, follow=True)
        self.assertRedirects(response, TASKS_PATH)
        self.assertContains(response, TASK_UPDATED)
        self.assertEqual(Task.objects.get(pk=self.task1.pk), self.task1)

    def test_delete_task(self):
        self.client.force_login(self.user1)
        url = reverse('tasks:delete', args=(self.task1.pk,))
        response = self.client.post(url, follow=True)

        with self.assertRaises(Task.DoesNotExist):
            Task.objects.get(pk=self.task1.pk)
        self.assertRedirects(response, TASKS_PATH)
        self.assertContains(response, TASK_DELETED)

    def test_delete_task_by_another_user(self):
        self.client.force_login(self.user1)
        url = reverse('tasks:delete', args=(self.task2.pk,))
        response = self.client.post(url, follow=True)
        self.assertTrue(Task.objects.filter(pk=self.task2.pk).exists())
        self.assertRedirects(response, TASKS_PATH)
        self.assertContains(response, BY_AUTHOR)
