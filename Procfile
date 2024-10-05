web: gunicorn event-management-api100.wsgi --log-file -
release: python manage.py migrate
heroku config:get DATABASE_URL -a event-management-api