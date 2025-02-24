from django.urls import path
from .views import index_view, callback_form_view
from .api import generate_authorize_url, get_person_data_api

urlpatterns = [
    path('', index_view, name='index'),
    path('callback', callback_form_view, name='callback'),
    path('api/persons', get_person_data_api, name='api-get-person-data'),
    path('api/authorize', generate_authorize_url, name='api-generate-authorize-url'),
]
