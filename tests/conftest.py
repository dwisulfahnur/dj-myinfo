import os
import pytest
import django
from django.core.management import call_command

os.environ['DJANGO_SETTINGS_MODULE'] = 'djmyinfo.testsettings'

django.setup()

@pytest.fixture(scope="session", autouse=True)
def setup_django():

    # Run migrations before tests
    call_command("migrate", "--noinput")
