# Alembic

Initialize alembic
```bash
uv run alembic init -t async alembic
```
This will create a new directory called `alembic` with the following structure:
```
alembic/
├── env.py
├── README
├── script.py.mako
└── versions
```
and a new file called `alembic.ini` in the root directory of your project.

### Configure alembic
Edit the `env.py` file to set up the database connection and other configurations.
```python
# ------------------------------------------
# Project Imports
# ------------------------------------------
from core.database import SQLModel
from core.database import DATABASE_URL

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config
# Set the connection string for the database from the environment variable
config.set_main_option("sqlalchemy.url", DATABASE_URL)

target_metadata = SQLModel.metadata
```

### Create a migration
```bash
uv run alembic revision --autogenerate -m "Initial migration"
```
Note: You can also use the `make migration` command to create the migration interactively.

### Apply the migration
```bash
uv run alembic upgrade head
```
Note: You can also use the `make migrate` command to apply the migration interactively.
