#!/usr/bin/env bash
set -o errexit

# Install dependencies
pip install -r requirements.txt

# ONLY run migrations (no collectstatic!)
python manage.py migrate --noinput
