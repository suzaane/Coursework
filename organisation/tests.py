from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Department, DepartmentLeader, TeamType

class DepartmentModelTest(TestCase):
    def setUp(self):
        self.dept = Department.objects.create(
            name='xTV Web', specialisation='Web streaming'
        )

    def test_department_created(self):
        self.assertEqual(Department.objects.count(), 1)

    def test_str_returns_name(self):
        self.assertEqual(str(self.dept), 'xTV Web')


class DepartmentViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='pass1234')
        self.client.login(username='testuser', password='pass1234')
        self.dept = Department.objects.create(name='Mobile', specialisation='Mobile apps')

    def test_department_list_loads(self):
        response = self.client.get(reverse('organisation:department_list'))
        self.assertEqual(response.status_code, 200)

    def test_department_detail_loads(self):
        response = self.client.get(
            reverse('organisation:department_detail', args=[self.dept.pk])
        )
        self.assertEqual(response.status_code, 200)

    def test_search_filters_results(self):
        response = self.client.get(
            reverse('organisation:department_list') + '?q=Mobile'
        )
        self.assertContains(response, 'Mobile')

    def test_unauthenticated_redirects(self):
        self.client.logout()
        response = self.client.get(reverse('organisation:department_list'))
        self.assertEqual(response.status_code, 302)
    
    def test_org_chart_loads(self):
        response = self.client.get(reverse('organisation:org_chart'))
        self.assertEqual(response.status_code, 200)
    
    def test_teamtype_list_loads(self):
        response = self.client.get(reverse('organisation:teamtype_list'))
        self.assertEqual(response.status_code, 200)
    
    def test_dependency_list_loads(self):
        response = self.client.get(reverse('organisation:dependency_list'))
        self.assertEqual(response.status_code, 200)


class TeamTypeTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='pass1234')
        self.client.login(username='testuser', password='pass1234')
        self.teamtype = TeamType.objects.create(name='Platform', description='Platform team')
    
    def test_teamtype_created(self):
        self.assertEqual(TeamType.objects.count(), 1)
    
    def test_teamtype_list_shows_type(self):
        response = self.client.get(reverse('organisation:teamtype_list'))
        self.assertContains(response, 'Platform')