# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
from ._enums import *

__all__ = [
    'ConfigurationIdentityArgs',
    'DependsOnDefinitionArgs',
    'ExtensionStatusArgs',
    'GitRepositoryDefinitionArgs',
    'HelmOperatorPropertiesArgs',
    'KubernetesConfigurationPrivateLinkScopePropertiesArgs',
    'KustomizationDefinitionArgs',
    'PrivateLinkServiceConnectionStateArgs',
    'RepositoryRefDefinitionArgs',
    'ScopeClusterArgs',
    'ScopeNamespaceArgs',
    'ScopeArgs',
]

@pulumi.input_type
class ConfigurationIdentityArgs:
    def __init__(__self__, *,
                 type: Optional[pulumi.Input['ResourceIdentityType']] = None):
        """
        Identity for the managed cluster.
        :param pulumi.Input['ResourceIdentityType'] type: The type of identity used for the configuration. Type 'SystemAssigned' will use an implicitly created identity. Type 'None' will not use Managed Identity for the configuration.
        """
        if type is not None:
            pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter
    def type(self) -> Optional[pulumi.Input['ResourceIdentityType']]:
        """
        The type of identity used for the configuration. Type 'SystemAssigned' will use an implicitly created identity. Type 'None' will not use Managed Identity for the configuration.
        """
        return pulumi.get(self, "type")

    @type.setter
    def type(self, value: Optional[pulumi.Input['ResourceIdentityType']]):
        pulumi.set(self, "type", value)


@pulumi.input_type
class DependsOnDefinitionArgs:
    def __init__(__self__, *,
                 kustomization_name: Optional[pulumi.Input[str]] = None):
        """
        Specify which kustomizations must succeed reconciliation on the cluster prior to reconciling this kustomization
        :param pulumi.Input[str] kustomization_name: Name of the kustomization to claim dependency on
        """
        if kustomization_name is not None:
            pulumi.set(__self__, "kustomization_name", kustomization_name)

    @property
    @pulumi.getter(name="kustomizationName")
    def kustomization_name(self) -> Optional[pulumi.Input[str]]:
        """
        Name of the kustomization to claim dependency on
        """
        return pulumi.get(self, "kustomization_name")

    @kustomization_name.setter
    def kustomization_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "kustomization_name", value)


@pulumi.input_type
class ExtensionStatusArgs:
    def __init__(__self__, *,
                 code: Optional[pulumi.Input[str]] = None,
                 display_status: Optional[pulumi.Input[str]] = None,
                 level: Optional[pulumi.Input[Union[str, 'LevelType']]] = None,
                 message: Optional[pulumi.Input[str]] = None,
                 time: Optional[pulumi.Input[str]] = None):
        """
        Status from this instance of the extension.
        :param pulumi.Input[str] code: Status code provided by the Extension
        :param pulumi.Input[str] display_status: Short description of status of this instance of the extension.
        :param pulumi.Input[Union[str, 'LevelType']] level: Level of the status.
        :param pulumi.Input[str] message: Detailed message of the status from the Extension instance.
        :param pulumi.Input[str] time: DateLiteral (per ISO8601) noting the time of installation status.
        """
        if code is not None:
            pulumi.set(__self__, "code", code)
        if display_status is not None:
            pulumi.set(__self__, "display_status", display_status)
        if level is None:
            level = 'Information'
        if level is not None:
            pulumi.set(__self__, "level", level)
        if message is not None:
            pulumi.set(__self__, "message", message)
        if time is not None:
            pulumi.set(__self__, "time", time)

    @property
    @pulumi.getter
    def code(self) -> Optional[pulumi.Input[str]]:
        """
        Status code provided by the Extension
        """
        return pulumi.get(self, "code")

    @code.setter
    def code(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "code", value)

    @property
    @pulumi.getter(name="displayStatus")
    def display_status(self) -> Optional[pulumi.Input[str]]:
        """
        Short description of status of this instance of the extension.
        """
        return pulumi.get(self, "display_status")

    @display_status.setter
    def display_status(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "display_status", value)

    @property
    @pulumi.getter
    def level(self) -> Optional[pulumi.Input[Union[str, 'LevelType']]]:
        """
        Level of the status.
        """
        return pulumi.get(self, "level")

    @level.setter
    def level(self, value: Optional[pulumi.Input[Union[str, 'LevelType']]]):
        pulumi.set(self, "level", value)

    @property
    @pulumi.getter
    def message(self) -> Optional[pulumi.Input[str]]:
        """
        Detailed message of the status from the Extension instance.
        """
        return pulumi.get(self, "message")

    @message.setter
    def message(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "message", value)

    @property
    @pulumi.getter
    def time(self) -> Optional[pulumi.Input[str]]:
        """
        DateLiteral (per ISO8601) noting the time of installation status.
        """
        return pulumi.get(self, "time")

    @time.setter
    def time(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "time", value)


