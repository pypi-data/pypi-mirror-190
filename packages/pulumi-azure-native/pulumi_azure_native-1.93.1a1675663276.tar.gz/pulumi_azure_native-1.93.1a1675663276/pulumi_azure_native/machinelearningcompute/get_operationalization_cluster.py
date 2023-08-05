# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
from . import outputs

__all__ = [
    'GetOperationalizationClusterResult',
    'AwaitableGetOperationalizationClusterResult',
    'get_operationalization_cluster',
    'get_operationalization_cluster_output',
]

@pulumi.output_type
class GetOperationalizationClusterResult:
    """
    Instance of an Azure ML Operationalization Cluster resource.
    """
    def __init__(__self__, app_insights=None, cluster_type=None, container_registry=None, container_service=None, created_on=None, description=None, global_service_configuration=None, id=None, location=None, modified_on=None, name=None, provisioning_errors=None, provisioning_state=None, storage_account=None, tags=None, type=None):
        if app_insights and not isinstance(app_insights, dict):
            raise TypeError("Expected argument 'app_insights' to be a dict")
        pulumi.set(__self__, "app_insights", app_insights)
        if cluster_type and not isinstance(cluster_type, str):
            raise TypeError("Expected argument 'cluster_type' to be a str")
        pulumi.set(__self__, "cluster_type", cluster_type)
        if container_registry and not isinstance(container_registry, dict):
            raise TypeError("Expected argument 'container_registry' to be a dict")
        pulumi.set(__self__, "container_registry", container_registry)
        if container_service and not isinstance(container_service, dict):
            raise TypeError("Expected argument 'container_service' to be a dict")
        pulumi.set(__self__, "container_service", container_service)
        if created_on and not isinstance(created_on, str):
            raise TypeError("Expected argument 'created_on' to be a str")
        pulumi.set(__self__, "created_on", created_on)
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, "description", description)
        if global_service_configuration and not isinstance(global_service_configuration, dict):
            raise TypeError("Expected argument 'global_service_configuration' to be a dict")
        pulumi.set(__self__, "global_service_configuration", global_service_configuration)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if location and not isinstance(location, str):
            raise TypeError("Expected argument 'location' to be a str")
        pulumi.set(__self__, "location", location)
        if modified_on and not isinstance(modified_on, str):
            raise TypeError("Expected argument 'modified_on' to be a str")
        pulumi.set(__self__, "modified_on", modified_on)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if provisioning_errors and not isinstance(provisioning_errors, list):
            raise TypeError("Expected argument 'provisioning_errors' to be a list")
        pulumi.set(__self__, "provisioning_errors", provisioning_errors)
        if provisioning_state and not isinstance(provisioning_state, str):
            raise TypeError("Expected argument 'provisioning_state' to be a str")
        pulumi.set(__self__, "provisioning_state", provisioning_state)
        if storage_account and not isinstance(storage_account, dict):
            raise TypeError("Expected argument 'storage_account' to be a dict")
        pulumi.set(__self__, "storage_account", storage_account)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter(name="appInsights")
    def app_insights(self) -> Optional['outputs.AppInsightsPropertiesResponse']:
        """
        AppInsights configuration.
        """
        return pulumi.get(self, "app_insights")

    @property
    @pulumi.getter(name="clusterType")
    def cluster_type(self) -> str:
        """
        The cluster type.
        """
        return pulumi.get(self, "cluster_type")

    @property
    @pulumi.getter(name="containerRegistry")
    def container_registry(self) -> Optional['outputs.ContainerRegistryPropertiesResponse']:
        """
        Container Registry properties.
        """
        return pulumi.get(self, "container_registry")

    @property
    @pulumi.getter(name="containerService")
    def container_service(self) -> Optional['outputs.AcsClusterPropertiesResponse']:
        """
        Parameters for the Azure Container Service cluster.
        """
        return pulumi.get(self, "container_service")

    @property
    @pulumi.getter(name="createdOn")
    def created_on(self) -> str:
        """
        The date and time when the cluster was created.
        """
        return pulumi.get(self, "created_on")

    @property
    @pulumi.getter
    def description(self) -> Optional[str]:
        """
        The description of the cluster.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="globalServiceConfiguration")
    def global_service_configuration(self) -> Optional['outputs.GlobalServiceConfigurationResponse']:
        """
        Contains global configuration for the web services in the cluster.
        """
        return pulumi.get(self, "global_service_configuration")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Specifies the resource ID.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def location(self) -> str:
        """
        Specifies the location of the resource.
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter(name="modifiedOn")
    def modified_on(self) -> str:
        """
        The date and time when the cluster was last modified.
        """
        return pulumi.get(self, "modified_on")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Specifies the name of the resource.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="provisioningErrors")
    def provisioning_errors(self) -> Sequence['outputs.ErrorResponseWrapperResponse']:
        """
        List of provisioning errors reported by the resource provider.
        """
        return pulumi.get(self, "provisioning_errors")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> str:
        """
        The provision state of the cluster. Valid values are Unknown, Updating, Provisioning, Succeeded, and Failed.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter(name="storageAccount")
    def storage_account(self) -> Optional['outputs.StorageAccountPropertiesResponse']:
        """
        Storage Account properties.
        """
        return pulumi.get(self, "storage_account")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Mapping[str, str]]:
        """
        Contains resource tags defined as key/value pairs.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        Specifies the type of the resource.
        """
        return pulumi.get(self, "type")


class AwaitableGetOperationalizationClusterResult(GetOperationalizationClusterResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetOperationalizationClusterResult(
            app_insights=self.app_insights,
            cluster_type=self.cluster_type,
            container_registry=self.container_registry,
            container_service=self.container_service,
            created_on=self.created_on,
            description=self.description,
            global_service_configuration=self.global_service_configuration,
            id=self.id,
            location=self.location,
            modified_on=self.modified_on,
            name=self.name,
            provisioning_errors=self.provisioning_errors,
            provisioning_state=self.provisioning_state,
            storage_account=self.storage_account,
            tags=self.tags,
            type=self.type)


def get_operationalization_cluster(cluster_name: Optional[str] = None,
                                   resource_group_name: Optional[str] = None,
                                   opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetOperationalizationClusterResult:
    """
    Instance of an Azure ML Operationalization Cluster resource.
    API Version: 2017-08-01-preview.


    :param str cluster_name: The name of the cluster.
    :param str resource_group_name: Name of the resource group in which the cluster is located.
    """
    __args__ = dict()
    __args__['clusterName'] = cluster_name
    __args__['resourceGroupName'] = resource_group_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:machinelearningcompute:getOperationalizationCluster', __args__, opts=opts, typ=GetOperationalizationClusterResult).value

    return AwaitableGetOperationalizationClusterResult(
        app_insights=__ret__.app_insights,
        cluster_type=__ret__.cluster_type,
        container_registry=__ret__.container_registry,
        container_service=__ret__.container_service,
        created_on=__ret__.created_on,
        description=__ret__.description,
        global_service_configuration=__ret__.global_service_configuration,
        id=__ret__.id,
        location=__ret__.location,
        modified_on=__ret__.modified_on,
        name=__ret__.name,
        provisioning_errors=__ret__.provisioning_errors,
        provisioning_state=__ret__.provisioning_state,
        storage_account=__ret__.storage_account,
        tags=__ret__.tags,
        type=__ret__.type)


@_utilities.lift_output_func(get_operationalization_cluster)
def get_operationalization_cluster_output(cluster_name: Optional[pulumi.Input[str]] = None,
                                          resource_group_name: Optional[pulumi.Input[str]] = None,
                                          opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetOperationalizationClusterResult]:
    """
    Instance of an Azure ML Operationalization Cluster resource.
    API Version: 2017-08-01-preview.


    :param str cluster_name: The name of the cluster.
    :param str resource_group_name: Name of the resource group in which the cluster is located.
    """
    ...
