import os
import django
from channels.routing import get_default_application
import channels

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'web_socket_app.settings')

django.setup()
application = get_default_application()