@pulumi.input_type
class GitRepositoryDefinitionArgs:
    def __init__(__self__, *,
                 https_ca_file: Optional[pulumi.Input[str]] = None,
                 https_user: Optional[pulumi.Input[str]] = None,
                 local_auth_ref: Optional[pulumi.Input[str]] = None,
                 repository_ref: Optional[pulumi.Input['RepositoryRefDefinitionArgs']] = None,
                 ssh_known_hosts: Optional[pulumi.Input[str]] = None,
                 sync_interval_in_seconds: Optional[pulumi.Input[float]] = None,
                 timeout_in_seconds: Optional[pulumi.Input[float]] = None,
                 url: Optional[pulumi.Input[str]] = None):
        """
        Parameters to reconcile to the GitRepository source kind type.
        :param pulumi.Input[str] https_ca_file: Base64-encoded HTTPS certificate authority contents used to access git private git repositories over HTTPS
        :param pulumi.Input[str] https_user: Base64-encoded HTTPS username used to access private git repositories over HTTPS
        :param pulumi.Input[str] local_auth_ref: Name of a local secret on the Kubernetes cluster to use as the authentication secret rather than the managed or user-provided configuration secrets.
        :param pulumi.Input['RepositoryRefDefinitionArgs'] repository_ref: The source reference for the GitRepository object.
        :param pulumi.Input[str] ssh_known_hosts: Base64-encoded known_hosts value containing public SSH keys required to access private git repositories over SSH
        :param pulumi.Input[float] sync_interval_in_seconds: The interval at which to re-reconcile the cluster git repository source with the remote.
        :param pulumi.Input[float] timeout_in_seconds: The maximum time to attempt to reconcile the cluster git repository source with the remote.
        :param pulumi.Input[str] url: The URL to sync for the flux configuration git repository.
        """
        if https_ca_file is not None:
            pulumi.set(__self__, "https_ca_file", https_ca_file)
        if https_user is not None:
            pulumi.set(__self__, "https_user", https_user)
        if local_auth_ref is not None:
            pulumi.set(__self__, "local_auth_ref", local_auth_ref)
        if repository_ref is not None:
            pulumi.set(__self__, "repository_ref", repository_ref)
        if ssh_known_hosts is not None:
            pulumi.set(__self__, "ssh_known_hosts", ssh_known_hosts)
        if sync_interval_in_seconds is None:
            sync_interval_in_seconds = 600
        if sync_interval_in_seconds is not None:
            pulumi.set(__self__, "sync_interval_in_seconds", sync_interval_in_seconds)
        if timeout_in_seconds is None:
            timeout_in_seconds = 600
        if timeout_in_seconds is not None:
            pulumi.set(__self__, "timeout_in_seconds", timeout_in_seconds)
        if url is not None:
            pulumi.set(__self__, "url", url)

    @property
    @pulumi.getter(name="httpsCAFile")
    def https_ca_file(self) -> Optional[pulumi.Input[str]]:
        """
        Base64-encoded HTTPS certificate authority contents used to access git private git repositories over HTTPS
        """
        return pulumi.get(self, "https_ca_file")

    @https_ca_file.setter
    def https_ca_file(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "https_ca_file", value)

    @property
    @pulumi.getter(name="httpsUser")
    def https_user(self) -> Optional[pulumi.Input[str]]:
        """
        Base64-encoded HTTPS username used to access private git repositories over HTTPS
        """
        return pulumi.get(self, "https_user")

    @https_user.setter
    def https_user(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "https_user", value)

    @property
    @pulumi.getter(name="localAuthRef")
    def local_auth_ref(self) -> Optional[pulumi.Input[str]]:
        """
        Name of a local secret on the Kubernetes cluster to use as the authentication secret rather than the managed or user-provided configuration secrets.
        """
        return pulumi.get(self, "local_auth_ref")

    @local_auth_ref.setter
    def local_auth_ref(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "local_auth_ref", value)

    @property
    @pulumi.getter(name="repositoryRef")
    def repository_ref(self) -> Optional[pulumi.Input['RepositoryRefDefinitionArgs']]:
        """
        The source reference for the GitRepository object.
        """
        return pulumi.get(self, "repository_ref")

    @repository_ref.setter
    def repository_ref(self, value: Optional[pulumi.Input['RepositoryRefDefinitionArgs']]):
        pulumi.set(self, "repository_ref", value)

    @property
    @pulumi.getter(name="sshKnownHosts")
    def ssh_known_hosts(self) -> Optional[pulumi.Input[str]]:
        """
        Base64-encoded known_hosts value containing public SSH keys required to access private git repositories over SSH
        """
        return pulumi.get(self, "ssh_known_hosts")

    @ssh_known_hosts.setter
    def ssh_known_hosts(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "ssh_known_hosts", value)

    @property
    @pulumi.getter(name="syncIntervalInSeconds")
    def sync_interval_in_seconds(self) -> Optional[pulumi.Input[float]]:
        """
        The interval at which to re-reconcile the cluster git repository source with the remote.
        """
        return pulumi.get(self, "sync_interval_in_seconds")

    @sync_interval_in_seconds.setter
    def sync_interval_in_seconds(self, value: Optional[pulumi.Input[float]]):
        pulumi.set(self, "sync_interval_in_seconds", value)

    @property
    @pulumi.getter(name="timeoutInSeconds")
    def timeout_in_seconds(self) -> Optional[pulumi.Input[float]]:
        """
        The maximum time to attempt to reconcile the cluster git repository source with the remote.
        """
        return pulumi.get(self, "timeout_in_seconds")

    @timeout_in_seconds.setter
    def timeout_in_seconds(self, value: Optional[pulumi.Input[float]]):
        pulumi.set(self, "timeout_in_seconds", value)

    @property
    @pulumi.getter
    def url(self) -> Optional[pulumi.Input[str]]:
        """
        The URL to sync for the flux configuration git repository.
        """
        return pulumi.get(self, "url")

    @url.setter
    def url(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "url", value)


