import logging
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request
from myinfo.services import MyInfoService
from myinfo.serializers import GetPersonDataSerializer

logger = logging.getLogger(__name__)


@api_view(['POST'])
def generate_authorize_url(request: Request):
    service = MyInfoService(request)
    authorize_url = service.generate_authorize_url()
    return Response({'authorize_url': authorize_url})


@api_view(['POST'])
def get_person_data_api(request: Request):
    serializer = GetPersonDataSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    service = MyInfoService(request)
    (
        person_data,
        error_msg,
        status_code
    ) = service.get_person_data(auth_code=serializer.validated_data['code'])

    if error_msg:
        return Response({"msg": error_msg}, status=status_code)

    return Response(person_data)
