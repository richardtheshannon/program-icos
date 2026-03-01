"""
Passenger WSGI entry point for cPanel/Passenger deployment.

cPanel's Passenger expects a top-level `application` callable in this file.
"""

import os
import sys

# Add the project directory to the Python path
project_dir = os.path.dirname(os.path.abspath(__file__))
if project_dir not in sys.path:
    sys.path.insert(0, project_dir)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings_production")

from django.core.wsgi import get_wsgi_application  # noqa: E402

application = get_wsgi_application()