@pulumi.input_type
class HelmOperatorPropertiesArgs:
    def __init__(__self__, *,
                 chart_values: Optional[pulumi.Input[str]] = None,
                 chart_version: Optional[pulumi.Input[str]] = None):
        """
        Properties for Helm operator.
        :param pulumi.Input[str] chart_values: Values override for the operator Helm chart.
        :param pulumi.Input[str] chart_version: Version of the operator Helm chart.
        """
        if chart_values is not None:
            pulumi.set(__self__, "chart_values", chart_values)
        if chart_version is not None:
            pulumi.set(__self__, "chart_version", chart_version)

    @property
    @pulumi.getter(name="chartValues")
    def chart_values(self) -> Optional[pulumi.Input[str]]:
        """
        Values override for the operator Helm chart.
        """
        return pulumi.get(self, "chart_values")

    @chart_values.setter
    def chart_values(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "chart_values", value)

    @property
    @pulumi.getter(name="chartVersion")
    def chart_version(self) -> Optional[pulumi.Input[str]]:
        """
        Version of the operator Helm chart.
        """
        return pulumi.get(self, "chart_version")

    @chart_version.setter
    def chart_version(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "chart_version", value)


@pulumi.input_type
class KubernetesConfigurationPrivateLinkScopePropertiesArgs:
    def __init__(__self__, *,
                 cluster_resource_id: pulumi.Input[str],
                 public_network_access: Optional[pulumi.Input[Union[str, 'PublicNetworkAccessType']]] = None):
        """
        Properties that define a Azure Arc PrivateLinkScope resource.
        :param pulumi.Input[str] cluster_resource_id: Managed Cluster ARM ID for the private link scope  (Required)
        :param pulumi.Input[Union[str, 'PublicNetworkAccessType']] public_network_access: Indicates whether machines associated with the private link scope can also use public Azure Arc service endpoints.
        """
        pulumi.set(__self__, "cluster_resource_id", cluster_resource_id)
        if public_network_access is not None:
            pulumi.set(__self__, "public_network_access", public_network_access)

    @property
    @pulumi.getter(name="clusterResourceId")
    def cluster_resource_id(self) -> pulumi.Input[str]:
        """
        Managed Cluster ARM ID for the private link scope  (Required)
        """
        return pulumi.get(self, "cluster_resource_id")

    @cluster_resource_id.setter
    def cluster_resource_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "cluster_resource_id", value)

    @property
    @pulumi.getter(name="publicNetworkAccess")
    def public_network_access(self) -> Optional[pulumi.Input[Union[str, 'PublicNetworkAccessType']]]:
        """
        Indicates whether machines associated with the private link scope can also use public Azure Arc service endpoints.
        """
        return pulumi.get(self, "public_network_access")

    @public_network_access.setter
    def public_network_access(self, value: Optional[pulumi.Input[Union[str, 'PublicNetworkAccessType']]]):
        pulumi.set(self, "public_network_access", value)


