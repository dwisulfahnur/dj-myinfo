import logging
from django.utils.crypto import get_random_string
from django.http.request import HttpRequest
from requests.exceptions import HTTPError
from myinfo.models import OauthSessionState
from myinfo.utils.client import MyInfoPersonalClientV4

logger = logging.getLogger(__name__)


class MyInfoService:

    def __init__(self, request: HttpRequest):
        self.client = MyInfoPersonalClientV4()
        self.request = request

    def get_callback_url(self):
        scheme = self.request.scheme
        host = self.request.get_host()
        return f'{scheme}://{host}/callback'

    def get_person_data(self, auth_code):
        """Retrieve personal data using MyInfo API."""
        session_key = self.request.session.session_key
        oauth_state = OauthSessionState.objects.filter(
            session_id=session_key).first()
        if not oauth_state:
            return None, "Invalid Request", 400

        try:
            person_data = self.client.retrieve_resource(
                state=oauth_state.key,
                callback_url=self.get_callback_url(),
                auth_code=auth_code,
            )
            if not person_data:
                return None, "Not Found", 404

            return person_data, None, 200
        except HTTPError:
            return None, "Code is not valid", 400
        except Exception as err:
            logger.error(err)
            return None, "Internal Server Error", 500

    def generate_authorize_url(self):
        """Generate authorization URL and manage session state."""
        session_key = self.request.session.session_key

        # Ensure session exists / create if not
        if not session_key:
            self.request.session.create()
            session_key = self.request.session.session_key

        callback_url = self.get_callback_url()
        myinfo_client = MyInfoPersonalClientV4()

        oauth_state = OauthSessionState.objects.filter(
            session_id=session_key).first()
        oauth_state_key = get_random_string(length=16)


        if not oauth_state:
            oauth_state = OauthSessionState.objects.create(
                session_id=session_key,
                key=oauth_state_key,
            )
        else:
            oauth_state.key = oauth_state_key

        oauth_state.save()

        authorize_url = myinfo_client.get_authorise_url(
            oauth_state=oauth_state.key,
            callback_url=callback_url,
        )

        return authorize_url
