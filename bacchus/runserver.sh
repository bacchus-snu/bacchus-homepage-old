#!/bin/bash

python manage.py syncdb
python manage.py collectstatic
python manage.py runserver dew.snucse.org:9090
