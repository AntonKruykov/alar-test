source .venv/bin/activate

cd route_reports
python manage.py migrate
python manage.py runserver --port=8082
