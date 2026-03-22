



web: python manage.py collectstatic --noinput && gunicorn ecommerceproject.wsgi



web: python manage.py collectstatic --noinput --verbosity 3 && python manage.py migrate && gunicorn ecommerceproject.wsgi:application