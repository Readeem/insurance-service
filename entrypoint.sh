#!/bin/sh

alembic upgrade head
python -O main.py