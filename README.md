# UserLink
A technical test that shows the use of FastAPI and SQLAlchemy. It is composed of the models or entities: User, Post, Comment and Tag; where a user can create many Posts, a Post can have many Comments and this in turn can have many Tags, as well as a Tag can have many Comments.

The application is supported by database migrations, which allows for its prompt restoration. All queries made to the database are asynchronous. 

## Installing App 

When we are going to install the application we must create a virtual environment, which will contain all the libraries of our project.

<b>Step #1</b>

Create a new Virtual Environment

<code>py -m venv .venv</code>

We must verify that the environment is activated, if not, we must activate it manually

<code>cd \<environment-folder></code>

<code>cd \<Scripts></code>

Run <code>Activate.bat</code>

<b>Step #2</b>

Install all requirements

<code>py -m pip install -r requirements.txt</code>

## Installing Database
We must install the database in the PostgreSQL database manager.

<b>Step #1</b>

```psql -u postgres -p```

<b>Step #2</b>

```CREATE DATABASE userlink_db;```

## Environment Variables

Environment variables manage all the external features of the application, the DB connection and its initial data.

### Server Config 

- **SERVER_HOSTNAME**='localhost' -> Nombre del servidor FastAPI(en muchos casos Localhost)
- **SERVER_PORT**=8000 -> Puerto de escucha para el servidor FastAPI

### Database Config 

- **DATABASE_HOSTNAME** : Database Server HostName
- **DATABASE_PORT**: Database Service Port  
- **DATABASE_USERNAME**: Database Username
- **DATABASE_PASSWORD**: Database Password
- **DATABASE_DBNAME**: Database Name

### JSON Web Token Config

- **ACCESS_TOKEN_EXPIRE_MINUTES**: Token expiration time
- **SECRET_KEY**: Key to encrypt token
##### Generating new key #####
```openssl rand -hex 32```
- **ALGORITHM**: Json Encrypt Algorithm (Ex: "HS256")

## General Config
**RESET_DB_FACTORY**: Restart Database Structure and Data

## Database Migrations

Database migration is the process of migrating data from one or more source databases to one or more target databases using a database migration service.

- **Create a new migration**

alembic revision --autogenerate -m "ex: Initial migration"

- **Query all migrations**

alembic history -> show all revisions

- **Show migration details**

alembic show <id revisions> -> show details of revision

- **Others Commands**

- alembic upgrade *< head | id rev >*: Upgrade migration with code or head
- alembic downgrade *< base | id rev>* : Downgrade migration code or base
- alembic upgrade *+1*: Upgrade migration with revision number
- alembic downgrade *-1*: Downgrade migration with revision number




