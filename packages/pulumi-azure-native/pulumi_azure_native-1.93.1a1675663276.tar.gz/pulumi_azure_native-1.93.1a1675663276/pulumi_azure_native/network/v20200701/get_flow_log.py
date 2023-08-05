# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from . import outputs

__all__ = [
    'GetFlowLogResult',
    'AwaitableGetFlowLogResult',
    'get_flow_log',
    'get_flow_log_output',
]

@pulumi.output_type
class GetFlowLogResult:
    """
    A flow log resource.
    """
    def __init__(__self__, enabled=None, etag=None, flow_analytics_configuration=None, format=None, id=None, location=None, name=None, provisioning_state=None, retention_policy=None, storage_id=None, tags=None, target_resource_guid=None, target_resource_id=None, type=None):
        if enabled and not isinstance(enabled, bool):
            raise TypeError("Expected argument 'enabled' to be a bool")
        pulumi.set(__self__, "enabled", enabled)
        if etag and not isinstance(etag, str):
            raise TypeError("Expected argument 'etag' to be a str")
        pulumi.set(__self__, "etag", etag)
        if flow_analytics_configuration and not isinstance(flow_analytics_configuration, dict):
            raise TypeError("Expected argument 'flow_analytics_configuration' to be a dict")
        pulumi.set(__self__, "flow_analytics_configuration", flow_analytics_configuration)
        if format and not isinstance(format, dict):
            raise TypeError("Expected argument 'format' to be a dict")
        pulumi.set(__self__, "format", format)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if location and not isinstance(location, str):
            raise TypeError("Expected argument 'location' to be a str")
        pulumi.set(__self__, "location", location)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if provisioning_state and not isinstance(provisioning_state, str):
            raise TypeError("Expected argument 'provisioning_state' to be a str")
        pulumi.set(__self__, "provisioning_state", provisioning_state)
        if retention_policy and not isinstance(retention_policy, dict):
            raise TypeError("Expected argument 'retention_policy' to be a dict")
        pulumi.set(__self__, "retention_policy", retention_policy)
        if storage_id and not isinstance(storage_id, str):
            raise TypeError("Expected argument 'storage_id' to be a str")
        pulumi.set(__self__, "storage_id", storage_id)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)
        if target_resource_guid and not isinstance(target_resource_guid, str):
            raise TypeError("Expected argument 'target_resource_guid' to be a str")
        pulumi.set(__self__, "target_resource_guid", target_resource_guid)
        if target_resource_id and not isinstance(target_resource_id, str):
            raise TypeError("Expected argument 'target_resource_id' to be a str")
        pulumi.set(__self__, "target_resource_id", target_resource_id)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter
    def enabled(self) -> Optional[bool]:
        """
        Flag to enable/disable flow logging.
        """
        return pulumi.get(self, "enabled")

    @property
    @pulumi.getter
    def etag(self) -> str:
        """
        A unique read-only string that changes whenever the resource is updated.
        """
        return pulumi.get(self, "etag")

    @property
    @pulumi.getter(name="flowAnalyticsConfiguration")
    def flow_analytics_configuration(self) -> Optional['outputs.TrafficAnalyticsPropertiesResponse']:
        """
        Parameters that define the configuration of traffic analytics.
        """
        return pulumi.get(self, "flow_analytics_configuration")

    @property
    @pulumi.getter
    def format(self) -> Optional['outputs.FlowLogFormatParametersResponse']:
        """
        Parameters that define the flow log format.
        """
        return pulumi.get(self, "format")

    @property
    @pulumi.getter
    def id(self) -> Optional[str]:
        """
        Resource ID.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def location(self) -> Optional[str]:
        """
        Resource location.
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Resource name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> str:
        """
        The provisioning state of the flow log.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter(name="retentionPolicy")
    def retention_policy(self) -> Optional['outputs.RetentionPolicyParametersResponse']:
        """
        Parameters that define the retention policy for flow log.
        """
        return pulumi.get(self, "retention_policy")

    @property
    @pulumi.getter(name="storageId")
    def storage_id(self) -> str:
        """
        ID of the storage account which is used to store the flow log.
        """
        return pulumi.get(self, "storage_id")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Mapping[str, str]]:
        """
        Resource tags.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="targetResourceGuid")
    def target_resource_guid(self) -> str:
        """
        Guid of network security group to which flow log will be applied.
        """
        return pulumi.get(self, "target_resource_guid")

    @property
    @pulumi.getter(name="targetResourceId")
    def target_resource_id(self) -> str:
        """
        ID of network security group to which flow log will be applied.
        """
        return pulumi.get(self, "target_resource_id")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        Resource type.
        """
        return pulumi.get(self, "type")


class AwaitableGetFlowLogResult(GetFlowLogResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetFlowLogResult(
            enabled=self.enabled,
            etag=self.etag,
            flow_analytics_configuration=self.flow_analytics_configuration,
            format=self.format,
            id=self.id,
            location=self.location,
            name=self.name,
            provisioning_state=self.provisioning_state,
            retention_policy=self.retention_policy,
            storage_id=self.storage_id,
            tags=self.tags,
            target_resource_guid=self.target_resource_guid,
            target_resource_id=self.target_resource_id,
            type=self.type)


def get_flow_log(flow_log_name: Optional[str] = None,
                 network_watcher_name: Optional[str] = None,
                 resource_group_name: Optional[str] = None,
                 opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetFlowLogResult:
    """
    A flow log resource.


    :param str flow_log_name: The name of the flow log resource.
    :param str network_watcher_name: The name of the network watcher.
    :param str resource_group_name: The name of the resource group.
    """
    __args__ = dict()
    __args__['flowLogName'] = flow_log_name
    __args__['networkWatcherName'] = network_watcher_name
    __args__['resourceGroupName'] = resource_group_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:network/v20200701:getFlowLog', __args__, opts=opts, typ=GetFlowLogResult).value

    return AwaitableGetFlowLogResult(
        enabled=__ret__.enabled,
        etag=__ret__.etag,
        flow_analytics_configuration=__ret__.flow_analytics_configuration,
        format=__ret__.format,
        id=__ret__.id,
        location=__ret__.location,
        name=__ret__.name,
        provisioning_state=__ret__.provisioning_state,
        retention_policy=__ret__.retention_policy,
        storage_id=__ret__.storage_id,
        tags=__ret__.tags,
        target_resource_guid=__ret__.target_resource_guid,
        target_resource_id=__ret__.target_resource_id,
        type=__ret__.type)


@_utilities.lift_output_func(get_flow_log)
def get_flow_log_output(flow_log_name: Optional[pulumi.Input[str]] = None,
                        network_watcher_name: Optional[pulumi.Input[str]] = None,
                        resource_group_name: Optional[pulumi.Input[str]] = None,
                        opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetFlowLogResult]:
    """
    A flow log resource.


    :param str flow_log_name: The name of the flow log resource.
    :param str network_watcher_name: The name of the network watcher.
    :param str resource_group_name: The name of the resource group.
    """
    ...
