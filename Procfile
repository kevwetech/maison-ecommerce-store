

web: echo "Static dir:" && ls static/ && python manage.py collectstatic --noinput --clear && python manage.py migrate && gunicorn ecommerceproject.wsgi:application