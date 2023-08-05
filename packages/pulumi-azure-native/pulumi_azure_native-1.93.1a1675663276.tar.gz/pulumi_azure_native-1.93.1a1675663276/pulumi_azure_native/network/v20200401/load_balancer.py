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

__all__ = ['LoadBalancerArgs', 'LoadBalancer']

@pulumi.input_type
class LoadBalancerArgs:
    def __init__(__self__, *,
                 resource_group_name: pulumi.Input[str],
                 backend_address_pools: Optional[pulumi.Input[Sequence[pulumi.Input['BackendAddressPoolArgs']]]] = None,
                 frontend_ip_configurations: Optional[pulumi.Input[Sequence[pulumi.Input['FrontendIPConfigurationArgs']]]] = None,
                 id: Optional[pulumi.Input[str]] = None,
                 inbound_nat_pools: Optional[pulumi.Input[Sequence[pulumi.Input['InboundNatPoolArgs']]]] = None,
                 inbound_nat_rules: Optional[pulumi.Input[Sequence[pulumi.Input['InboundNatRuleArgs']]]] = None,
                 load_balancer_name: Optional[pulumi.Input[str]] = None,
                 load_balancing_rules: Optional[pulumi.Input[Sequence[pulumi.Input['LoadBalancingRuleArgs']]]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 outbound_rules: Optional[pulumi.Input[Sequence[pulumi.Input['OutboundRuleArgs']]]] = None,
                 probes: Optional[pulumi.Input[Sequence[pulumi.Input['ProbeArgs']]]] = None,
                 sku: Optional[pulumi.Input['LoadBalancerSkuArgs']] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None):
        """
        The set of arguments for constructing a LoadBalancer resource.
        :param pulumi.Input[str] resource_group_name: The name of the resource group.
        :param pulumi.Input[Sequence[pulumi.Input['BackendAddressPoolArgs']]] backend_address_pools: Collection of backend address pools used by a load balancer.
        :param pulumi.Input[Sequence[pulumi.Input['FrontendIPConfigurationArgs']]] frontend_ip_configurations: Object representing the frontend IPs to be used for the load balancer.
        :param pulumi.Input[str] id: Resource ID.
        :param pulumi.Input[Sequence[pulumi.Input['InboundNatPoolArgs']]] inbound_nat_pools: Defines an external port range for inbound NAT to a single backend port on NICs associated with a load balancer. Inbound NAT rules are created automatically for each NIC associated with the Load Balancer using an external port from this range. Defining an Inbound NAT pool on your Load Balancer is mutually exclusive with defining inbound Nat rules. Inbound NAT pools are referenced from virtual machine scale sets. NICs that are associated with individual virtual machines cannot reference an inbound NAT pool. They have to reference individual inbound NAT rules.
        :param pulumi.Input[Sequence[pulumi.Input['InboundNatRuleArgs']]] inbound_nat_rules: Collection of inbound NAT Rules used by a load balancer. Defining inbound NAT rules on your load balancer is mutually exclusive with defining an inbound NAT pool. Inbound NAT pools are referenced from virtual machine scale sets. NICs that are associated with individual virtual machines cannot reference an Inbound NAT pool. They have to reference individual inbound NAT rules.
        :param pulumi.Input[str] load_balancer_name: The name of the load balancer.
        :param pulumi.Input[Sequence[pulumi.Input['LoadBalancingRuleArgs']]] load_balancing_rules: Object collection representing the load balancing rules Gets the provisioning.
        :param pulumi.Input[str] location: Resource location.
        :param pulumi.Input[Sequence[pulumi.Input['OutboundRuleArgs']]] outbound_rules: The outbound rules.
        :param pulumi.Input[Sequence[pulumi.Input['ProbeArgs']]] probes: Collection of probe objects used in the load balancer.
        :param pulumi.Input['LoadBalancerSkuArgs'] sku: The load balancer SKU.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Resource tags.
        """
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        if backend_address_pools is not None:
            pulumi.set(__self__, "backend_address_pools", backend_address_pools)
        if frontend_ip_configurations is not None:
            pulumi.set(__self__, "frontend_ip_configurations", frontend_ip_configurations)
        if id is not None:
            pulumi.set(__self__, "id", id)
        if inbound_nat_pools is not None:
            pulumi.set(__self__, "inbound_nat_pools", inbound_nat_pools)
        if inbound_nat_rules is not None:
            pulumi.set(__self__, "inbound_nat_rules", inbound_nat_rules)
        if load_balancer_name is not None:
            pulumi.set(__self__, "load_balancer_name", load_balancer_name)
        if load_balancing_rules is not None:
            pulumi.set(__self__, "load_balancing_rules", load_balancing_rules)
        if location is not None:
            pulumi.set(__self__, "location", location)
        if outbound_rules is not None:
            pulumi.set(__self__, "outbound_rules", outbound_rules)
        if probes is not None:
            pulumi.set(__self__, "probes", probes)
        if sku is not None:
            pulumi.set(__self__, "sku", sku)
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
    @pulumi.getter(name="backendAddressPools")
    def backend_address_pools(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['BackendAddressPoolArgs']]]]:
        """
        Collection of backend address pools used by a load balancer.
        """
        return pulumi.get(self, "backend_address_pools")

    @backend_address_pools.setter
    def backend_address_pools(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['BackendAddressPoolArgs']]]]):
        pulumi.set(self, "backend_address_pools", value)

    @property
    @pulumi.getter(name="frontendIPConfigurations")
    def frontend_ip_configurations(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['FrontendIPConfigurationArgs']]]]:
        """
        Object representing the frontend IPs to be used for the load balancer.
        """
        return pulumi.get(self, "frontend_ip_configurations")

    @frontend_ip_configurations.setter
    def frontend_ip_configurations(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['FrontendIPConfigurationArgs']]]]):
        pulumi.set(self, "frontend_ip_configurations", value)

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
    @pulumi.getter(name="inboundNatPools")
    def inbound_nat_pools(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['InboundNatPoolArgs']]]]:
        """
        Defines an external port range for inbound NAT to a single backend port on NICs associated with a load balancer. Inbound NAT rules are created automatically for each NIC associated with the Load Balancer using an external port from this range. Defining an Inbound NAT pool on your Load Balancer is mutually exclusive with defining inbound Nat rules. Inbound NAT pools are referenced from virtual machine scale sets. NICs that are associated with individual virtual machines cannot reference an inbound NAT pool. They have to reference individual inbound NAT rules.
        """
        return pulumi.get(self, "inbound_nat_pools")

    @inbound_nat_pools.setter
    def inbound_nat_pools(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['InboundNatPoolArgs']]]]):
        pulumi.set(self, "inbound_nat_pools", value)

    @property
    @pulumi.getter(name="inboundNatRules")
    def inbound_nat_rules(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['InboundNatRuleArgs']]]]:
        """
        Collection of inbound NAT Rules used by a load balancer. Defining inbound NAT rules on your load balancer is mutually exclusive with defining an inbound NAT pool. Inbound NAT pools are referenced from virtual machine scale sets. NICs that are associated with individual virtual machines cannot reference an Inbound NAT pool. They have to reference individual inbound NAT rules.
        """
        return pulumi.get(self, "inbound_nat_rules")

    @inbound_nat_rules.setter
    def inbound_nat_rules(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['InboundNatRuleArgs']]]]):
        pulumi.set(self, "inbound_nat_rules", value)

    @property
    @pulumi.getter(name="loadBalancerName")
    def load_balancer_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the load balancer.
        """
        return pulumi.get(self, "load_balancer_name")

    @load_balancer_name.setter
    def load_balancer_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "load_balancer_name", value)

    @property
    @pulumi.getter(name="loadBalancingRules")
    def load_balancing_rules(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['LoadBalancingRuleArgs']]]]:
        """
        Object collection representing the load balancing rules Gets the provisioning.
        """
        return pulumi.get(self, "load_balancing_rules")

    @load_balancing_rules.setter
    def load_balancing_rules(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['LoadBalancingRuleArgs']]]]):
        pulumi.set(self, "load_balancing_rules", value)

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
    @pulumi.getter(name="outboundRules")
    def outbound_rules(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['OutboundRuleArgs']]]]:
        """
        The outbound rules.
        """
        return pulumi.get(self, "outbound_rules")

    @outbound_rules.setter
    def outbound_rules(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['OutboundRuleArgs']]]]):
        pulumi.set(self, "outbound_rules", value)

    @property
    @pulumi.getter
    def probes(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['ProbeArgs']]]]:
        """
        Collection of probe objects used in the load balancer.
        """
        return pulumi.get(self, "probes")

    @probes.setter
    def probes(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['ProbeArgs']]]]):
        pulumi.set(self, "probes", value)

    @property
    @pulumi.getter
    def sku(self) -> Optional[pulumi.Input['LoadBalancerSkuArgs']]:
        """
        The load balancer SKU.
        """
        return pulumi.get(self, "sku")

    @sku.setter
    def sku(self, value: Optional[pulumi.Input['LoadBalancerSkuArgs']]):
        pulumi.set(self, "sku", value)

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


class LoadBalancer(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 backend_address_pools: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['BackendAddressPoolArgs']]]]] = None,
                 frontend_ip_configurations: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['FrontendIPConfigurationArgs']]]]] = None,
                 id: Optional[pulumi.Input[str]] = None,
                 inbound_nat_pools: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['InboundNatPoolArgs']]]]] = None,
                 inbound_nat_rules: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['InboundNatRuleArgs']]]]] = None,
                 load_balancer_name: Optional[pulumi.Input[str]] = None,
                 load_balancing_rules: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['LoadBalancingRuleArgs']]]]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 outbound_rules: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['OutboundRuleArgs']]]]] = None,
                 probes: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ProbeArgs']]]]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 sku: Optional[pulumi.Input[pulumi.InputType['LoadBalancerSkuArgs']]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None):
        """
        LoadBalancer resource.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['BackendAddressPoolArgs']]]] backend_address_pools: Collection of backend address pools used by a load balancer.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['FrontendIPConfigurationArgs']]]] frontend_ip_configurations: Object representing the frontend IPs to be used for the load balancer.
        :param pulumi.Input[str] id: Resource ID.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['InboundNatPoolArgs']]]] inbound_nat_pools: Defines an external port range for inbound NAT to a single backend port on NICs associated with a load balancer. Inbound NAT rules are created automatically for each NIC associated with the Load Balancer using an external port from this range. Defining an Inbound NAT pool on your Load Balancer is mutually exclusive with defining inbound Nat rules. Inbound NAT pools are referenced from virtual machine scale sets. NICs that are associated with individual virtual machines cannot reference an inbound NAT pool. They have to reference individual inbound NAT rules.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['InboundNatRuleArgs']]]] inbound_nat_rules: Collection of inbound NAT Rules used by a load balancer. Defining inbound NAT rules on your load balancer is mutually exclusive with defining an inbound NAT pool. Inbound NAT pools are referenced from virtual machine scale sets. NICs that are associated with individual virtual machines cannot reference an Inbound NAT pool. They have to reference individual inbound NAT rules.
        :param pulumi.Input[str] load_balancer_name: The name of the load balancer.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['LoadBalancingRuleArgs']]]] load_balancing_rules: Object collection representing the load balancing rules Gets the provisioning.
        :param pulumi.Input[str] location: Resource location.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['OutboundRuleArgs']]]] outbound_rules: The outbound rules.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ProbeArgs']]]] probes: Collection of probe objects used in the load balancer.
        :param pulumi.Input[str] resource_group_name: The name of the resource group.
        :param pulumi.Input[pulumi.InputType['LoadBalancerSkuArgs']] sku: The load balancer SKU.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Resource tags.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: LoadBalancerArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        LoadBalancer resource.

        :param str resource_name: The name of the resource.
        :param LoadBalancerArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(LoadBalancerArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 backend_address_pools: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['BackendAddressPoolArgs']]]]] = None,
                 frontend_ip_configurations: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['FrontendIPConfigurationArgs']]]]] = None,
                 id: Optional[pulumi.Input[str]] = None,
                 inbound_nat_pools: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['InboundNatPoolArgs']]]]] = None,
                 inbound_nat_rules: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['InboundNatRuleArgs']]]]] = None,
                 load_balancer_name: Optional[pulumi.Input[str]] = None,
                 load_balancing_rules: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['LoadBalancingRuleArgs']]]]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 outbound_rules: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['OutboundRuleArgs']]]]] = None,
                 probes: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ProbeArgs']]]]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 sku: Optional[pulumi.Input[pulumi.InputType['LoadBalancerSkuArgs']]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = LoadBalancerArgs.__new__(LoadBalancerArgs)

            __props__.__dict__["backend_address_pools"] = backend_address_pools
            __props__.__dict__["frontend_ip_configurations"] = frontend_ip_configurations
            __props__.__dict__["id"] = id
            __props__.__dict__["inbound_nat_pools"] = inbound_nat_pools
            __props__.__dict__["inbound_nat_rules"] = inbound_nat_rules
            __props__.__dict__["load_balancer_name"] = load_balancer_name
            __props__.__dict__["load_balancing_rules"] = load_balancing_rules
            __props__.__dict__["location"] = location
            __props__.__dict__["outbound_rules"] = outbound_rules
            __props__.__dict__["probes"] = probes
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            __props__.__dict__["sku"] = sku
            __props__.__dict__["tags"] = tags
            __props__.__dict__["etag"] = None
            __props__.__dict__["name"] = None
            __props__.__dict__["provisioning_state"] = None
            __props__.__dict__["resource_guid"] = None
            __props__.__dict__["type"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-native:network:LoadBalancer"), pulumi.Alias(type_="azure-native:network/v20150501preview:LoadBalancer"), pulumi.Alias(type_="azure-native:network/v20150615:LoadBalancer"), pulumi.Alias(type_="azure-native:network/v20160330:LoadBalancer"), pulumi.Alias(type_="azure-native:network/v20160601:LoadBalancer"), pulumi.Alias(type_="azure-native:network/v20160901:LoadBalancer"), pulumi.Alias(type_="azure-native:network/v20161201:LoadBalancer"), pulumi.Alias(type_="azure-native:network/v20170301:LoadBalancer"), pulumi.Alias(type_="azure-native:network/v20170601:LoadBalancer"), pulumi.Alias(type_="azure-native:network/v20170801:LoadBalancer"), pulumi.Alias(type_="azure-native:network/v20170901:LoadBalancer"), pulumi.Alias(type_="azure-native:network/v20171001:LoadBalancer"), pulumi.Alias(type_="azure-native:network/v20171101:LoadBalancer"), pulumi.Alias(type_="azure-native:network/v20180101:LoadBalancer"), pulumi.Alias(type_="azure-native:network/v20180201:LoadBalancer"), pulumi.Alias(type_="azure-native:network/v20180401:LoadBalancer"), pulumi.Alias(type_="azure-native:network/v20180601:LoadBalancer"), pulumi.Alias(type_="azure-native:network/v20180701:LoadBalancer"), pulumi.Alias(type_="azure-native:network/v20180801:LoadBalancer"), pulumi.Alias(type_="azure-native:network/v20181001:LoadBalancer"), pulumi.Alias(type_="azure-native:network/v20181101:LoadBalancer"), pulumi.Alias(type_="azure-native:network/v20181201:LoadBalancer"), pulumi.Alias(type_="azure-native:network/v20190201:LoadBalancer"), pulumi.Alias(type_="azure-native:network/v20190401:LoadBalancer"), pulumi.Alias(type_="azure-native:network/v20190601:LoadBalancer"), pulumi.Alias(type_="azure-native:network/v20190701:LoadBalancer"), pulumi.Alias(type_="azure-native:network/v20190801:LoadBalancer"), pulumi.Alias(type_="azure-native:network/v20190901:LoadBalancer"), pulumi.Alias(type_="azure-native:network/v20191101:LoadBalancer"), pulumi.Alias(type_="azure-native:network/v20191201:LoadBalancer"), pulumi.Alias(type_="azure-native:network/v20200301:LoadBalancer"), pulumi.Alias(type_="azure-native:network/v20200501:LoadBalancer"), pulumi.Alias(type_="azure-native:network/v20200601:LoadBalancer"), pulumi.Alias(type_="azure-native:network/v20200701:LoadBalancer"), pulumi.Alias(type_="azure-native:network/v20200801:LoadBalancer"), pulumi.Alias(type_="azure-native:network/v20201101:LoadBalancer"), pulumi.Alias(type_="azure-native:network/v20210201:LoadBalancer"), pulumi.Alias(type_="azure-native:network/v20210301:LoadBalancer"), pulumi.Alias(type_="azure-native:network/v20210501:LoadBalancer"), pulumi.Alias(type_="azure-native:network/v20210801:LoadBalancer"), pulumi.Alias(type_="azure-native:network/v20220101:LoadBalancer"), pulumi.Alias(type_="azure-native:network/v20220501:LoadBalancer"), pulumi.Alias(type_="azure-native:network/v20220701:LoadBalancer")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(LoadBalancer, __self__).__init__(
            'azure-native:network/v20200401:LoadBalancer',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'LoadBalancer':
        """
        Get an existing LoadBalancer resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = LoadBalancerArgs.__new__(LoadBalancerArgs)

        __props__.__dict__["backend_address_pools"] = None
        __props__.__dict__["etag"] = None
        __props__.__dict__["frontend_ip_configurations"] = None
        __props__.__dict__["inbound_nat_pools"] = None
        __props__.__dict__["inbound_nat_rules"] = None
        __props__.__dict__["load_balancing_rules"] = None
        __props__.__dict__["location"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["outbound_rules"] = None
        __props__.__dict__["probes"] = None
        __props__.__dict__["provisioning_state"] = None
        __props__.__dict__["resource_guid"] = None
        __props__.__dict__["sku"] = None
        __props__.__dict__["tags"] = None
        __props__.__dict__["type"] = None
        return LoadBalancer(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="backendAddressPools")
    def backend_address_pools(self) -> pulumi.Output[Optional[Sequence['outputs.BackendAddressPoolResponse']]]:
        """
        Collection of backend address pools used by a load balancer.
        """
        return pulumi.get(self, "backend_address_pools")

    @property
    @pulumi.getter
    def etag(self) -> pulumi.Output[str]:
        """
        A unique read-only string that changes whenever the resource is updated.
        """
        return pulumi.get(self, "etag")

    @property
    @pulumi.getter(name="frontendIPConfigurations")
    def frontend_ip_configurations(self) -> pulumi.Output[Optional[Sequence['outputs.FrontendIPConfigurationResponse']]]:
        """
        Object representing the frontend IPs to be used for the load balancer.
        """
        return pulumi.get(self, "frontend_ip_configurations")

    @property
    @pulumi.getter(name="inboundNatPools")
    def inbound_nat_pools(self) -> pulumi.Output[Optional[Sequence['outputs.InboundNatPoolResponse']]]:
        """
        Defines an external port range for inbound NAT to a single backend port on NICs associated with a load balancer. Inbound NAT rules are created automatically for each NIC associated with the Load Balancer using an external port from this range. Defining an Inbound NAT pool on your Load Balancer is mutually exclusive with defining inbound Nat rules. Inbound NAT pools are referenced from virtual machine scale sets. NICs that are associated with individual virtual machines cannot reference an inbound NAT pool. They have to reference individual inbound NAT rules.
        """
        return pulumi.get(self, "inbound_nat_pools")

    @property
    @pulumi.getter(name="inboundNatRules")
    def inbound_nat_rules(self) -> pulumi.Output[Optional[Sequence['outputs.InboundNatRuleResponse']]]:
        """
        Collection of inbound NAT Rules used by a load balancer. Defining inbound NAT rules on your load balancer is mutually exclusive with defining an inbound NAT pool. Inbound NAT pools are referenced from virtual machine scale sets. NICs that are associated with individual virtual machines cannot reference an Inbound NAT pool. They have to reference individual inbound NAT rules.
        """
        return pulumi.get(self, "inbound_nat_rules")

    @property
    @pulumi.getter(name="loadBalancingRules")
    def load_balancing_rules(self) -> pulumi.Output[Optional[Sequence['outputs.LoadBalancingRuleResponse']]]:
        """
        Object collection representing the load balancing rules Gets the provisioning.
        """
        return pulumi.get(self, "load_balancing_rules")

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[Optional[str]]:
        """
        Resource location.
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Resource name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="outboundRules")
    def outbound_rules(self) -> pulumi.Output[Optional[Sequence['outputs.OutboundRuleResponse']]]:
        """
        The outbound rules.
        """
        return pulumi.get(self, "outbound_rules")

    @property
    @pulumi.getter
    def probes(self) -> pulumi.Output[Optional[Sequence['outputs.ProbeResponse']]]:
        """
        Collection of probe objects used in the load balancer.
        """
        return pulumi.get(self, "probes")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> pulumi.Output[str]:
        """
        The provisioning state of the load balancer resource.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter(name="resourceGuid")
    def resource_guid(self) -> pulumi.Output[str]:
        """
        The resource GUID property of the load balancer resource.
        """
        return pulumi.get(self, "resource_guid")

    @property
    @pulumi.getter
    def sku(self) -> pulumi.Output[Optional['outputs.LoadBalancerSkuResponse']]:
        """
        The load balancer SKU.
        """
        return pulumi.get(self, "sku")

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