@pulumi.input_type
class KustomizationDefinitionArgs:
    def __init__(__self__, *,
                 depends_on: Optional[pulumi.Input[Sequence[pulumi.Input['DependsOnDefinitionArgs']]]] = None,
                 force: Optional[pulumi.Input[bool]] = None,
                 path: Optional[pulumi.Input[str]] = None,
                 prune: Optional[pulumi.Input[bool]] = None,
                 retry_interval_in_seconds: Optional[pulumi.Input[float]] = None,
                 sync_interval_in_seconds: Optional[pulumi.Input[float]] = None,
                 timeout_in_seconds: Optional[pulumi.Input[float]] = None,
                 validation: Optional[pulumi.Input[Union[str, 'KustomizationValidationType']]] = None):
        """
        The Kustomization defining how to reconcile the artifact pulled by the source type on the cluster.
        :param pulumi.Input[Sequence[pulumi.Input['DependsOnDefinitionArgs']]] depends_on: Specifies other Kustomizations that this Kustomization depends on. This Kustomization will not reconcile until all dependencies have completed their reconciliation.
        :param pulumi.Input[bool] force: Enable/disable re-creating Kubernetes resources on the cluster when patching fails due to an immutable field change.
        :param pulumi.Input[str] path: The path in the source reference to reconcile on the cluster.
        :param pulumi.Input[bool] prune: Enable/disable garbage collections of Kubernetes objects created by this Kustomization.
        :param pulumi.Input[float] retry_interval_in_seconds: The interval at which to re-reconcile the Kustomization on the cluster in the event of failure on reconciliation.
        :param pulumi.Input[float] sync_interval_in_seconds: The interval at which to re-reconcile the Kustomization on the cluster.
        :param pulumi.Input[float] timeout_in_seconds: The maximum time to attempt to reconcile the Kustomization on the cluster.
        :param pulumi.Input[Union[str, 'KustomizationValidationType']] validation: Specify whether to validate the Kubernetes objects referenced in the Kustomization before applying them to the cluster.
        """
        if depends_on is not None:
            pulumi.set(__self__, "depends_on", depends_on)
        if force is None:
            force = False
        if force is not None:
            pulumi.set(__self__, "force", force)
        if path is None:
            path = ''
        if path is not None:
            pulumi.set(__self__, "path", path)
        if prune is None:
            prune = False
        if prune is not None:
            pulumi.set(__self__, "prune", prune)
        if retry_interval_in_seconds is not None:
            pulumi.set(__self__, "retry_interval_in_seconds", retry_interval_in_seconds)
        if sync_interval_in_seconds is None:
            sync_interval_in_seconds = 600
        if sync_interval_in_seconds is not None:
            pulumi.set(__self__, "sync_interval_in_seconds", sync_interval_in_seconds)
        if timeout_in_seconds is None:
            timeout_in_seconds = 600
        if timeout_in_seconds is not None:
            pulumi.set(__self__, "timeout_in_seconds", timeout_in_seconds)
        if validation is not None:
            pulumi.set(__self__, "validation", validation)

    @property
    @pulumi.getter(name="dependsOn")
    def depends_on(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['DependsOnDefinitionArgs']]]]:
        """
        Specifies other Kustomizations that this Kustomization depends on. This Kustomization will not reconcile until all dependencies have completed their reconciliation.
        """
        return pulumi.get(self, "depends_on")

    @depends_on.setter
    def depends_on(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['DependsOnDefinitionArgs']]]]):
        pulumi.set(self, "depends_on", value)

    @property
    @pulumi.getter
    def force(self) -> Optional[pulumi.Input[bool]]:
        """
        Enable/disable re-creating Kubernetes resources on the cluster when patching fails due to an immutable field change.
        """
        return pulumi.get(self, "force")

    @force.setter
    def force(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "force", value)

    @property
    @pulumi.getter
    def path(self) -> Optional[pulumi.Input[str]]:
        """
        The path in the source reference to reconcile on the cluster.
        """
        return pulumi.get(self, "path")

    @path.setter
    def path(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "path", value)

    @property
    @pulumi.getter
    def prune(self) -> Optional[pulumi.Input[bool]]:
        """
        Enable/disable garbage collections of Kubernetes objects created by this Kustomization.
        """
        return pulumi.get(self, "prune")

    @prune.setter
    def prune(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "prune", value)

    @property
    @pulumi.getter(name="retryIntervalInSeconds")
    def retry_interval_in_seconds(self) -> Optional[pulumi.Input[float]]:
        """
        The interval at which to re-reconcile the Kustomization on the cluster in the event of failure on reconciliation.
        """
        return pulumi.get(self, "retry_interval_in_seconds")

    @retry_interval_in_seconds.setter
    def retry_interval_in_seconds(self, value: Optional[pulumi.Input[float]]):
        pulumi.set(self, "retry_interval_in_seconds", value)

    @property
    @pulumi.getter(name="syncIntervalInSeconds")
    def sync_interval_in_seconds(self) -> Optional[pulumi.Input[float]]:
        """
        The interval at which to re-reconcile the Kustomization on the cluster.
        """
        return pulumi.get(self, "sync_interval_in_seconds")

    @sync_interval_in_seconds.setter
    def sync_interval_in_seconds(self, value: Optional[pulumi.Input[float]]):
        pulumi.set(self, "sync_interval_in_seconds", value)

    @property
    @pulumi.getter(name="timeoutInSeconds")
    def timeout_in_seconds(self) -> Optional[pulumi.Input[float]]:
        """
        The maximum time to attempt to reconcile the Kustomization on the cluster.
        """
        return pulumi.get(self, "timeout_in_seconds")

    @timeout_in_seconds.setter
    def timeout_in_seconds(self, value: Optional[pulumi.Input[float]]):
        pulumi.set(self, "timeout_in_seconds", value)

    @property
    @pulumi.getter
    def validation(self) -> Optional[pulumi.Input[Union[str, 'KustomizationValidationType']]]:
        """
        Specify whether to validate the Kubernetes objects referenced in the Kustomization before applying them to the cluster.
        """
        return pulumi.get(self, "validation")

    @validation.setter
    def validation(self, value: Optional[pulumi.Input[Union[str, 'KustomizationValidationType']]]):
        pulumi.set(self, "validation", value)


