from django.test import TestCase
from .models import Employee, Department
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth.models import User

class BasicApiTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('test','t@example.com','pwd')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        d = Department.objects.create(name='Eng')
        Employee.objects.create(first_name='A', last_name='B', email='a@b.com', department=d, hire_date='2020-01-01', salary=50000)

    def test_employees_list(self):
        resp = self.client.get('/api/employees/')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('results' in resp.data)
