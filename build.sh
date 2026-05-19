#!/usr/bin/env bash
set -o errexit

# Installa le dipendenze
pip install -r requirements.txt

# Raccoglie i file statici
python manage.py collectstatic --no-input

# Esegue le migrazioni
python manage.py migrate

# Crea il superuser leggendo dalle variabili d'ambiente
python manage.py shell -c "
from django.contrib.auth.models import User
import os

username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@scifiverse.com')
password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'PasswordSicura123')

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username, email, password)
    print('Utente amministratore creato con successo.')
else:
    print('L utente amministratore esiste gia.')
"