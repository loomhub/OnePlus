1. Run python3 -m venv venv
2. Run source venv/bin/activate

Alembic

1. Run `alembic init alembic` to create an alembic folder
2. Edit alembic.ini file to add "sqlalchemy.url=postgresql+psycopg2://admin:admin@localhost/oneplusrealtydb"
3. Edit alembic/env.py file to add "from oneplus.mylibrary.database.db import Base # Import the Base class"
4. Edit alembic/env.py file to add "target_metadata = Base.metadata # Set the target metadata to the Base.metadata"
5. Run `alembic revision --autogenerate -m "Create new database oneplusrealtydb"`
6. Alembic Revision ID: 112c2833dc69

PostgresSQL using terminal

1. In terminal, type `psql postgres`
2. Now run `CREATE DATABASE oneplusrealtydb OWNER admin;`
3. Now run "GRANT ALL PRIVILEGES ON DATABASE oneplusrealtydb TO admin;"
4. Run "\q" to exit

PostgreSQL Database using pgAdmin:
Port: The default PostgreSQL port is 5432. Use this unless you've changed it during the PostgreSQL installation or configuration.
Server: localhost
Database: oneplusrealtydb
Username: admin
Password: admin

FLOW OF THE PROGRAM

A) CONTROLLERS:
Controllers contain the methods (GET, PUT, POST, DELETE, PATCH, HEAD, OPTIONS ) specifying the type of operation client wants to perform on a resource.

A1. GET: This method is used to retrieve data from a server at the specified resource. GET requests should only retrieve data and have no other effect on the data.

A2. PUT: This method is used to update or replace the current representation of the target resource with the uploaded content. It is expected that PUT requests are idempotent, meaning that multiple identical PUT requests should have the same effect as a single request.

A3. POST: This method is used to send data to the server. For example, uploading a file, submitting a completed form, or creating a new record. POST requests usually result in a change of state or side effects on the server.

A4. DELETE: This method is used to delete a resource identified by the URL.

A5. PATCH: This method is used for making partial changes to an existing resource, whereas PUT might replace an existing resource entirely.

A6. HEAD: Similar to GET, but it retrieves only the headers that would be returned if the HEAD request was a GET request. This can be used to check the existence or size of a resource without downloading it.

A7. OPTIONS: This method is used to describe the communication options for the target resource. It can be used to check which HTTP methods are supported by the server.
