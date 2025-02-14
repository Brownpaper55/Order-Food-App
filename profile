web: gunicorn E_kitchen.wsgi --log-file
web: python manage.py migrate && gunicorn E_kitchen.wsg