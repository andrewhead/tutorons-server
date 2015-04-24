#! /bin/bash
(cd expserver && python manage.py runserver 8001)&
(cd js && python -mSimpleHTTPServer 8000)&
