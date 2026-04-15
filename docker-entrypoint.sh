#!/bin/sh
set -e

python manage.py migrate --noinput

if [ "${POPULATE_TRACKS:-0}" = "1" ]; then
  python manage.py populate_tracks
fi

exec "$@"
