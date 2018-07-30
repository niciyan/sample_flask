#!/bin/sh


source venv/bin/activate

while true; do
    python manage.py deploy
    if [[ "$?" == "0" ]]; then
        break
    fi
    echo Deploy command failed, retrying in 5 secs...
    sleep 10
done

exec gunicorn -b :5000 --access-logfile - --error-logfile - manage:app
