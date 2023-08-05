from __future__ import annotations

import logging
from collections.abc import Iterable
from dataclasses import dataclass
from typing import (
    Optional,
    Protocol,
)

from sretoolbox.utils import threaded

from reconcile.utils.secret_reader import (
    HasSecret,
    SecretNotFound,
    SecretReaderBase,
)


class Disable(Protocol):
    integrations: Optional[list[str]]
    e2e_tests: Optional[list[str]]


class Cluster(Protocol):
    name: str
    server_url: str
    internal: Optional[bool]
    insecure_skip_tls_verify: Optional[bool]

    @property
    def automation_token(self) -> Optional[HasSecret]:
        ...

    @property
    def cluster_admin_automation_token(self) -> Optional[HasSecret]:
        ...

    @property
    def disable(self) -> Optional[Disable]:
        ...


class Namespace(Protocol):
    cluster_admin: Optional[bool]

    @property
    def cluster(self) -> Cluster:
        ...


@dataclass
class OCConnectionParameters:
    """
    Container for Openshift Client (OC) parameters.
    These parameters are necessary to initialize a connection to a cluster.
    As a convenience, this class is able to convert generated classes
    into proper OC connection parameters.
    """

    cluster_name: str
    server_url: str
    is_internal: Optional[bool]
    is_cluster_admin: Optional[bool]
    skip_tls_verify: Optional[bool]
    automation_token: Optional[str]
    cluster_admin_automation_token: Optional[str]
    disabled_integrations: list[str]
    disabled_e2e_tests: list[str]

    @staticmethod
    def from_cluster(
        cluster: Cluster, secret_reader: SecretReaderBase
    ) -> OCConnectionParameters:
        automation_token: Optional[str] = None
        if cluster.automation_token:
            try:
                automation_token = secret_reader.read_secret(cluster.automation_token)
            except SecretNotFound as e:
                logging.error(
                    f"[{cluster.name}] secret {cluster.automation_token} not found"
                )
                raise e

        disabled_integrations = []
        disabled_e2e_tests = []
        if cluster.disable:
            disabled_integrations = cluster.disable.integrations or []
            disabled_e2e_tests = cluster.disable.e2e_tests or []

        return OCConnectionParameters(
            cluster_name=cluster.name,
            server_url=cluster.server_url,
            is_internal=cluster.internal,
            skip_tls_verify=cluster.insecure_skip_tls_verify,
            disabled_e2e_tests=disabled_e2e_tests,
            disabled_integrations=disabled_integrations,
            automation_token=automation_token,
            # is_cluster_admin only possible for namespace queries
            is_cluster_admin=None,
            cluster_admin_automation_token=None,
        )

    @staticmethod
    def from_namespace(
        namespace: Namespace, secret_reader: SecretReaderBase
    ) -> OCConnectionParameters:
        """
        This does the same as from_cluster(), but additionally checks
        for cluster_admin credentials.
        """
        cluster = namespace.cluster
        parameter = OCConnectionParameters.from_cluster(
            cluster=cluster, secret_reader=secret_reader
        )
        if namespace.cluster_admin is None:
            return parameter

        cluster_admin_automation_token = None
        if cluster.cluster_admin_automation_token and namespace.cluster_admin:
            try:
                cluster_admin_automation_token = secret_reader.read_secret(
                    cluster.cluster_admin_automation_token
                )
            except SecretNotFound as e:
                logging.error(
                    f"[{cluster.name}] secret {cluster.automation_token} not found"
                )
                raise e

        return OCConnectionParameters(
            cluster_name=parameter.cluster_name,
            server_url=parameter.server_url,
            is_internal=parameter.is_internal,
            skip_tls_verify=parameter.skip_tls_verify,
            disabled_e2e_tests=parameter.disabled_e2e_tests,
            disabled_integrations=parameter.disabled_integrations,
            automation_token=parameter.automation_token,
            is_cluster_admin=namespace.cluster_admin,
            cluster_admin_automation_token=cluster_admin_automation_token,
        )


def get_oc_connection_parameters_from_clusters(
    secret_reader: SecretReaderBase,
    clusters: Iterable[Cluster],
    thread_pool_size: int = 1,
) -> list[OCConnectionParameters]:
    """
    Convert nested generated cluster classes from queries into flat ClusterParameter objects.
    Also fetch required ClusterParameter secrets from vault with multiple threads.
    ClusterParameter objects are used to initialize an OCMap.
    """
    parameters: list[OCConnectionParameters] = threaded.run(
        OCConnectionParameters.from_cluster,
        clusters,
        thread_pool_size,
        secret_reader=secret_reader,
    )
    return parameters


def get_oc_connection_parameters_from_namespaces(
    secret_reader: SecretReaderBase,
    namespaces: Iterable[Namespace],
    thread_pool_size: int = 1,
) -> list[OCConnectionParameters]:
    """
    Convert nested generated namespace classes from queries into flat ClusterParameter objects.
    Also fetch required ClusterParameter secrets from vault with multiple threads.
    ClusterParameter objects are used to initialize an OCMap.
    """
    parameters: list[OCConnectionParameters] = threaded.run(
        OCConnectionParameters.from_namespace,
        namespaces,
        thread_pool_size,
        secret_reader=secret_reader,
    )
    return parameters
