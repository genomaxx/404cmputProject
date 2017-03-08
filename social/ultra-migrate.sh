#!/usr/bin/bash

rm -rf post/migrations/*
rm -rf comment/migrations/*
rm -rf author/migrations/*

python manage.py makemigrations author
python manage.py makemigrations post
python manage.py makemigrations comment

python manage.py migrate
