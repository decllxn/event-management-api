web: gunicorn event-management-api.wsgi --log-file -
release: python manage.py migrate
heroku config:get DATABASE_URL -a event-management-api