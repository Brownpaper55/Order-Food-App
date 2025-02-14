web: gunicorn kitchenette.wsgi --log-file
web: python manage.py migrate && gunicorn kitchenette.wsgi
application --workers 3 --bind 0.0.0.0:$PORT 