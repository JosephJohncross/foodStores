set -o errexit

pip install -r requirements.txt
pip install GDAL-3.4.3-cp311-cp311-win_amd64.whl, gunicorn

python manage.py collectstatic --no-input

python manage.py migrate