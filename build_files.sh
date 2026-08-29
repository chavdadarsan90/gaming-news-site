#!/bin/bash
echo "Installing dependencies..."
python3 -m pip install -r requirements.txt

echo "Collecting static files..."
python3 gaming_news_site/manage.py collectstatic --noinput --clear
echo "Build completed successfully."
