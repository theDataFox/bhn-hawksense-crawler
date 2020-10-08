#!/bin/sh

python manage.py db init
python manage.py db migrate
python manage.py db upgrade

# alembic stamp head
# alembic revision --autogenerate -m "comment"