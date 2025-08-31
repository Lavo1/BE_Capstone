from django.test import TestCase
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from accounts.models import CustomUser
from .models import Case, TimeEntry, Invoice

# -------------------------------
# Model Tests
# -------------------------------
class InvoiceModelTest(TestCase):
    def setUp(self):
        self.partner = CustomUser.objects.create_user(username='partner1', password='pass123', role='Partner')
        self.case = Case.objects.create(
            case_title='Case B',
            client_name='Client B',
            assigned_to=self.partner,
            status='Open',
            deadline='2025-10-15'
        )
        self.time_entry1 = TimeEntry.objects.create(user=self.partner, case=self.case, hours_worked=2)
        self.time_entry2 = TimeEntry.objects.create(user=self.partner, case=self.case, hours_worked=3)

    def test_invoice_total_calculation(self):
        invoice = Invoice.objects.create(case=self.case, due_date='2025-10-30')
        invoice.save()  # triggers save() method
        self.assertEqual(invoice.total_amount, 5 * 500)  # 5 hours * 500 rate


# -------------------------------
# Permission Tests
# -------------------------------
class TimeEntryPermissionTest(APITestCase):
    def setUp(self):
        # Users
        self.partner = CustomUser.objects.create_user(username='partner1', password='pass123', role='Partner')
        self.secretary = CustomUser.objects.create_user(username='secretary1', password='pass123', role='Secretary')
        self.other_secretary = CustomUser.objects.create_user(username='secretary2', password='pass123', role='Secretary')

        # Case and time entry
        self.case = Case.objects.create(case_title='Case A', client_name='Client A', assigned_to=self.partner, status='Open', deadline='2025-09-30')
        self.time_entry = TimeEntry.objects.create(user=self.secretary, case=self.case, hours_worked=2)

        self.client = APIClient()

    def test_secretary_cannot_edit_others_entry(self):
        self.client.force_authenticate(user=self.other_secretary)
        url = reverse('time-entries-detail', kwargs={'pk': self.time_entry.id})
        response = self.client.put(url, {'hours_worked': 5, 'case': self.case.id, 'user': self.secretary.id, 'description': 'Test'})
        self.assertEqual(response.status_code, 403)

    def test_secretary_can_edit_own_entry(self):
        self.client.force_authenticate(user=self.secretary)
        url = reverse('time-entries-detail', kwargs={'pk': self.time_entry.id})
        response = self.client.put(url, {'hours_worked': 4, 'case': self.case.id, 'user': self.secretary.id, 'description': 'Updated'})
        self.assertEqual(response.status_code, 200)
        self.time_entry.refresh_from_db()
        self.assertEqual(self.time_entry.hours_worked, 4)


# -------------------------------
# API Endpoint Tests
# -------------------------------
class CaseAPITest(APITestCase):
    def setUp(self):
        self.partner = CustomUser.objects.create_user(username='partner1', password='pass123', role='Partner')
        self.secretary = CustomUser.objects.create_user(username='secretary1', password='pass123', role='Secretary')

        self.client.force_authenticate(user=self.partner)
        self.case = Case.objects.create(case_title='Case C', client_name='Client C', assigned_to=self.partner, status='Open', deadline='2025-10-31')

    def test_partner_can_update_case(self):
        url = reverse('cases-detail', kwargs={'pk': self.case.id})
        data = {
            'case_title': 'Updated Case',
            'client_name': 'Client C',
            'assigned_to': self.partner.id,
            'status': 'Closed',
            'deadline': '2025-10-31'
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, 200)
        self.case.refresh_from_db()
        self.assertEqual(self.case.status, 'Closed')

    def test_get_cases_list(self):
        url = reverse('cases-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
