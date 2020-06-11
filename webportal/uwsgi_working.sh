export DB_PASS=dbpass
uwsgi -s mysite.sock --wsgi-file app.py --callable app -C
