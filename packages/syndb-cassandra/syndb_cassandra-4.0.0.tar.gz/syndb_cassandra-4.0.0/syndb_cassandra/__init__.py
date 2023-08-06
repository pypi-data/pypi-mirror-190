import os

os.environ["CQLENG_ALLOW_SCHEMA_MANAGEMENT"] = "1"

IN_PRODUCTION = os.environ.get("IN_PRODUCTION", False)
PROJECT_NAME: str = "syndb-cassandra"
