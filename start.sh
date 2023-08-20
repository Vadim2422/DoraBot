#!/bin/bash
touch ./db/dora.db
pip install alembic
alembic upgrade head
