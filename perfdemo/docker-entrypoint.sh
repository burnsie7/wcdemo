#!/bin/bash
if [ "$IS_WORKER" == "true" ]; then
    echo 'starting celery worker';
    export C_FORCE_ROOT=1
    DATADOG_ENV=wcd ddtrace-run celery -A perfdemo worker -l info
elif [ "$IS_BEAT" == "true" ]; then
    echo 'starting celery beat';
    export C_FORCE_ROOT=1
    DATADOG_ENV=wcd ddtrace-run celery -A perfdemo beat -l info
else
    echo 'starting gunicorn web server';
    gunicorn -w 5 --statsd-host dd-agent:8125 -b :8000 perfdemo.wsgi:application
fi
