from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from http import HTTPStatus
from PersonalTasks.settings import env


class RegisterAuthenticationTestCase(TestCase):
    fixtures = [
        'db.json'
    ]

    def setUp(self):
        print('Test Started')

    def tearDown(self):
        print('Test Passed')

    def test_get_register_form(self):
        path = reverse('users:signup')
        response = self.client.get(path)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'users/sign_up.html')

    def test_user_has_registered(self):

        data = {
            'username': 'Oleg1990',
            'first_name': 'Oleg',
            'last_name': 'Vorobiev',
            'email': 'oleg_vorobiev@mail.ru',
            'password1': env('PASSWORD'),
            'password2': env('PASSWORD')
        }

        path = reverse('users:signup')
        response = self.client.post(path, data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('users:login'))
        self.assertTrue(get_user_model().objects.filter(username=data['username']).exists())
