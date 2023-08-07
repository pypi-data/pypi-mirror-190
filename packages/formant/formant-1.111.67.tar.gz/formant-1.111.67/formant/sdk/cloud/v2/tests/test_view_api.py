import unittest
from formant.sdk.cloud.v2.src.admin_api import AdminAPI
from formant.sdk.cloud.v2.formant_admin_api_client.models import PartialView
import os

EMAIL = os.getenv("FORMANT_EMAIL")
PASSWORD = os.getenv("FORMANT_PASSWORD")
ADMIN_API_URL = "https://api.formant.io/v1/admin"


class TestViews(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestViews, self).__init__(*args, **kwargs)
        self.client = AdminAPI(email=EMAIL, password=PASSWORD, api_url=ADMIN_API_URL)

    def test_get(self):
        device_id = "88d977e4-65c0-4e2f-8657-91a2863407f3"
        result = self.client.views.get(device_id)
        self.assertEqual(result.status_code, 200)

    def test_get_all(self):
        result = self.client.views.get_all()
        self.assertEqual(result.status_code, 200)

    def test_patch(self):
        device_id = "88d977e4-65c0-4e2f-8657-91a2863407f3"
        partial_view = PartialView(organization_id=self.client.organization_id)
        result = self.client.views.patch(device_id, partial_view)
        self.assertEqual(result.status_code, 200)


unittest.main()
