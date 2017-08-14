#!/bin/bash
SETTING_PATH=`find /app/fireshot/ -name settings.py`

pip3 install -r req.txt
if [ ! -f /app/password.txt ] ; then
    # Start Postgres
    /etc/init.d/postgresql start & sleep 5s
    # Set password
    POSTGRES_DJANGO_PASSWORD=`pwgen -c -n -1 12`

    echo -e "POSTGRES_DJANGO_PASSWORD = $POSTGRES_DJANGO_PASSWORD\n" > /app/password.txt

    # Initialize Postgres
    sed -i "s|password|$POSTGRES_DJANGO_PASSWORD|g" /app/init.sql
    su - postgres -c 'psql -f /app/init.sql'

    pip3 install psycopg2

    # Modify database setting to Postgres
    sed -i "s|django.db.backends.sqlite3|django.db.backends.postgresql_psycopg2|g" $SETTING_PATH
    sed -i "s|os.path.join(BASE_DIR, 'db.sqlite3')|'django',\n        'HOST': '127.0.0.1',\n        'USER': 'django',\n        'PASSWORD': '$POSTGRES_DJANGO_PASSWORD'|g" $SETTING_PATH

    python3 /app/manage.py migrate
    /etc/init.d/postgresql stop
fi

# Start all the services
/usr/bin/supervisord -n