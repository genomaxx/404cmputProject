#!/usr/bin/bash

rm -rf post/migrations/*
rm -rf comment/migrations/*
rm -rf author/migrations/*
rm -rf node/migrations/*
rm -rf api/migrations/*
rm -rf settings/migrations/*

python manage.py makemigrations settings
python manage.py makemigrations author
python manage.py makemigrations post
python manage.py makemigrations comment
python manage.py makemigrations node
python manage.py makemigrations api

python manage.py migrate
