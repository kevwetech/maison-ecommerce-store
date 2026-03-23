




web: mkdir -p staticfiles && rm -f staticfiles/staticfiles.json && python manage.py collectstatic --noinput --clear && python manage.py migrate && gunicorn ecommerceproject.wsgi:application

