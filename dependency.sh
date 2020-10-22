apt-get install -y nginx
pip install gunicorn
gunicorn --bind 0.0.0.0:8080 Medi_Co.wsgi:application
