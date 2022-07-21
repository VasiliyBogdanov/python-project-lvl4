from django.test import TestCase
from django.urls import reverse

from task_manager.statuses.models import Status
from task_manager.users.models import User
from .translations import (STATUS_CREATED, STATUS_UPDATED, STATUS_DELETED)
from .views import STATUSES_LIST

STATUS_200 = 200
STATUSES = 'statuses'
NAME = 'name'
STATUSES_PATH = '/statuses/'


class TestStatuses(TestCase):

    fixtures = ["statuses.json", "users.json"]

    def setUp(self):
        self.user = User.objects.get(pk=1)
        self.status1 = Status.objects.get(pk=1)
        self.status2 = Status.objects.get(pk=2)

    def test_statuses_list(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse(STATUSES_LIST))
        statuses_list = list(response.context[STATUSES])

        self.assertEqual(response.status_code, STATUS_200)
        self.assertQuerysetEqual(statuses_list, [self.status1, self.status2])

    def test_create_status(self):
        self.client.force_login(self.user)
        status_name = 'status3'
        status = {NAME: status_name}
        response = self.client.post(
            reverse("statuses:create"),
            status,
            follow=True,
        )

        created_status = Status.objects.get(name=status[NAME])
        self.assertRedirects(response, STATUSES_PATH)
        self.assertContains(response, STATUS_CREATED)
        self.assertEquals(created_status.name, status_name)

    def test_update_status(self):
        self.client.force_login(self.user)
        url = reverse("statuses:update", args=(self.status1.pk,))
        new_status = {NAME: "status4"}
        response = self.client.post(url, new_status, follow=True)

        self.assertRedirects(response, STATUSES_PATH)
        self.assertContains(response, STATUS_UPDATED)
        self.assertEqual(Status.objects.get(pk=self.status1.id), self.status1)

    def test_delete_status(self):
        self.client.force_login(self.user)
        # Delete task, when implemented
        url = reverse("statuses:delete", args=(self.status1.pk,))
        response = self.client.post(url, follow=True)

        with self.assertRaises(Status.DoesNotExist):
            Status.objects.get(pk=self.status1.pk)
        self.assertRedirects(response, STATUSES_PATH)
        self.assertContains(response, STATUS_DELETED)
