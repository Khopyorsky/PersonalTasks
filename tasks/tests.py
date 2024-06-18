from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from http import HTTPStatus

from PersonalTasks.settings import env

from .models import Task


class CustomMixin(TestCase):

    def setUp(self):
        print('Starting Test')

    def tearDown(self):
        print('Test Passed')


# Create your tests here.
class GetPagesWithoutUserTestCase(CustomMixin):

    def test_redirect_from_index(self):
        path = reverse('tasks:tasks')
        response = self.client.get(path)
        redirect_uri = reverse('users:login') + '?next=' + path
        # тест открывает главную страницу без пользователя, поэтому перенаправляется на страничку авторизации
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertIn('users/login', response.url)
        self.assertRedirects(response, redirect_uri)


class GetPagesTestCase(CustomMixin):
    fixtures = [
        'db.json'
    ]

    def test_index(self):
        path = reverse('tasks:tasks')
        self.client.login(username=env('USER'), password=env('PASSWORD'))
        response = self.client.get(path)
        self.assertEqual(response.status_code, HTTPStatus.OK)


class GetDataTestCase(CustomMixin):
    fixtures = [
        'db.json'
    ]

    def test_users_queryset(self):
        path = reverse('tasks:tasks')
        self.client.login(username=env('USER'), password=env('PASSWORD'))
        response = self.client.get(path)
        user = get_user_model().objects.get(username=env('USER'))
        queryset = Task.objects.filter(performers=user)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertQuerysetEqual(queryset, response.context_data['tasks'])
