# Mailganer test

### Start project

1. Run all services with docker compose
```sh
docker-compose up -d
```
    1.1. Load test data
    ```sh
    docker-compose exec web ./manage.py loaddata ./fixtures/initial_data.json
    ```
    1.2. Create superuser (optional)
    ```sh
    docker-compose exec web ./manage.py changepassword admin
    ```

2. Enter to Django admin interface: http://localhost:8000/admin/.

    Default credentials:
    - username: admin
    - password: Zaq1Xsw2

3. For looking sending emails in console use the next command:
```sh
docker-compose logs -f celery
```

4. Create Event for send emails use this url: http://localhost:8000/events/

5. Flower for monitoring Celery tasks: http://localhost:8005/tasks
