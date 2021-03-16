from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse


class TestHealthAlertsSignUpView(TestCase):
    def setUp(self):
        super().setUp()
        self.url = reverse("health_alerts_sign_up")
        self.sign_up_data = {
            "personal_first_name": "SpongeBob",
            "personal_last_name": "SquarePants",
            "personal_medical_expertise": "Sutures",
            "personal_professional_licenses": "1293-3P",
            "agency_name": "The Crabby Patty",
            "agency_type": "Restaurant Health",
            "agency_zip_code": "12340",
            "agency_position": "Manager",
            "agency_work_phone": "(120) 192-1929",
            "network_email": "crabbypatty@gmail.com",
            "network_fax": "(120) 192-1929",
        }
        self.success_msg = (
            (
                "You are now subscribed to receiving Health Alerts "
                "from the Philadelphia Department of Public Health."
            ),
        )

    def test_get_page(self):
        r = self.client.get(self.url)
        self.assertEqual(HTTPStatus.OK, r.status_code)
        self.assertTemplateUsed(r, "health_alerts/health_alert_index_page.html")
        self.assertIn("form", r.context)

    def test_success_msg_shown(self):
        r = self.client.post(self.url, self.sign_up_data)
        self.assertEqual(HTTPStatus.FOUND, r.status_code)
        messages = list(r.context["messages"])
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0], self.success_msg)
