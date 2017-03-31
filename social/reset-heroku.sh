heroku pg:reset DATABASE_URL --confirm calm-wave-83737
heroku run bash ultra-migrate.sh
heroku run "python manage.py shell < dummy_data.py"