import os
import sys
from pathlib import Path
from django.core.wsgi import get_wsgi_application

# Resolve project paths
ROOT_DIR = Path(__file__).resolve().parent.parent
PROJECT_DIR = ROOT_DIR / 'gaming_news_site'

# Add gaming_news_site directory to Python path
if str(PROJECT_DIR) not in sys.path:
    sys.path.insert(0, str(PROJECT_DIR))

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gaming_news_site.settings')

# Expose WSGI application for Vercel Serverless Function
app = get_wsgi_application()

