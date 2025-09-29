#!/usr/bin/env bash
# Render deployment build script

set -o errexit  # Exit on error

# Install Python dependencies
pip install -r requirements.txt

# Collect static files for Django
python manage.py collectstatic --noinput

# Run database migrations
python manage.py migrate