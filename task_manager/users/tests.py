from django.test import TestCase
from django.urls import reverse

from .forms import (USERNAME, FIRST_NAME, LAST_NAME, PASSWORD1, PASSWORD2, )
from .models import User
from .translations import (USER_UPDATED, USER_CREATED, USER_DELETED, )
from .views import (USERS_CONTEXT_NAME, USERS_LIST_NAME, )

USERS_FIXTURE = 'users.json'
STATUS_200 = 200

LOGIN_PATH = '/login/'
USERS_PATH = '/users/'

USERS_CREATE_PATH = 'users:create_user'
USERS_UPDATE_PATH = 'users:update'
USERS_DELETE_PATH = 'users:delete'


class TestUsers(TestCase):
    fixtures = [USERS_FIXTURE]

    def setUp(self):
        self.user1 = User.objects.get(pk=1)
        self.user2 = User.objects.get(pk=2)

    def test_users_list(self):
        response = self.client.get(reverse(USERS_LIST_NAME))
        users_list = list(response.context[USERS_CONTEXT_NAME])
        test_user1, test_user2 = users_list

        self.assertEqual(response.status_code, STATUS_200)
        self.assertEqual(test_user1.username, "User1")
        self.assertEqual(test_user2.first_name, "firstName2")

    def test_user_create(self):
        url = reverse(USERS_CREATE_PATH)
        test_password = "12345678_"
        new_user = {
            USERNAME: "testUser",
            FIRST_NAME: "testFirstName",
            LAST_NAME: "testLastName",
            PASSWORD1: test_password,
            PASSWORD2: test_password,
        }
        response = self.client.post(
            url,
            new_user,
            follow=True,
        )
        created_user = User.objects.get(username=new_user[USERNAME])

        self.assertRedirects(response, LOGIN_PATH)
        self.assertContains(response, USER_CREATED)
        self.assertTrue(created_user.check_password(test_password))

    def test_user_update(self):
        user = self.user1
        self.client.force_login(user)
        url = reverse(USERS_UPDATE_PATH, args=(user.id,))
        test_password = "_87654321"
        new_data = {
            USERNAME: user.username,
            FIRST_NAME: user.first_name,
            LAST_NAME: user.last_name,
            PASSWORD1: test_password,
            PASSWORD2: test_password,
        }
        response = self.client.post(path=url, data=new_data, follow=True)
        changed_user = User.objects.get(username=user.username)

        self.assertRedirects(response, USERS_PATH)
        self.assertContains(response, USER_UPDATED)
        self.assertTrue(changed_user.check_password(test_password))

    def test_user_delete(self):
        user = self.user1
        self.client.force_login(user)
        url = reverse(USERS_DELETE_PATH, args=(user.id,))
        response = self.client.post(url, follow=True)

        with self.assertRaises(User.DoesNotExist):
            User.objects.get(pk=self.user1.id)

        self.assertRedirects(response, USERS_PATH)
        self.assertContains(response, USER_DELETED)
