#!/usr/bin/env bash
# Blocca lo script in caso di errore
set -o errexit

# Installa le dipendenze
pip install -r requirements.txt

# Raccoglie i file statici
python manage.py collectstatic --no-input

# Esegue le migrazioni del database
python manage.py migrate

# Crea il superuser automaticamente leggendo dalle variabili d'ambiente di Render
python manage.py shell -c "
from django.contrib.auth.models import User
import os

username = os.environ.get('DJANGO_SUPERUSER_USERNAME')
email = os.environ.get('DJANGO_SUPERUSER_EMAIL')
password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')

if username and password:
    if not User.objects.filter(username=username).exists():
        print('Creazione superuser in corso...')
        User.objects.create_superuser(username, email, password)
        print('Superuser creato con successo.')
    else:
        print('Il superuser esiste già.')
else:
    print('Variabili d'ambiente per il superuser non configurate.')
"