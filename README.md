# IIS-ITS
## Prerequisites
```shell script
docker-compose up
````
and reflect changes in database
```shell script
docker-compose run web python manage.py migrate
```
web server will be available at http://localhost:8000