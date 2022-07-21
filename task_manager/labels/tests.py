from django.test import TestCase
from django.urls import reverse

from task_manager.statuses.models import Status
from task_manager.tasks.models import Task
from task_manager.users.models import User
from .models import Label
from .translations import (
    LABEL_CREATED, LABEL_CHANGED, LABEL_IN_USE, LABEL_DELETED)

STATUS_200 = 200
LABELS_LIST = "labels:labels_list"
LABELS = 'labels'
NAME = 'name'
LABELS_PATH = '/labels/'


class TestLabels(TestCase):
    fixtures = ["labels.json", "tasks.json", "users.json", "statuses.json"]

    def setUp(self):
        self.label1 = Label.objects.get(pk=1)
        self.label2 = Label.objects.get(pk=2)
        self.status1 = Status.objects.get(pk=1)
        self.task1 = Task.objects.get(pk=1)
        self.user1 = User.objects.get(pk=1)

    def test_labels_list(self):
        self.client.force_login(self.user1)
        response = self.client.get(reverse(LABELS_LIST))
        labels_list = list(response.context[LABELS])

        self.assertEqual(response.status_code, STATUS_200)
        self.assertQuerysetEqual(
            labels_list,
            [
                self.label1,
                self.label2,
            ],
        )

    def test_create_label(self):
        self.client.force_login(self.user1)
        label = {NAME: "label3"}
        response = self.client.post(
            reverse("labels:create"), label, follow=True)
        created_label = Label.objects.get(name=label[NAME])

        self.assertRedirects(response, LABELS_PATH)
        self.assertContains(response, LABEL_CREATED)
        self.assertEquals(created_label.name, "label3")

    def test_change_label(self):
        self.client.force_login(self.user1)
        url = reverse("labels:change", args=(self.label1.pk,))
        new_label = {NAME: "changed"}
        response = self.client.post(url, new_label, follow=True)

        self.assertRedirects(response, LABELS_PATH)
        self.assertContains(response, LABEL_CHANGED)
        self.assertEqual(Label.objects.get(pk=self.label1.id), self.label1)

    def test_delete_label(self):
        self.client.force_login(self.user1)
        Task.objects.all().delete()
        url = reverse("labels:delete", args=(self.label1.pk,))
        response = self.client.post(url, follow=True)

        with self.assertRaises(Label.DoesNotExist):
            Label.objects.get(pk=self.label1.pk)
        self.assertRedirects(response, LABELS_PATH)
        self.assertContains(response, LABEL_DELETED)

    def test_label_with_tasks_delete(self):
        self.client.force_login(self.user1)
        url = reverse("labels:delete", args=(self.label1.pk,))
        response = self.client.post(url, follow=True)

        self.assertTrue(Label.objects.filter(pk=self.label1.id).exists())
        self.assertRedirects(response, LABELS_PATH)
        self.assertContains(response, LABEL_IN_USE)
