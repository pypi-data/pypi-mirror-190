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
from ._enums import *
from ._inputs import *

__all__ = ['PrivateEndpointConnectionArgs', 'PrivateEndpointConnection']

@pulumi.input_type
class PrivateEndpointConnectionArgs:
    def __init__(__self__, *,
                 resource_group_name: pulumi.Input[str],
                 search_service_name: pulumi.Input[str],
                 private_endpoint_connection_name: Optional[pulumi.Input[str]] = None,
                 properties: Optional[pulumi.Input['PrivateEndpointConnectionPropertiesArgs']] = None):
        """
        The set of arguments for constructing a PrivateEndpointConnection resource.
        :param pulumi.Input[str] resource_group_name: The name of the resource group within the current subscription. You can obtain this value from the Azure Resource Manager API or the portal.
        :param pulumi.Input[str] search_service_name: The name of the Azure Cognitive Search service associated with the specified resource group.
        :param pulumi.Input[str] private_endpoint_connection_name: The name of the private endpoint connection to the Azure Cognitive Search service with the specified resource group.
        :param pulumi.Input['PrivateEndpointConnectionPropertiesArgs'] properties: Describes the properties of an existing Private Endpoint connection to the Azure Cognitive Search service.
        """
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        pulumi.set(__self__, "search_service_name", search_service_name)
        if private_endpoint_connection_name is not None:
            pulumi.set(__self__, "private_endpoint_connection_name", private_endpoint_connection_name)
        if properties is not None:
            pulumi.set(__self__, "properties", properties)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Input[str]:
        """
        The name of the resource group within the current subscription. You can obtain this value from the Azure Resource Manager API or the portal.
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "resource_group_name", value)

    @property
    @pulumi.getter(name="searchServiceName")
    def search_service_name(self) -> pulumi.Input[str]:
        """
        The name of the Azure Cognitive Search service associated with the specified resource group.
        """
        return pulumi.get(self, "search_service_name")

    @search_service_name.setter
    def search_service_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "search_service_name", value)

    @property
    @pulumi.getter(name="privateEndpointConnectionName")
    def private_endpoint_connection_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the private endpoint connection to the Azure Cognitive Search service with the specified resource group.
        """
        return pulumi.get(self, "private_endpoint_connection_name")

    @private_endpoint_connection_name.setter
    def private_endpoint_connection_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "private_endpoint_connection_name", value)

    @property
    @pulumi.getter
    def properties(self) -> Optional[pulumi.Input['PrivateEndpointConnectionPropertiesArgs']]:
        """
        Describes the properties of an existing Private Endpoint connection to the Azure Cognitive Search service.
        """
        return pulumi.get(self, "properties")

    @properties.setter
    def properties(self, value: Optional[pulumi.Input['PrivateEndpointConnectionPropertiesArgs']]):
        pulumi.set(self, "properties", value)


class PrivateEndpointConnection(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 private_endpoint_connection_name: Optional[pulumi.Input[str]] = None,
                 properties: Optional[pulumi.Input[pulumi.InputType['PrivateEndpointConnectionPropertiesArgs']]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 search_service_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Describes an existing Private Endpoint connection to the Azure Cognitive Search service.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] private_endpoint_connection_name: The name of the private endpoint connection to the Azure Cognitive Search service with the specified resource group.
        :param pulumi.Input[pulumi.InputType['PrivateEndpointConnectionPropertiesArgs']] properties: Describes the properties of an existing Private Endpoint connection to the Azure Cognitive Search service.
        :param pulumi.Input[str] resource_group_name: The name of the resource group within the current subscription. You can obtain this value from the Azure Resource Manager API or the portal.
        :param pulumi.Input[str] search_service_name: The name of the Azure Cognitive Search service associated with the specified resource group.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: PrivateEndpointConnectionArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Describes an existing Private Endpoint connection to the Azure Cognitive Search service.

        :param str resource_name: The name of the resource.
        :param PrivateEndpointConnectionArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(PrivateEndpointConnectionArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 private_endpoint_connection_name: Optional[pulumi.Input[str]] = None,
                 properties: Optional[pulumi.Input[pulumi.InputType['PrivateEndpointConnectionPropertiesArgs']]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 search_service_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = PrivateEndpointConnectionArgs.__new__(PrivateEndpointConnectionArgs)

            __props__.__dict__["private_endpoint_connection_name"] = private_endpoint_connection_name
            __props__.__dict__["properties"] = properties
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            if search_service_name is None and not opts.urn:
                raise TypeError("Missing required property 'search_service_name'")
            __props__.__dict__["search_service_name"] = search_service_name
            __props__.__dict__["name"] = None
            __props__.__dict__["type"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-native:search:PrivateEndpointConnection"), pulumi.Alias(type_="azure-native:search/v20191001preview:PrivateEndpointConnection"), pulumi.Alias(type_="azure-native:search/v20200313:PrivateEndpointConnection"), pulumi.Alias(type_="azure-native:search/v20200801:PrivateEndpointConnection"), pulumi.Alias(type_="azure-native:search/v20200801preview:PrivateEndpointConnection"), pulumi.Alias(type_="azure-native:search/v20220901:PrivateEndpointConnection")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(PrivateEndpointConnection, __self__).__init__(
            'azure-native:search/v20210401preview:PrivateEndpointConnection',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'PrivateEndpointConnection':
        """
        Get an existing PrivateEndpointConnection resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = PrivateEndpointConnectionArgs.__new__(PrivateEndpointConnectionArgs)

        __props__.__dict__["name"] = None
        __props__.__dict__["properties"] = None
        __props__.__dict__["type"] = None
        return PrivateEndpointConnection(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the resource
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def properties(self) -> pulumi.Output['outputs.PrivateEndpointConnectionPropertiesResponse']:
        """
        Describes the properties of an existing Private Endpoint connection to the Azure Cognitive Search service.
        """
        return pulumi.get(self, "properties")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        The type of the resource. E.g. "Microsoft.Compute/virtualMachines" or "Microsoft.Storage/storageAccounts"
        """
        return pulumi.get(self, "type")

