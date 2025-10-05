#!/bin/sh
set -e
# run with args forwarded, e.g. `docker run … scraper --file urls.txt`
exec python -u src/main.py "$@"
