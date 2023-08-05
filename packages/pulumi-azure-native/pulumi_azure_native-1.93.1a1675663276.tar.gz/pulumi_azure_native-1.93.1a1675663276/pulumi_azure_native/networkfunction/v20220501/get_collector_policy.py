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
    'GetCollectorPolicyResult',
    'AwaitableGetCollectorPolicyResult',
    'get_collector_policy',
    'get_collector_policy_output',
]

@pulumi.output_type
class GetCollectorPolicyResult:
    """
    Collector policy resource.
    """
    def __init__(__self__, emission_policies=None, etag=None, id=None, ingestion_policy=None, name=None, provisioning_state=None, system_data=None, type=None):
        if emission_policies and not isinstance(emission_policies, list):
            raise TypeError("Expected argument 'emission_policies' to be a list")
        pulumi.set(__self__, "emission_policies", emission_policies)
        if etag and not isinstance(etag, str):
            raise TypeError("Expected argument 'etag' to be a str")
        pulumi.set(__self__, "etag", etag)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if ingestion_policy and not isinstance(ingestion_policy, dict):
            raise TypeError("Expected argument 'ingestion_policy' to be a dict")
        pulumi.set(__self__, "ingestion_policy", ingestion_policy)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if provisioning_state and not isinstance(provisioning_state, str):
            raise TypeError("Expected argument 'provisioning_state' to be a str")
        pulumi.set(__self__, "provisioning_state", provisioning_state)
        if system_data and not isinstance(system_data, dict):
            raise TypeError("Expected argument 'system_data' to be a dict")
        pulumi.set(__self__, "system_data", system_data)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter(name="emissionPolicies")
    def emission_policies(self) -> Optional[Sequence['outputs.EmissionPoliciesPropertiesFormatResponse']]:
        """
        Emission policies.
        """
        return pulumi.get(self, "emission_policies")

    @property
    @pulumi.getter
    def etag(self) -> str:
        """
        A unique read-only string that changes whenever the resource is updated.
        """
        return pulumi.get(self, "etag")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Azure resource Id
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="ingestionPolicy")
    def ingestion_policy(self) -> Optional['outputs.IngestionPolicyPropertiesFormatResponse']:
        """
        Ingestion policies.
        """
        return pulumi.get(self, "ingestion_policy")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Azure resource name
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> str:
        """
        The provisioning state.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter(name="systemData")
    def system_data(self) -> 'outputs.CollectorPolicyResponseSystemData':
        """
        Metadata pertaining to creation and last modification of the resource.
        """
        return pulumi.get(self, "system_data")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        Azure resource type
        """
        return pulumi.get(self, "type")


class AwaitableGetCollectorPolicyResult(GetCollectorPolicyResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetCollectorPolicyResult(
            emission_policies=self.emission_policies,
            etag=self.etag,
            id=self.id,
            ingestion_policy=self.ingestion_policy,
            name=self.name,
            provisioning_state=self.provisioning_state,
            system_data=self.system_data,
            type=self.type)


def get_collector_policy(azure_traffic_collector_name: Optional[str] = None,
                         collector_policy_name: Optional[str] = None,
                         resource_group_name: Optional[str] = None,
                         opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetCollectorPolicyResult:
    """
    Collector policy resource.


    :param str azure_traffic_collector_name: Azure Traffic Collector name
    :param str collector_policy_name: Collector Policy Name
    :param str resource_group_name: The name of the resource group.
    """
    __args__ = dict()
    __args__['azureTrafficCollectorName'] = azure_traffic_collector_name
    __args__['collectorPolicyName'] = collector_policy_name
    __args__['resourceGroupName'] = resource_group_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:networkfunction/v20220501:getCollectorPolicy', __args__, opts=opts, typ=GetCollectorPolicyResult).value

    return AwaitableGetCollectorPolicyResult(
        emission_policies=__ret__.emission_policies,
        etag=__ret__.etag,
        id=__ret__.id,
        ingestion_policy=__ret__.ingestion_policy,
        name=__ret__.name,
        provisioning_state=__ret__.provisioning_state,
        system_data=__ret__.system_data,
        type=__ret__.type)


@_utilities.lift_output_func(get_collector_policy)
def get_collector_policy_output(azure_traffic_collector_name: Optional[pulumi.Input[str]] = None,
                                collector_policy_name: Optional[pulumi.Input[str]] = None,
                                resource_group_name: Optional[pulumi.Input[str]] = None,
                                opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetCollectorPolicyResult]:
    """
    Collector policy resource.


    :param str azure_traffic_collector_name: Azure Traffic Collector name
    :param str collector_policy_name: Collector Policy Name
    :param str resource_group_name: The name of the resource group.
    """
    ...
