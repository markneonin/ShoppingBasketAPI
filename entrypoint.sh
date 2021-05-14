#! /bin/bash

cd TheShoppingBasket

python createdatabase.py

exec gunicorn -w 8 "wsgi:app" --bind 0.0.0.0:8000 --reload