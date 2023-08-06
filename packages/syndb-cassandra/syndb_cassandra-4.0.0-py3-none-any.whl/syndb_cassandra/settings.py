import base64
import json
import ssl
import subprocess
from functools import cached_property
from typing import ClassVar, Optional, Type, TypeVar

from pydantic import BaseSettings, DirectoryPath, FilePath

from syndb_cassandra import IN_PRODUCTION


class BaseSyndbCassandraSettings(BaseSettings):
    cqlsh_host_name: str = ...
    cqlsh_tls_path: Optional[DirectoryPath]

    superuser_role_name: str = "su"
    modify_role_name: str = "mod"

    remove_pre_existing_syndb: bool = False

    cassandra_connection_name: ClassVar[str] = "stargate"

    class Config:
        keep_untouched = (cached_property,)

    @property
    def cassandra_auth_provider(self):
        return None

    @property
    def cluster(self):
        from cassandra.cluster import Cluster

        return Cluster(
            contact_points=[self.cqlsh_host_name],
            ssl_context=self.ssl_context,
            auth_provider=self.cassandra_auth_provider,
        )

    @property
    def ssl_context(self):
        if not self.cqlsh_tls_path:
            return None
        result = ssl.SSLContext(ssl.PROTOCOL_TLS)
        result.load_cert_chain(self.cqlsh_tls_path / "tls.crt", self.cqlsh_tls_path / "tls.key")
        return result

    def cassandra_connection(self):
        from cassandra.cqlengine import connection

        cassandra_session = self.cluster.connect()
        connection.register_connection(self.cassandra_connection_name, session=cassandra_session)
        return cassandra_session

    @classmethod
    def from_json(cls, json_path: FilePath):
        with open(json_path, "rb") as in_json:
            return json.load(in_json)


SyndbCassandraSettings = TypeVar("SyndbCassandraSettings", bound=BaseSyndbCassandraSettings)


class SyndbCassandraTestSettings(BaseSyndbCassandraSettings):
    cqlsh_host_name = "localhost"
    remove_pre_existing_syndb = True


class SyndbCassandraProductionSettings(BaseSyndbCassandraSettings):
    cqlsh_username: str = ...
    cqlsh_password: str = ...

    @cached_property
    def cassandra_auth_provider(self):
        from cassandra.auth import PlainTextAuthProvider

        return PlainTextAuthProvider(username=self.cqlsh_username, password=self.cqlsh_password)


def outside_production_settings() -> SyndbCassandraProductionSettings:
    return SyndbCassandraProductionSettings(
        cqlsh_host_name="localhost",
        cqlsh_username=base64.b64decode(
            subprocess.Popen(
                [
                    "kubectl",
                    "get",
                    "secret",
                    "k8ssandra-cluster-superuser",
                    "-n",
                    "syndb-k8ssandra",
                    "-o=jsonpath='{.data.username}'",
                ],
                stdout=subprocess.PIPE,
            )
            .communicate()[0]
            .rstrip()
        ).decode("utf-8"),
        cqlsh_password=base64.b64decode(
            subprocess.Popen(
                [
                    "kubectl",
                    "get",
                    "secret",
                    "k8ssandra-cluster-superuser",
                    "-n",
                    "syndb-k8ssandra",
                    "-o=jsonpath='{.data.password}'",
                ],
                stdout=subprocess.PIPE,
            )
            .communicate()[0]
            .rstrip()
        ).decode("utf-8"),
    )


def cassandra_settings_getter(
    manual_testing_override: bool = False, manual_production_override: bool = False
) -> Type[SyndbCassandraProductionSettings | SyndbCassandraTestSettings]:
    assert not (manual_testing_override and manual_production_override)

    if manual_testing_override:
        return SyndbCassandraTestSettings
    if manual_production_override:
        return SyndbCassandraProductionSettings

    return SyndbCassandraProductionSettings if IN_PRODUCTION else SyndbCassandraTestSettings
