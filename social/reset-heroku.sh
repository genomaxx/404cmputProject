heroku pg:reset DATABASE_URL --confirm mysterious-falls-21653
heroku run bash ultra-migrate.sh
heroku run "python manage.py shell < dummy_data.py"
