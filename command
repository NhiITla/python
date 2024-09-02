- create django app with docker compose:
docker-compose run --rm app sh -c "django-admin startproject app ."
docker-compose run --rm app sh -c "python manage.py startapp core"

docker-compose up

- 2. run django app:
docker-compose up
- to delete resouce after docker-compose-up: 
docker-compose down -v --rmi all

This will stop and remove everything created by docker-compose up, including containers, networks, volumes, and images.

Make sure you run these commands from the directory where your docker-compose.yml file is located or specify the path to the Compose file using the -f option.

- 3. added github action:

write the test after that write the code

-4. run test:
docker-compose run --rm app sh -c "python manage.py test"
docker-compose run --rm app sh -c "python manage.py wait_for_db"
