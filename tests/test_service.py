from unittest.mock import patch, MagicMock
from django.test import TestCase, RequestFactory
from myinfo.models import OauthSessionState
from myinfo.services import MyInfoService


class MyInfoServiceTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.request = self.factory.post('/api/persons')
        self.request.session = self.client.session
        self.request.session.save()

        self.session_key = self.request.session.session_key
        self.oauth_state = OauthSessionState.objects.create(
            session_id=self.session_key, key="test_key"
        )

        self.service = MyInfoService(self.request)

    @patch.object(MyInfoService, "get_callback_url", return_value="https://example.com/callback")
    def test_get_callback_url(self, mock_callback_url):
        """Test get_callback_url() returns the correct URL."""
        self.assertEqual(self.service.get_callback_url(),
                         "https://example.com/callback")

    @patch("myinfo.utils.client.MyInfoPersonalClientV4.retrieve_resource", return_value={"name": "John Doe"})
    def test_get_person_data_success(self, mock_retrieve_resource):
        """Test that get_person_data returns the correct response without making an external API call."""
        data, error_msg, status_code = self.service.get_person_data(
            auth_code="valid_code")

        self.assertEqual(data, {"name": "John Doe"})
        self.assertIsNone(error_msg)
        self.assertEqual(status_code, 200)

        # Ensure retrieve_resource was called once
        mock_retrieve_resource.assert_called_once()

    @patch("myinfo.utils.client.MyInfoPersonalClientV4.retrieve_resource", side_effect=Exception("Invalid code"))
    def test_get_person_data_invalid_code(self, mock_retrieve_resource):
        """Test handling of an invalid auth_code, ensuring no external call happens."""
        data, error_msg, status_code = self.service.get_person_data(
            auth_code="invalid_code")

        self.assertIsNone(data)
        self.assertEqual(error_msg, "Internal Server Error")
        self.assertEqual(status_code, 500)

        # Ensure retrieve_resource was called once
        mock_retrieve_resource.assert_called_once()

    @patch("myinfo.utils.client.MyInfoPersonalClientV4.get_authorise_url", return_value="https://example.com/authorize")
    def test_generate_authorize_url_success(self, mock_get_authorise_url):
        """Test generating an authorize URL successfully."""
        authorize_url = self.service.generate_authorize_url()

        self.assertEqual(authorize_url, "https://example.com/authorize")

        # Ensure the mocked method was called once
        mock_get_authorise_url.assert_called_once()

    def test_get_person_data_invalid_session(self):
        """Test when session is missing or invalid."""
        self.request.session.flush()  # This clears the session and assigns a new session_key

        self.service = MyInfoService(self.request)

        data, error_msg, status_code = self.service.get_person_data(
            auth_code="valid_code")

        self.assertIsNone(data)
        self.assertEqual(error_msg, "Invalid Request")
        self.assertEqual(status_code, 400)
