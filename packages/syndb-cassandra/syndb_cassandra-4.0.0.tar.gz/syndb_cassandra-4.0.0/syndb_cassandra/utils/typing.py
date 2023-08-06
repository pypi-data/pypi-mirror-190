from typing import TypeVar

from cassandra.cqlengine.models import Model

CassandraModel = TypeVar("CassandraModel", bound=Model)
