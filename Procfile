



web: python manage.py collectstatic --noinput && gunicorn ecommerceproject.wsgi



web: python manage.py collectstatic --noinput --verbosity 2 && python manage.py migrate && gunicorn ecommerceproject.wsgi:application