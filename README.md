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

2. Enter to Django admin interface http://localhost:8000/admin/.

    Default credentials:
    - username: admin
    - password: Zaq1Xsw2
