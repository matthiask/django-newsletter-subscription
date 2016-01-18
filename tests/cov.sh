#!/bin/sh
venv/bin/coverage run --branch --include="*newsletter_subscription/*" --omit="*tests*" ./manage.py test testapp
venv/bin/coverage html
