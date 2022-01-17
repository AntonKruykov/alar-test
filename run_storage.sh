source .venv/bin/activate

cd route_storage
python manage.py migrate
python manage.py runserver --port=8080
