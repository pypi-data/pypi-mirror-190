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
    'GetLinkerResult',
    'AwaitableGetLinkerResult',
    'get_linker',
    'get_linker_output',
]

@pulumi.output_type
class GetLinkerResult:
    """
    Linker of source and target resource
    """
    def __init__(__self__, auth_info=None, client_type=None, id=None, name=None, provisioning_state=None, secret_store=None, system_data=None, target_id=None, type=None, v_net_solution=None):
        if auth_info and not isinstance(auth_info, dict):
            raise TypeError("Expected argument 'auth_info' to be a dict")
        pulumi.set(__self__, "auth_info", auth_info)
        if client_type and not isinstance(client_type, str):
            raise TypeError("Expected argument 'client_type' to be a str")
        pulumi.set(__self__, "client_type", client_type)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if provisioning_state and not isinstance(provisioning_state, str):
            raise TypeError("Expected argument 'provisioning_state' to be a str")
        pulumi.set(__self__, "provisioning_state", provisioning_state)
        if secret_store and not isinstance(secret_store, dict):
            raise TypeError("Expected argument 'secret_store' to be a dict")
        pulumi.set(__self__, "secret_store", secret_store)
        if system_data and not isinstance(system_data, dict):
            raise TypeError("Expected argument 'system_data' to be a dict")
        pulumi.set(__self__, "system_data", system_data)
        if target_id and not isinstance(target_id, str):
            raise TypeError("Expected argument 'target_id' to be a str")
        pulumi.set(__self__, "target_id", target_id)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)
        if v_net_solution and not isinstance(v_net_solution, dict):
            raise TypeError("Expected argument 'v_net_solution' to be a dict")
        pulumi.set(__self__, "v_net_solution", v_net_solution)

    @property
    @pulumi.getter(name="authInfo")
    def auth_info(self) -> Optional[Any]:
        """
        The authentication type.
        """
        return pulumi.get(self, "auth_info")

    @property
    @pulumi.getter(name="clientType")
    def client_type(self) -> Optional[str]:
        """
        The application client type
        """
        return pulumi.get(self, "client_type")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Fully qualified resource ID for the resource. Ex - /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/{resourceProviderNamespace}/{resourceType}/{resourceName}
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The name of the resource
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
    @pulumi.getter(name="secretStore")
    def secret_store(self) -> Optional['outputs.SecretStoreResponse']:
        """
        An option to store secret value in secure place
        """
        return pulumi.get(self, "secret_store")

    @property
    @pulumi.getter(name="systemData")
    def system_data(self) -> 'outputs.SystemDataResponse':
        """
        The system data.
        """
        return pulumi.get(self, "system_data")

    @property
    @pulumi.getter(name="targetId")
    def target_id(self) -> Optional[str]:
        """
        The resource Id of target service.
        """
        return pulumi.get(self, "target_id")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        The type of the resource. E.g. "Microsoft.Compute/virtualMachines" or "Microsoft.Storage/storageAccounts"
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter(name="vNetSolution")
    def v_net_solution(self) -> Optional['outputs.VNetSolutionResponse']:
        """
        The VNet solution.
        """
        return pulumi.get(self, "v_net_solution")


class AwaitableGetLinkerResult(GetLinkerResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetLinkerResult(
            auth_info=self.auth_info,
            client_type=self.client_type,
            id=self.id,
            name=self.name,
            provisioning_state=self.provisioning_state,
            secret_store=self.secret_store,
            system_data=self.system_data,
            target_id=self.target_id,
            type=self.type,
            v_net_solution=self.v_net_solution)


def get_linker(linker_name: Optional[str] = None,
               resource_uri: Optional[str] = None,
               opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetLinkerResult:
    """
    Linker of source and target resource


    :param str linker_name: The name Linker resource.
    :param str resource_uri: The fully qualified Azure Resource manager identifier of the resource to be connected.
    """
    __args__ = dict()
    __args__['linkerName'] = linker_name
    __args__['resourceUri'] = resource_uri
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:servicelinker/v20211101preview:getLinker', __args__, opts=opts, typ=GetLinkerResult).value

    return AwaitableGetLinkerResult(
        auth_info=__ret__.auth_info,
        client_type=__ret__.client_type,
        id=__ret__.id,
        name=__ret__.name,
        provisioning_state=__ret__.provisioning_state,
        secret_store=__ret__.secret_store,
        system_data=__ret__.system_data,
        target_id=__ret__.target_id,
        type=__ret__.type,
        v_net_solution=__ret__.v_net_solution)


@_utilities.lift_output_func(get_linker)
def get_linker_output(linker_name: Optional[pulumi.Input[str]] = None,
                      resource_uri: Optional[pulumi.Input[str]] = None,
                      opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetLinkerResult]:
    """
    Linker of source and target resource


    :param str linker_name: The name Linker resource.
    :param str resource_uri: The fully qualified Azure Resource manager identifier of the resource to be connected.
    """
    ...
