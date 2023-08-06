from typing import Optional

from pydantic import FilePath

from syndb_cassandra.settings import outside_production_settings
from syndb_cassandra.workflows.rings import create_syndb_tables


def create_from_outside(settings_json: Optional[FilePath] = None):
    create_syndb_tables(settings=settings_json or outside_production_settings())
