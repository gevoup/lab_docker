#!/bin/sh

# Wait for database to be ready
sleep 2

# Initialize migrations if they don't exist
if [ ! -d "migrations" ]; then
    flask db init
    flask db migrate -m "Initial migration"
fi

# Apply migrations and start app
flask db upgrade
python app.py
