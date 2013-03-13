#!/bin/sh
coverage run --branch --include="*newsletter_subscription/*" --omit="*tests*" ./manage.py test testapp
coverage html
