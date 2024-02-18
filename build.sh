#!/usr/bin/env bash
# exit on error

set -o errexit

# poetry install
pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate cuentas --database=default
# python manage.py migrate logs --database=logsdb

echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@example.com', 'admin2023')" | python manage.py shell