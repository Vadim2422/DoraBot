#!/bin/bash
touch ./db/dora.db
pip install -r requirements.txt
alembic upgrade head