@pulumi.input_type
class PrivateLinkServiceConnectionStateArgs:
    def __init__(__self__, *,
                 actions_required: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 status: Optional[pulumi.Input[Union[str, 'PrivateEndpointServiceConnectionStatus']]] = None):
        """
        A collection of information about the state of the connection between service consumer and provider.
        :param pulumi.Input[str] actions_required: A message indicating if changes on the service provider require any updates on the consumer.
        :param pulumi.Input[str] description: The reason for approval/rejection of the connection.
        :param pulumi.Input[Union[str, 'PrivateEndpointServiceConnectionStatus']] status: Indicates whether the connection has been Approved/Rejected/Removed by the owner of the service.
        """
        if actions_required is not None:
            pulumi.set(__self__, "actions_required", actions_required)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if status is not None:
            pulumi.set(__self__, "status", status)

    @property
    @pulumi.getter(name="actionsRequired")
    def actions_required(self) -> Optional[pulumi.Input[str]]:
        """
        A message indicating if changes on the service provider require any updates on the consumer.
        """
        return pulumi.get(self, "actions_required")

    @actions_required.setter
    def actions_required(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "actions_required", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        The reason for approval/rejection of the connection.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter
    def status(self) -> Optional[pulumi.Input[Union[str, 'PrivateEndpointServiceConnectionStatus']]]:
        """
        Indicates whether the connection has been Approved/Rejected/Removed by the owner of the service.
        """
        return pulumi.get(self, "status")

    @status.setter
    def status(self, value: Optional[pulumi.Input[Union[str, 'PrivateEndpointServiceConnectionStatus']]]):
        pulumi.set(self, "status", value)


@pulumi.input_type
class RepositoryRefDefinitionArgs:
    def __init__(__self__, *,
                 branch: Optional[pulumi.Input[str]] = None,
                 commit: Optional[pulumi.Input[str]] = None,
                 semver: Optional[pulumi.Input[str]] = None,
                 tag: Optional[pulumi.Input[str]] = None):
        """
        The source reference for the GitRepository object.
        :param pulumi.Input[str] branch: The git repository branch name to checkout.
        :param pulumi.Input[str] commit: The commit SHA to checkout. This value must be combined with the branch name to be valid. This takes precedence over semver.
        :param pulumi.Input[str] semver: The semver range used to match against git repository tags. This takes precedence over tag.
        :param pulumi.Input[str] tag: The git repository tag name to checkout. This takes precedence over branch.
        """
        if branch is not None:
            pulumi.set(__self__, "branch", branch)
        if commit is not None:
            pulumi.set(__self__, "commit", commit)
        if semver is not None:
            pulumi.set(__self__, "semver", semver)
        if tag is not None:
            pulumi.set(__self__, "tag", tag)

    @property
    @pulumi.getter
    def branch(self) -> Optional[pulumi.Input[str]]:
        """
        The git repository branch name to checkout.
        """
        return pulumi.get(self, "branch")

    @branch.setter
    def branch(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "branch", value)

    @property
    @pulumi.getter
    def commit(self) -> Optional[pulumi.Input[str]]:
        """
        The commit SHA to checkout. This value must be combined with the branch name to be valid. This takes precedence over semver.
        """
        return pulumi.get(self, "commit")

    @commit.setter
    def commit(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "commit", value)

    @property
    @pulumi.getter
    def semver(self) -> Optional[pulumi.Input[str]]:
        """
        The semver range used to match against git repository tags. This takes precedence over tag.
        """
        return pulumi.get(self, "semver")

    @semver.setter
    def semver(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "semver", value)

    @property
    @pulumi.getter
    def tag(self) -> Optional[pulumi.Input[str]]:
        """
        The git repository tag name to checkout. This takes precedence over branch.
        """
        return pulumi.get(self, "tag")

    @tag.setter
    def tag(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "tag", value)


@pulumi.input_type
class ScopeClusterArgs:
    def __init__(__self__, *,
                 release_namespace: Optional[pulumi.Input[str]] = None):
        """
        Specifies that the scope of the extensionInstance is Cluster
        :param pulumi.Input[str] release_namespace: Namespace where the extension Release must be placed, for a Cluster scoped extensionInstance.  If this namespace does not exist, it will be created
        """
        if release_namespace is not None:
            pulumi.set(__self__, "release_namespace", release_namespace)

    @property
    @pulumi.getter(name="releaseNamespace")
    def release_namespace(self) -> Optional[pulumi.Input[str]]:
        """
        Namespace where the extension Release must be placed, for a Cluster scoped extensionInstance.  If this namespace does not exist, it will be created
        """
        return pulumi.get(self, "release_namespace")

    @release_namespace.setter
    def release_namespace(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "release_namespace", value)


@pulumi.input_type
class ScopeNamespaceArgs:
    def __init__(__self__, *,
                 target_namespace: Optional[pulumi.Input[str]] = None):
        """
        Specifies that the scope of the extensionInstance is Namespace
        :param pulumi.Input[str] target_namespace: Namespace where the extensionInstance will be created for an Namespace scoped extensionInstance.  If this namespace does not exist, it will be created
        """
        if target_namespace is not None:
            pulumi.set(__self__, "target_namespace", target_namespace)

    @property
    @pulumi.getter(name="targetNamespace")
    def target_namespace(self) -> Optional[pulumi.Input[str]]:
        """
        Namespace where the extensionInstance will be created for an Namespace scoped extensionInstance.  If this namespace does not exist, it will be created
        """
        return pulumi.get(self, "target_namespace")

    @target_namespace.setter
    def target_namespace(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "target_namespace", value)


@pulumi.input_type
class ScopeArgs:
    def __init__(__self__, *,
                 cluster: Optional[pulumi.Input['ScopeClusterArgs']] = None,
                 namespace: Optional[pulumi.Input['ScopeNamespaceArgs']] = None):
        """
        Scope of the extensionInstance. It can be either Cluster or Namespace; but not both.
        :param pulumi.Input['ScopeClusterArgs'] cluster: Specifies that the scope of the extensionInstance is Cluster
        :param pulumi.Input['ScopeNamespaceArgs'] namespace: Specifies that the scope of the extensionInstance is Namespace
        """
        if cluster is not None:
            pulumi.set(__self__, "cluster", cluster)
        if namespace is not None:
            pulumi.set(__self__, "namespace", namespace)

    @property
    @pulumi.getter
    def cluster(self) -> Optional[pulumi.Input['ScopeClusterArgs']]:
        """
        Specifies that the scope of the extensionInstance is Cluster
        """
        return pulumi.get(self, "cluster")

    @cluster.setter
    def cluster(self, value: Optional[pulumi.Input['ScopeClusterArgs']]):
        pulumi.set(self, "cluster", value)

    @property
    @pulumi.getter
    def namespace(self) -> Optional[pulumi.Input['ScopeNamespaceArgs']]:
        """
        Specifies that the scope of the extensionInstance is Namespace
        """
        return pulumi.get(self, "namespace")

    @namespace.setter
    def namespace(self, value: Optional[pulumi.Input['ScopeNamespaceArgs']]):
        pulumi.set(self, "namespace", value)


