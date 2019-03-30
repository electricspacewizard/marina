# Marina app

Built to manage boats on the dock. Specifically for obtain position for crane points.

# Setup

Copy `.env-template` to `.env` and give values to the placeholder variables.

With the Postgres DB running, execute the seed data from `database-seed.sql`.

# Usage

Boot up the Flask server with:
`python3 app.py`

Alternatively boot up as a Docker container with:
`docker build -t marina:latest .`
`docker run --rm -p 5000:80 marina`

Boot up the Docker based Postgres with:
`docker run --rm --name postgres-db -p 5432:5432 -e POSTGRES_USER=marina -e POSTGRES_PASSWORD=marina -e POSTGRES_DBNAME=marina -v $(pwd)/database:/var/lib/postgresql/data  postgres`

# Deploy

Currently deployed to AWS Fargate

For the AWS CLI login, use the correct profile with:
`$(aws ecr get-login --no-include-email --region eu-west-2)`

Then push the built docker image up to the `marina` ECS repo with the usual push commands.
Once pushed, head into the `marina` cluster and run as a new Task.


# Troubeshooting?

Finding Postgres queries hang?
Try looking up long-running processes and kill 'em via pid as follows:

`select * from pg_stat_activity;
SELECT pg_terminate_backend(47)`


