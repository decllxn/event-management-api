web: gunicorn event_management_api.wsgi --log-file -
release: python manage.py migrate
heroku config:get DATABASE_URL -a event-management-api