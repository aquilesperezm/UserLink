# UserLink
A technical test that shows the use of FastAPI and SQLAlchemy. It is composed of the models or entities: User, Post, Comment and Tag; where a user can create many Posts, a Post can have many Comments and this in turn can have many Tags, as well as a Tag can have many Comments.

The application is supported by database migrations, which allows for its prompt restoration. All queries made to the database are asynchronous. 

## Installing App 


## Installing Database

openssl rand -hex 32

#### generate new secret string
pip freeze > requirements.txt

#### create new enviroment
py -m venv .venv -r requirements.txt

#### create migrations
alembic revision --autogenerate -m "Initial migration"

alembic history -> show all revisions

alembic show <id revisions> -> show details of revision

alembic upgrade < head | id rev >
alembic downgrade < base | id rev>
alembic upgrade +1
alembic downgrade -1




