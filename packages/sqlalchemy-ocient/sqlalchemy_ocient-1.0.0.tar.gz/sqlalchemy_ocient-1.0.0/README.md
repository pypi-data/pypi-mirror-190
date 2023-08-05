# Ocient Dialect for SQLAlchemy

The Ocient Database Python API extension gives application developers the full power and flexibility of SQLAlchemy.

## Installation

Install the sqlalchemy-ocient package.

```python
pip install sqlalchemy-ocient
```

## SQLAlchemy URI


The Ocient DSN is of the format:
```shell
ocient://user:password@[host][:port][/database][?param1=value1&...]
```

**NOTE**: You must enter the `user` and `password` credentials.  `host` defaults to localhost,
port defaults to 4050, database defaults to `system` and `tls` defaults
to `off`.

## User Access Control

Make sure the user has privileges to access and use all required databases, schemas, tables, views, and warehouses, as the Ocient SQLAlchemy engine does not test for user or role rights by default.
