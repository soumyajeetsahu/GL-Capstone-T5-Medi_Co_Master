apt-get install -y nginx
pip install gunicorn
cd /var/www/html
gunicorn --bind 0.0.0.0:8080 Medi_Co.wsgi:application
