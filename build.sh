#!/usr/bin/env bash
# exit on error

set -o errexit

# poetry install
pip install -r requirements.txt

# Revertir las migraciones
python manage.py migrate cuentas zero --database=default
python manage.py migrate logs zero --database=logsdb

# Aplicar las migraciones nuevamente
python manage.py migrate cuentas --database=default
python manage.py migrate logs --database=logsdb

# Crear un superusuario
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@example.com', 'admin2023')" | python manage.py shell
WORD=sFwZbJ6SOkdh99N71nva530qw6aggiD4 psql -h dpg-cn94jb6d3nmc73dgl240-a.oregon-postgres.render.com -U chaucheritadb_user chaucheritadb -c "ALTER TABLE auth_user ALTER COLUMN last_login SET NOT NULL;"