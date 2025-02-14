web: gunicorn kitchenette.wsgi:application --workers 3 --bind 0.0.0.0:$PORT
web: python manage.py migrate && gunicorn kitchenette.wsgi