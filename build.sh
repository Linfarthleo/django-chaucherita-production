#!/usr/bin/env bash
# exit on error

set -o errexit

# poetry install
pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate cuentas --database=default
python manage.py migrate logs --database=logsdb

PGPASSWORD=sFwZbJ6SOkdh99N71nva530qw6aggiD4 psql -h dpg-cn94jb6d3nmc73dgl240-a.oregon-postgres.render.com -U chaucheritadb_user chaucheritadb -c "ALTER TABLE auth_user ALTER COLUMN last_login DROP NOT NULL;"

echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@example.com', 'admin2023')" | python manage.py shell

PGPASSWORD=sFwZbJ6SOkdh99N71nva530qw6aggiD4 psql -h dpg-cn94jb6d3nmc73dgl240-a.oregon-postgres.render.com -U chaucheritadb_user chaucheritadb -c "ALTER TABLE auth_user ALTER COLUMN last_login SET NOT NULL;"