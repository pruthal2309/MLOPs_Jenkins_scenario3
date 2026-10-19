# Scenario 3 - Separate web and database apps

```text
webapp/
	app.py
	model.pkl
	Dockerfile
	requirements.txt
	templates/
dbapp/
	app.py
	Dockerfile
	requirements.txt
```

`webapp` serves the Iris prediction pages and model. `dbapp` is a Flask API
whose SQLAlchemy model reads and writes prediction records in PostgreSQL. The
PostgreSQL server is a third container; the database API and web app are
separate app containers.

## Run

From this directory:

```powershell
docker compose up --build
```

Open http://localhost:5000. Prediction history is available at
http://localhost:5000/records. PostgreSQL is available to local database tools
on `localhost:5432` with database `iris_db`, username `iris_user`, and password
`iris_password`. The data persists in the `postgres_data` Docker volume.

To stop the apps, press `Ctrl+C` or run `docker compose down`. To also delete
the saved predictions, run `docker compose down --volumes`.

## Build the app images separately

```powershell
docker build -t iris-webapp ./webapp
docker build -t iris-dbapp ./dbapp
```

Compose is the recommended way to run them because it configures their network,
database connection, health checks, and startup order.
