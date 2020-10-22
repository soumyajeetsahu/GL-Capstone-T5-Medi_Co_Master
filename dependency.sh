apt-get install -y nginx
pip install gunicorn
cd /var/www/html
sudo apt-get remove libapache2-mod-python libapache2-mod-wsgi
apt-get install libapache2-mod-wsgi-py3
gunicorn --bind 0.0.0.0:8080 Medi_Co.wsgi:application
