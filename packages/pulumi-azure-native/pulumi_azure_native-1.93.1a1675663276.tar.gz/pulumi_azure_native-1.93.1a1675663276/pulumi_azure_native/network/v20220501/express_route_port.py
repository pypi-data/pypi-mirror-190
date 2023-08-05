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

__all__ = ['ExpressRoutePortArgs', 'ExpressRoutePort']

@pulumi.input_type
class ExpressRoutePortArgs:
    def __init__(__self__, *,
                 resource_group_name: pulumi.Input[str],
                 bandwidth_in_gbps: Optional[pulumi.Input[int]] = None,
                 billing_type: Optional[pulumi.Input[Union[str, 'ExpressRoutePortsBillingType']]] = None,
                 encapsulation: Optional[pulumi.Input[Union[str, 'ExpressRoutePortsEncapsulation']]] = None,
                 express_route_port_name: Optional[pulumi.Input[str]] = None,
                 id: Optional[pulumi.Input[str]] = None,
                 identity: Optional[pulumi.Input['ManagedServiceIdentityArgs']] = None,
                 links: Optional[pulumi.Input[Sequence[pulumi.Input['ExpressRouteLinkArgs']]]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 peering_location: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None):
        """
        The set of arguments for constructing a ExpressRoutePort resource.
        :param pulumi.Input[str] resource_group_name: The name of the resource group.
        :param pulumi.Input[int] bandwidth_in_gbps: Bandwidth of procured ports in Gbps.
        :param pulumi.Input[Union[str, 'ExpressRoutePortsBillingType']] billing_type: The billing type of the ExpressRoutePort resource.
        :param pulumi.Input[Union[str, 'ExpressRoutePortsEncapsulation']] encapsulation: Encapsulation method on physical ports.
        :param pulumi.Input[str] express_route_port_name: The name of the ExpressRoutePort resource.
        :param pulumi.Input[str] id: Resource ID.
        :param pulumi.Input['ManagedServiceIdentityArgs'] identity: The identity of ExpressRoutePort, if configured.
        :param pulumi.Input[Sequence[pulumi.Input['ExpressRouteLinkArgs']]] links: The set of physical links of the ExpressRoutePort resource.
        :param pulumi.Input[str] location: Resource location.
        :param pulumi.Input[str] peering_location: The name of the peering location that the ExpressRoutePort is mapped to physically.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Resource tags.
        """
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        if bandwidth_in_gbps is not None:
            pulumi.set(__self__, "bandwidth_in_gbps", bandwidth_in_gbps)
        if billing_type is not None:
            pulumi.set(__self__, "billing_type", billing_type)
        if encapsulation is not None:
            pulumi.set(__self__, "encapsulation", encapsulation)
        if express_route_port_name is not None:
            pulumi.set(__self__, "express_route_port_name", express_route_port_name)
        if id is not None:
            pulumi.set(__self__, "id", id)
        if identity is not None:
            pulumi.set(__self__, "identity", identity)
        if links is not None:
            pulumi.set(__self__, "links", links)
        if location is not None:
            pulumi.set(__self__, "location", location)
        if peering_location is not None:
            pulumi.set(__self__, "peering_location", peering_location)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Input[str]:
        """
        The name of the resource group.
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "resource_group_name", value)

    @property
    @pulumi.getter(name="bandwidthInGbps")
    def bandwidth_in_gbps(self) -> Optional[pulumi.Input[int]]:
        """
        Bandwidth of procured ports in Gbps.
        """
        return pulumi.get(self, "bandwidth_in_gbps")

    @bandwidth_in_gbps.setter
    def bandwidth_in_gbps(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "bandwidth_in_gbps", value)

    @property
    @pulumi.getter(name="billingType")
    def billing_type(self) -> Optional[pulumi.Input[Union[str, 'ExpressRoutePortsBillingType']]]:
        """
        The billing type of the ExpressRoutePort resource.
        """
        return pulumi.get(self, "billing_type")

    @billing_type.setter
    def billing_type(self, value: Optional[pulumi.Input[Union[str, 'ExpressRoutePortsBillingType']]]):
        pulumi.set(self, "billing_type", value)

    @property
    @pulumi.getter
    def encapsulation(self) -> Optional[pulumi.Input[Union[str, 'ExpressRoutePortsEncapsulation']]]:
        """
        Encapsulation method on physical ports.
        """
        return pulumi.get(self, "encapsulation")

    @encapsulation.setter
    def encapsulation(self, value: Optional[pulumi.Input[Union[str, 'ExpressRoutePortsEncapsulation']]]):
        pulumi.set(self, "encapsulation", value)

    @property
    @pulumi.getter(name="expressRoutePortName")
    def express_route_port_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the ExpressRoutePort resource.
        """
        return pulumi.get(self, "express_route_port_name")

    @express_route_port_name.setter
    def express_route_port_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "express_route_port_name", value)

    @property
    @pulumi.getter
    def id(self) -> Optional[pulumi.Input[str]]:
        """
        Resource ID.
        """
        return pulumi.get(self, "id")

    @id.setter
    def id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "id", value)

    @property
    @pulumi.getter
    def identity(self) -> Optional[pulumi.Input['ManagedServiceIdentityArgs']]:
        """
        The identity of ExpressRoutePort, if configured.
        """
        return pulumi.get(self, "identity")

    @identity.setter
    def identity(self, value: Optional[pulumi.Input['ManagedServiceIdentityArgs']]):
        pulumi.set(self, "identity", value)

    @property
    @pulumi.getter
    def links(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['ExpressRouteLinkArgs']]]]:
        """
        The set of physical links of the ExpressRoutePort resource.
        """
        return pulumi.get(self, "links")

    @links.setter
    def links(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['ExpressRouteLinkArgs']]]]):
        pulumi.set(self, "links", value)

    @property
    @pulumi.getter
    def location(self) -> Optional[pulumi.Input[str]]:
        """
        Resource location.
        """
        return pulumi.get(self, "location")

    @location.setter
    def location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "location", value)

    @property
    @pulumi.getter(name="peeringLocation")
    def peering_location(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the peering location that the ExpressRoutePort is mapped to physically.
        """
        return pulumi.get(self, "peering_location")

    @peering_location.setter
    def peering_location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "peering_location", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Resource tags.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)


class ExpressRoutePort(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 bandwidth_in_gbps: Optional[pulumi.Input[int]] = None,
                 billing_type: Optional[pulumi.Input[Union[str, 'ExpressRoutePortsBillingType']]] = None,
                 encapsulation: Optional[pulumi.Input[Union[str, 'ExpressRoutePortsEncapsulation']]] = None,
                 express_route_port_name: Optional[pulumi.Input[str]] = None,
                 id: Optional[pulumi.Input[str]] = None,
                 identity: Optional[pulumi.Input[pulumi.InputType['ManagedServiceIdentityArgs']]] = None,
                 links: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ExpressRouteLinkArgs']]]]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 peering_location: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None):
        """
        ExpressRoutePort resource definition.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[int] bandwidth_in_gbps: Bandwidth of procured ports in Gbps.
        :param pulumi.Input[Union[str, 'ExpressRoutePortsBillingType']] billing_type: The billing type of the ExpressRoutePort resource.
        :param pulumi.Input[Union[str, 'ExpressRoutePortsEncapsulation']] encapsulation: Encapsulation method on physical ports.
        :param pulumi.Input[str] express_route_port_name: The name of the ExpressRoutePort resource.
        :param pulumi.Input[str] id: Resource ID.
        :param pulumi.Input[pulumi.InputType['ManagedServiceIdentityArgs']] identity: The identity of ExpressRoutePort, if configured.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ExpressRouteLinkArgs']]]] links: The set of physical links of the ExpressRoutePort resource.
        :param pulumi.Input[str] location: Resource location.
        :param pulumi.Input[str] peering_location: The name of the peering location that the ExpressRoutePort is mapped to physically.
        :param pulumi.Input[str] resource_group_name: The name of the resource group.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Resource tags.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: ExpressRoutePortArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        ExpressRoutePort resource definition.

        :param str resource_name: The name of the resource.
        :param ExpressRoutePortArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ExpressRoutePortArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 bandwidth_in_gbps: Optional[pulumi.Input[int]] = None,
                 billing_type: Optional[pulumi.Input[Union[str, 'ExpressRoutePortsBillingType']]] = None,
                 encapsulation: Optional[pulumi.Input[Union[str, 'ExpressRoutePortsEncapsulation']]] = None,
                 express_route_port_name: Optional[pulumi.Input[str]] = None,
                 id: Optional[pulumi.Input[str]] = None,
                 identity: Optional[pulumi.Input[pulumi.InputType['ManagedServiceIdentityArgs']]] = None,
                 links: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ExpressRouteLinkArgs']]]]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 peering_location: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = ExpressRoutePortArgs.__new__(ExpressRoutePortArgs)

            __props__.__dict__["bandwidth_in_gbps"] = bandwidth_in_gbps
            __props__.__dict__["billing_type"] = billing_type
            __props__.__dict__["encapsulation"] = encapsulation
            __props__.__dict__["express_route_port_name"] = express_route_port_name
            __props__.__dict__["id"] = id
            __props__.__dict__["identity"] = identity
            __props__.__dict__["links"] = links
            __props__.__dict__["location"] = location
            __props__.__dict__["peering_location"] = peering_location
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            __props__.__dict__["tags"] = tags
            __props__.__dict__["allocation_date"] = None
            __props__.__dict__["circuits"] = None
            __props__.__dict__["etag"] = None
            __props__.__dict__["ether_type"] = None
            __props__.__dict__["mtu"] = None
            __props__.__dict__["name"] = None
            __props__.__dict__["provisioned_bandwidth_in_gbps"] = None
            __props__.__dict__["provisioning_state"] = None
            __props__.__dict__["resource_guid"] = None
            __props__.__dict__["type"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-native:network:ExpressRoutePort"), pulumi.Alias(type_="azure-native:network/v20180801:ExpressRoutePort"), pulumi.Alias(type_="azure-native:network/v20181001:ExpressRoutePort"), pulumi.Alias(type_="azure-native:network/v20181101:ExpressRoutePort"), pulumi.Alias(type_="azure-native:network/v20181201:ExpressRoutePort"), pulumi.Alias(type_="azure-native:network/v20190201:ExpressRoutePort"), pulumi.Alias(type_="azure-native:network/v20190401:ExpressRoutePort"), pulumi.Alias(type_="azure-native:network/v20190601:ExpressRoutePort"), pulumi.Alias(type_="azure-native:network/v20190701:ExpressRoutePort"), pulumi.Alias(type_="azure-native:network/v20190801:ExpressRoutePort"), pulumi.Alias(type_="azure-native:network/v20190901:ExpressRoutePort"), pulumi.Alias(type_="azure-native:network/v20191101:ExpressRoutePort"), pulumi.Alias(type_="azure-native:network/v20191201:ExpressRoutePort"), pulumi.Alias(type_="azure-native:network/v20200301:ExpressRoutePort"), pulumi.Alias(type_="azure-native:network/v20200401:ExpressRoutePort"), pulumi.Alias(type_="azure-native:network/v20200501:ExpressRoutePort"), pulumi.Alias(type_="azure-native:network/v20200601:ExpressRoutePort"), pulumi.Alias(type_="azure-native:network/v20200701:ExpressRoutePort"), pulumi.Alias(type_="azure-native:network/v20200801:ExpressRoutePort"), pulumi.Alias(type_="azure-native:network/v20201101:ExpressRoutePort"), pulumi.Alias(type_="azure-native:network/v20210201:ExpressRoutePort"), pulumi.Alias(type_="azure-native:network/v20210301:ExpressRoutePort"), pulumi.Alias(type_="azure-native:network/v20210501:ExpressRoutePort"), pulumi.Alias(type_="azure-native:network/v20210801:ExpressRoutePort"), pulumi.Alias(type_="azure-native:network/v20220101:ExpressRoutePort"), pulumi.Alias(type_="azure-native:network/v20220701:ExpressRoutePort")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(ExpressRoutePort, __self__).__init__(
            'azure-native:network/v20220501:ExpressRoutePort',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'ExpressRoutePort':
        """
        Get an existing ExpressRoutePort resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = ExpressRoutePortArgs.__new__(ExpressRoutePortArgs)

        __props__.__dict__["allocation_date"] = None
        __props__.__dict__["bandwidth_in_gbps"] = None
        __props__.__dict__["billing_type"] = None
        __props__.__dict__["circuits"] = None
        __props__.__dict__["encapsulation"] = None
        __props__.__dict__["etag"] = None
        __props__.__dict__["ether_type"] = None
        __props__.__dict__["identity"] = None
        __props__.__dict__["links"] = None
        __props__.__dict__["location"] = None
        __props__.__dict__["mtu"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["peering_location"] = None
        __props__.__dict__["provisioned_bandwidth_in_gbps"] = None
        __props__.__dict__["provisioning_state"] = None
        __props__.__dict__["resource_guid"] = None
        __props__.__dict__["tags"] = None
        __props__.__dict__["type"] = None
        return ExpressRoutePort(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="allocationDate")
    def allocation_date(self) -> pulumi.Output[str]:
        """
        Date of the physical port allocation to be used in Letter of Authorization.
        """
        return pulumi.get(self, "allocation_date")

    @property
    @pulumi.getter(name="bandwidthInGbps")
    def bandwidth_in_gbps(self) -> pulumi.Output[Optional[int]]:
        """
        Bandwidth of procured ports in Gbps.
        """
        return pulumi.get(self, "bandwidth_in_gbps")

    @property
    @pulumi.getter(name="billingType")
    def billing_type(self) -> pulumi.Output[Optional[str]]:
        """
        The billing type of the ExpressRoutePort resource.
        """
        return pulumi.get(self, "billing_type")

    @property
    @pulumi.getter
    def circuits(self) -> pulumi.Output[Sequence['outputs.SubResourceResponse']]:
        """
        Reference the ExpressRoute circuit(s) that are provisioned on this ExpressRoutePort resource.
        """
        return pulumi.get(self, "circuits")

    @property
    @pulumi.getter
    def encapsulation(self) -> pulumi.Output[Optional[str]]:
        """
        Encapsulation method on physical ports.
        """
        return pulumi.get(self, "encapsulation")

    @property
    @pulumi.getter
    def etag(self) -> pulumi.Output[str]:
        """
        A unique read-only string that changes whenever the resource is updated.
        """
        return pulumi.get(self, "etag")

    @property
    @pulumi.getter(name="etherType")
    def ether_type(self) -> pulumi.Output[str]:
        """
        Ether type of the physical port.
        """
        return pulumi.get(self, "ether_type")

    @property
    @pulumi.getter
    def identity(self) -> pulumi.Output[Optional['outputs.ManagedServiceIdentityResponse']]:
        """
        The identity of ExpressRoutePort, if configured.
        """
        return pulumi.get(self, "identity")

    @property
    @pulumi.getter
    def links(self) -> pulumi.Output[Optional[Sequence['outputs.ExpressRouteLinkResponse']]]:
        """
        The set of physical links of the ExpressRoutePort resource.
        """
        return pulumi.get(self, "links")

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[Optional[str]]:
        """
        Resource location.
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def mtu(self) -> pulumi.Output[str]:
        """
        Maximum transmission unit of the physical port pair(s).
        """
        return pulumi.get(self, "mtu")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Resource name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="peeringLocation")
    def peering_location(self) -> pulumi.Output[Optional[str]]:
        """
        The name of the peering location that the ExpressRoutePort is mapped to physically.
        """
        return pulumi.get(self, "peering_location")

    @property
    @pulumi.getter(name="provisionedBandwidthInGbps")
    def provisioned_bandwidth_in_gbps(self) -> pulumi.Output[float]:
        """
        Aggregate Gbps of associated circuit bandwidths.
        """
        return pulumi.get(self, "provisioned_bandwidth_in_gbps")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> pulumi.Output[str]:
        """
        The provisioning state of the express route port resource.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter(name="resourceGuid")
    def resource_guid(self) -> pulumi.Output[str]:
        """
        The resource GUID property of the express route port resource.
        """
        return pulumi.get(self, "resource_guid")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        Resource tags.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        Resource type.
        """
        return pulumi.get(self, "type")

