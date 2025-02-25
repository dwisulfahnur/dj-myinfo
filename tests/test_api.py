import json
from unittest.mock import patch
from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status


class MyInfoAPITestCase(TestCase):
    def setUp(self):
        self.client = Client()

    @patch('myinfo.services.MyInfoService.generate_authorize_url')
    def test_generate_authorize_url_success(self, mock_generate_url):
        mock_url = "https://test.myinfo.gov.sg/authorize?client_id=TEST"
        mock_generate_url.return_value = mock_url

        response = self.client.post(reverse('api-generate-authorize-url'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {'authorize_url': mock_url})
        mock_generate_url.assert_called_once()

    @patch('myinfo.services.MyInfoService.get_person_data')
    def test_get_person_data_success(self, mock_get_person_data):
        mock_person_data = {
            'uinfin': {'value': 'S1234567A'},
            'name': {'value': 'Test User'},
        }
        mock_get_person_data.return_value = (mock_person_data, None, 200)

        response = self.client.post(
            reverse('api-get-person-data'),
            data=json.dumps({'code': 'test_auth_code'}),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), mock_person_data)
        mock_get_person_data.assert_called_once_with(
            auth_code='test_auth_code')

    @patch('myinfo.services.MyInfoService.get_person_data')
    def test_get_person_data_error(self, mock_get_person_data):
        error_msg = "Invalid Request"
        mock_get_person_data.return_value = (None, error_msg, 400)

        response = self.client.post(
            reverse('api-get-person-data'),
            data=json.dumps({'code': 'invalid_code'}),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {'msg': error_msg})

    def test_get_person_data_validation_error(self):
        # Act - omit the required 'code' field
        response = self.client.post(
            reverse('api-get-person-data'),
            data=json.dumps({}),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Should contain validation error about 'code'
        self.assertIn('code', response.json())
