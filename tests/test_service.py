import requests
from unittest.mock import patch, MagicMock
from django.test import TestCase
from myinfo.models import OauthSessionState
from django.contrib.sessions.models import Session


class MyInfoServiceTestCase(TestCase):
    def setUp(self):
        # Create a mock request
        self.request = MagicMock()
        self.request.scheme = 'https'
        self.request.get_host.return_value = 'testserver'
        self.request.session = MagicMock()
        self.request.session.session_key = 'test_session_key'
        self.request.session.create = MagicMock()

        # Create a real session record for tests
        self.session = Session.objects.create(
            session_key='test_session_key',
            expire_date='2099-01-01 00:00:00Z'
        )

        # Create service instance
        from myinfo.services import MyInfoService
        self.service = MyInfoService(self.request)

    def test_get_callback_url(self):
        callback_url = self.service.get_callback_url()

        self.assertEqual(callback_url, 'https://testserver/callback')

    @patch('myinfo.utils.client.MyInfoPersonalClientV4.get_authorise_url')
    def test_generate_authorize_url(self, mock_get_authorise_url):
        mock_url = "https://test.myinfo.gov.sg/authorize?client_id=TEST"
        mock_get_authorise_url.return_value = mock_url

        url = self.service.generate_authorize_url()

        self.assertEqual(url, mock_url)

        # Verify session state was created
        oauth_state = OauthSessionState.objects.filter(
            session_id='test_session_key').first()
        self.assertIsNotNone(oauth_state)
        mock_get_authorise_url.assert_called_once()

    @patch('myinfo.utils.client.MyInfoPersonalClientV4.retrieve_resource')
    def test_get_person_data_success(self, mock_retrieve_resource):
        mock_data = {'name': {'value': 'Test User'}}
        mock_retrieve_resource.return_value = mock_data

        # Create OauthSessionState record
        OauthSessionState.objects.create(
            session_id='test_session_key', key='test_state')

        data, error, status = self.service.get_person_data('test_auth_code')

        self.assertEqual(data, mock_data)
        self.assertIsNone(error)
        self.assertEqual(status, 200)
        mock_retrieve_resource.assert_called_once_with(
            state='test_state',
            callback_url='https://testserver/callback',
            auth_code='test_auth_code'
        )

    def test_get_person_data_no_state(self):
        # Act (without creating OauthSessionState)
        data, error, status = self.service.get_person_data('test_auth_code')

        self.assertIsNone(data)
        self.assertEqual(error, 'Invalid Request')
        self.assertEqual(status, 400)

    @patch('myinfo.utils.client.MyInfoPersonalClientV4.retrieve_resource')
    def test_get_person_data_http_error(self, mock_retrieve_resource):
        # Arrange
        mock_retrieve_resource.side_effect = requests.HTTPError()

        # Create OauthSessionState record
        OauthSessionState.objects.create(
            session_id='test_session_key', key='test_state')

        data, error, status = self.service.get_person_data('test_auth_code')

        self.assertIsNone(data)
        self.assertEqual(error, 'Code is not valid')
        self.assertEqual(status, 400)

    @patch('myinfo.utils.client.MyInfoPersonalClientV4.retrieve_resource')
    def test_get_person_data_general_exception(self, mock_retrieve_resource):
        # Arrange
        mock_retrieve_resource.side_effect = Exception

        # Create OauthSessionState record
        OauthSessionState.objects.create(
            session_id='test_session_key', key='test_state')

        data, error, status = self.service.get_person_data('test_auth_code')

        self.assertIsNone(data)
        self.assertEqual(error, 'Internal Server Error')
        self.assertEqual(status, 500)

