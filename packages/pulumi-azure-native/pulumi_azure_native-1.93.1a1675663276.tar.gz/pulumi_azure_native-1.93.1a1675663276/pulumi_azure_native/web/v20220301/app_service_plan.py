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
from ._inputs import *

__all__ = ['AppServicePlanArgs', 'AppServicePlan']

@pulumi.input_type
class AppServicePlanArgs:
    def __init__(__self__, *,
                 resource_group_name: pulumi.Input[str],
                 elastic_scale_enabled: Optional[pulumi.Input[bool]] = None,
                 extended_location: Optional[pulumi.Input['ExtendedLocationArgs']] = None,
                 free_offer_expiration_time: Optional[pulumi.Input[str]] = None,
                 hosting_environment_profile: Optional[pulumi.Input['HostingEnvironmentProfileArgs']] = None,
                 hyper_v: Optional[pulumi.Input[bool]] = None,
                 is_spot: Optional[pulumi.Input[bool]] = None,
                 is_xenon: Optional[pulumi.Input[bool]] = None,
                 kind: Optional[pulumi.Input[str]] = None,
                 kube_environment_profile: Optional[pulumi.Input['KubeEnvironmentProfileArgs']] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 maximum_elastic_worker_count: Optional[pulumi.Input[int]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 per_site_scaling: Optional[pulumi.Input[bool]] = None,
                 reserved: Optional[pulumi.Input[bool]] = None,
                 sku: Optional[pulumi.Input['SkuDescriptionArgs']] = None,
                 spot_expiration_time: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 target_worker_count: Optional[pulumi.Input[int]] = None,
                 target_worker_size_id: Optional[pulumi.Input[int]] = None,
                 worker_tier_name: Optional[pulumi.Input[str]] = None,
                 zone_redundant: Optional[pulumi.Input[bool]] = None):
        """
        The set of arguments for constructing a AppServicePlan resource.
        :param pulumi.Input[str] resource_group_name: Name of the resource group to which the resource belongs.
        :param pulumi.Input[bool] elastic_scale_enabled: ServerFarm supports ElasticScale. Apps in this plan will scale as if the ServerFarm was ElasticPremium sku
        :param pulumi.Input['ExtendedLocationArgs'] extended_location: Extended Location.
        :param pulumi.Input[str] free_offer_expiration_time: The time when the server farm free offer expires.
        :param pulumi.Input['HostingEnvironmentProfileArgs'] hosting_environment_profile: Specification for the App Service Environment to use for the App Service plan.
        :param pulumi.Input[bool] hyper_v: If Hyper-V container app service plan <code>true</code>, <code>false</code> otherwise.
        :param pulumi.Input[bool] is_spot: If <code>true</code>, this App Service Plan owns spot instances.
        :param pulumi.Input[bool] is_xenon: Obsolete: If Hyper-V container app service plan <code>true</code>, <code>false</code> otherwise.
        :param pulumi.Input[str] kind: Kind of resource.
        :param pulumi.Input['KubeEnvironmentProfileArgs'] kube_environment_profile: Specification for the Kubernetes Environment to use for the App Service plan.
        :param pulumi.Input[str] location: Resource Location.
        :param pulumi.Input[int] maximum_elastic_worker_count: Maximum number of total workers allowed for this ElasticScaleEnabled App Service Plan
        :param pulumi.Input[str] name: Name of the App Service plan.
        :param pulumi.Input[bool] per_site_scaling: If <code>true</code>, apps assigned to this App Service plan can be scaled independently.
               If <code>false</code>, apps assigned to this App Service plan will scale to all instances of the plan.
        :param pulumi.Input[bool] reserved: If Linux app service plan <code>true</code>, <code>false</code> otherwise.
        :param pulumi.Input['SkuDescriptionArgs'] sku: Description of a SKU for a scalable resource.
        :param pulumi.Input[str] spot_expiration_time: The time when the server farm expires. Valid only if it is a spot server farm.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Resource tags.
        :param pulumi.Input[int] target_worker_count: Scaling worker count.
        :param pulumi.Input[int] target_worker_size_id: Scaling worker size ID.
        :param pulumi.Input[str] worker_tier_name: Target worker tier assigned to the App Service plan.
        :param pulumi.Input[bool] zone_redundant: If <code>true</code>, this App Service Plan will perform availability zone balancing.
               If <code>false</code>, this App Service Plan will not perform availability zone balancing.
        """
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        if elastic_scale_enabled is not None:
            pulumi.set(__self__, "elastic_scale_enabled", elastic_scale_enabled)
        if extended_location is not None:
            pulumi.set(__self__, "extended_location", extended_location)
        if free_offer_expiration_time is not None:
            pulumi.set(__self__, "free_offer_expiration_time", free_offer_expiration_time)
        if hosting_environment_profile is not None:
            pulumi.set(__self__, "hosting_environment_profile", hosting_environment_profile)
        if hyper_v is None:
            hyper_v = False
        if hyper_v is not None:
            pulumi.set(__self__, "hyper_v", hyper_v)
        if is_spot is not None:
            pulumi.set(__self__, "is_spot", is_spot)
        if is_xenon is None:
            is_xenon = False
        if is_xenon is not None:
            pulumi.set(__self__, "is_xenon", is_xenon)
        if kind is not None:
            pulumi.set(__self__, "kind", kind)
        if kube_environment_profile is not None:
            pulumi.set(__self__, "kube_environment_profile", kube_environment_profile)
        if location is not None:
            pulumi.set(__self__, "location", location)
        if maximum_elastic_worker_count is not None:
            pulumi.set(__self__, "maximum_elastic_worker_count", maximum_elastic_worker_count)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if per_site_scaling is None:
            per_site_scaling = False
        if per_site_scaling is not None:
            pulumi.set(__self__, "per_site_scaling", per_site_scaling)
        if reserved is None:
            reserved = False
        if reserved is not None:
            pulumi.set(__self__, "reserved", reserved)
        if sku is not None:
            pulumi.set(__self__, "sku", sku)
        if spot_expiration_time is not None:
            pulumi.set(__self__, "spot_expiration_time", spot_expiration_time)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)
        if target_worker_count is not None:
            pulumi.set(__self__, "target_worker_count", target_worker_count)
        if target_worker_size_id is not None:
            pulumi.set(__self__, "target_worker_size_id", target_worker_size_id)
        if worker_tier_name is not None:
            pulumi.set(__self__, "worker_tier_name", worker_tier_name)
        if zone_redundant is None:
            zone_redundant = False
        if zone_redundant is not None:
            pulumi.set(__self__, "zone_redundant", zone_redundant)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Input[str]:
        """
        Name of the resource group to which the resource belongs.
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "resource_group_name", value)

    @property
    @pulumi.getter(name="elasticScaleEnabled")
    def elastic_scale_enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        ServerFarm supports ElasticScale. Apps in this plan will scale as if the ServerFarm was ElasticPremium sku
        """
        return pulumi.get(self, "elastic_scale_enabled")

    @elastic_scale_enabled.setter
    def elastic_scale_enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "elastic_scale_enabled", value)

    @property
    @pulumi.getter(name="extendedLocation")
    def extended_location(self) -> Optional[pulumi.Input['ExtendedLocationArgs']]:
        """
        Extended Location.
        """
        return pulumi.get(self, "extended_location")

    @extended_location.setter
    def extended_location(self, value: Optional[pulumi.Input['ExtendedLocationArgs']]):
        pulumi.set(self, "extended_location", value)

    @property
    @pulumi.getter(name="freeOfferExpirationTime")
    def free_offer_expiration_time(self) -> Optional[pulumi.Input[str]]:
        """
        The time when the server farm free offer expires.
        """
        return pulumi.get(self, "free_offer_expiration_time")

    @free_offer_expiration_time.setter
    def free_offer_expiration_time(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "free_offer_expiration_time", value)

    @property
    @pulumi.getter(name="hostingEnvironmentProfile")
    def hosting_environment_profile(self) -> Optional[pulumi.Input['HostingEnvironmentProfileArgs']]:
        """
        Specification for the App Service Environment to use for the App Service plan.
        """
        return pulumi.get(self, "hosting_environment_profile")

    @hosting_environment_profile.setter
    def hosting_environment_profile(self, value: Optional[pulumi.Input['HostingEnvironmentProfileArgs']]):
        pulumi.set(self, "hosting_environment_profile", value)

    @property
    @pulumi.getter(name="hyperV")
    def hyper_v(self) -> Optional[pulumi.Input[bool]]:
        """
        If Hyper-V container app service plan <code>true</code>, <code>false</code> otherwise.
        """
        return pulumi.get(self, "hyper_v")

    @hyper_v.setter
    def hyper_v(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "hyper_v", value)

    @property
    @pulumi.getter(name="isSpot")
    def is_spot(self) -> Optional[pulumi.Input[bool]]:
        """
        If <code>true</code>, this App Service Plan owns spot instances.
        """
        return pulumi.get(self, "is_spot")

    @is_spot.setter
    def is_spot(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "is_spot", value)

    @property
    @pulumi.getter(name="isXenon")
    def is_xenon(self) -> Optional[pulumi.Input[bool]]:
        """
        Obsolete: If Hyper-V container app service plan <code>true</code>, <code>false</code> otherwise.
        """
        return pulumi.get(self, "is_xenon")

    @is_xenon.setter
    def is_xenon(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "is_xenon", value)

    @property
    @pulumi.getter
    def kind(self) -> Optional[pulumi.Input[str]]:
        """
        Kind of resource.
        """
        return pulumi.get(self, "kind")

    @kind.setter
    def kind(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "kind", value)

    @property
    @pulumi.getter(name="kubeEnvironmentProfile")
    def kube_environment_profile(self) -> Optional[pulumi.Input['KubeEnvironmentProfileArgs']]:
        """
        Specification for the Kubernetes Environment to use for the App Service plan.
        """
        return pulumi.get(self, "kube_environment_profile")

    @kube_environment_profile.setter
    def kube_environment_profile(self, value: Optional[pulumi.Input['KubeEnvironmentProfileArgs']]):
        pulumi.set(self, "kube_environment_profile", value)

    @property
    @pulumi.getter
    def location(self) -> Optional[pulumi.Input[str]]:
        """
        Resource Location.
        """
        return pulumi.get(self, "location")

    @location.setter
    def location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "location", value)

    @property
    @pulumi.getter(name="maximumElasticWorkerCount")
    def maximum_elastic_worker_count(self) -> Optional[pulumi.Input[int]]:
        """
        Maximum number of total workers allowed for this ElasticScaleEnabled App Service Plan
        """
        return pulumi.get(self, "maximum_elastic_worker_count")

    @maximum_elastic_worker_count.setter
    def maximum_elastic_worker_count(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "maximum_elastic_worker_count", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Name of the App Service plan.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="perSiteScaling")
    def per_site_scaling(self) -> Optional[pulumi.Input[bool]]:
        """
        If <code>true</code>, apps assigned to this App Service plan can be scaled independently.
        If <code>false</code>, apps assigned to this App Service plan will scale to all instances of the plan.
        """
        return pulumi.get(self, "per_site_scaling")

    @per_site_scaling.setter
    def per_site_scaling(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "per_site_scaling", value)

    @property
    @pulumi.getter
    def reserved(self) -> Optional[pulumi.Input[bool]]:
        """
        If Linux app service plan <code>true</code>, <code>false</code> otherwise.
        """
        return pulumi.get(self, "reserved")

    @reserved.setter
    def reserved(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "reserved", value)

    @property
    @pulumi.getter
    def sku(self) -> Optional[pulumi.Input['SkuDescriptionArgs']]:
        """
        Description of a SKU for a scalable resource.
        """
        return pulumi.get(self, "sku")

    @sku.setter
    def sku(self, value: Optional[pulumi.Input['SkuDescriptionArgs']]):
        pulumi.set(self, "sku", value)

    @property
    @pulumi.getter(name="spotExpirationTime")
    def spot_expiration_time(self) -> Optional[pulumi.Input[str]]:
        """
        The time when the server farm expires. Valid only if it is a spot server farm.
        """
        return pulumi.get(self, "spot_expiration_time")

    @spot_expiration_time.setter
    def spot_expiration_time(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "spot_expiration_time", value)

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

    @property
    @pulumi.getter(name="targetWorkerCount")
    def target_worker_count(self) -> Optional[pulumi.Input[int]]:
        """
        Scaling worker count.
        """
        return pulumi.get(self, "target_worker_count")

    @target_worker_count.setter
    def target_worker_count(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "target_worker_count", value)

    @property
    @pulumi.getter(name="targetWorkerSizeId")
    def target_worker_size_id(self) -> Optional[pulumi.Input[int]]:
        """
        Scaling worker size ID.
        """
        return pulumi.get(self, "target_worker_size_id")

    @target_worker_size_id.setter
    def target_worker_size_id(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "target_worker_size_id", value)

    @property
    @pulumi.getter(name="workerTierName")
    def worker_tier_name(self) -> Optional[pulumi.Input[str]]:
        """
        Target worker tier assigned to the App Service plan.
        """
        return pulumi.get(self, "worker_tier_name")

    @worker_tier_name.setter
    def worker_tier_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "worker_tier_name", value)

    @property
    @pulumi.getter(name="zoneRedundant")
    def zone_redundant(self) -> Optional[pulumi.Input[bool]]:
        """
        If <code>true</code>, this App Service Plan will perform availability zone balancing.
        If <code>false</code>, this App Service Plan will not perform availability zone balancing.
        """
        return pulumi.get(self, "zone_redundant")

    @zone_redundant.setter
    def zone_redundant(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "zone_redundant", value)


class AppServicePlan(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 elastic_scale_enabled: Optional[pulumi.Input[bool]] = None,
                 extended_location: Optional[pulumi.Input[pulumi.InputType['ExtendedLocationArgs']]] = None,
                 free_offer_expiration_time: Optional[pulumi.Input[str]] = None,
                 hosting_environment_profile: Optional[pulumi.Input[pulumi.InputType['HostingEnvironmentProfileArgs']]] = None,
                 hyper_v: Optional[pulumi.Input[bool]] = None,
                 is_spot: Optional[pulumi.Input[bool]] = None,
                 is_xenon: Optional[pulumi.Input[bool]] = None,
                 kind: Optional[pulumi.Input[str]] = None,
                 kube_environment_profile: Optional[pulumi.Input[pulumi.InputType['KubeEnvironmentProfileArgs']]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 maximum_elastic_worker_count: Optional[pulumi.Input[int]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 per_site_scaling: Optional[pulumi.Input[bool]] = None,
                 reserved: Optional[pulumi.Input[bool]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 sku: Optional[pulumi.Input[pulumi.InputType['SkuDescriptionArgs']]] = None,
                 spot_expiration_time: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 target_worker_count: Optional[pulumi.Input[int]] = None,
                 target_worker_size_id: Optional[pulumi.Input[int]] = None,
                 worker_tier_name: Optional[pulumi.Input[str]] = None,
                 zone_redundant: Optional[pulumi.Input[bool]] = None,
                 __props__=None):
        """
        App Service plan.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[bool] elastic_scale_enabled: ServerFarm supports ElasticScale. Apps in this plan will scale as if the ServerFarm was ElasticPremium sku
        :param pulumi.Input[pulumi.InputType['ExtendedLocationArgs']] extended_location: Extended Location.
        :param pulumi.Input[str] free_offer_expiration_time: The time when the server farm free offer expires.
        :param pulumi.Input[pulumi.InputType['HostingEnvironmentProfileArgs']] hosting_environment_profile: Specification for the App Service Environment to use for the App Service plan.
        :param pulumi.Input[bool] hyper_v: If Hyper-V container app service plan <code>true</code>, <code>false</code> otherwise.
        :param pulumi.Input[bool] is_spot: If <code>true</code>, this App Service Plan owns spot instances.
        :param pulumi.Input[bool] is_xenon: Obsolete: If Hyper-V container app service plan <code>true</code>, <code>false</code> otherwise.
        :param pulumi.Input[str] kind: Kind of resource.
        :param pulumi.Input[pulumi.InputType['KubeEnvironmentProfileArgs']] kube_environment_profile: Specification for the Kubernetes Environment to use for the App Service plan.
        :param pulumi.Input[str] location: Resource Location.
        :param pulumi.Input[int] maximum_elastic_worker_count: Maximum number of total workers allowed for this ElasticScaleEnabled App Service Plan
        :param pulumi.Input[str] name: Name of the App Service plan.
        :param pulumi.Input[bool] per_site_scaling: If <code>true</code>, apps assigned to this App Service plan can be scaled independently.
               If <code>false</code>, apps assigned to this App Service plan will scale to all instances of the plan.
        :param pulumi.Input[bool] reserved: If Linux app service plan <code>true</code>, <code>false</code> otherwise.
        :param pulumi.Input[str] resource_group_name: Name of the resource group to which the resource belongs.
        :param pulumi.Input[pulumi.InputType['SkuDescriptionArgs']] sku: Description of a SKU for a scalable resource.
        :param pulumi.Input[str] spot_expiration_time: The time when the server farm expires. Valid only if it is a spot server farm.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Resource tags.
        :param pulumi.Input[int] target_worker_count: Scaling worker count.
        :param pulumi.Input[int] target_worker_size_id: Scaling worker size ID.
        :param pulumi.Input[str] worker_tier_name: Target worker tier assigned to the App Service plan.
        :param pulumi.Input[bool] zone_redundant: If <code>true</code>, this App Service Plan will perform availability zone balancing.
               If <code>false</code>, this App Service Plan will not perform availability zone balancing.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: AppServicePlanArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        App Service plan.

        :param str resource_name: The name of the resource.
        :param AppServicePlanArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(AppServicePlanArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 elastic_scale_enabled: Optional[pulumi.Input[bool]] = None,
                 extended_location: Optional[pulumi.Input[pulumi.InputType['ExtendedLocationArgs']]] = None,
                 free_offer_expiration_time: Optional[pulumi.Input[str]] = None,
                 hosting_environment_profile: Optional[pulumi.Input[pulumi.InputType['HostingEnvironmentProfileArgs']]] = None,
                 hyper_v: Optional[pulumi.Input[bool]] = None,
                 is_spot: Optional[pulumi.Input[bool]] = None,
                 is_xenon: Optional[pulumi.Input[bool]] = None,
                 kind: Optional[pulumi.Input[str]] = None,
                 kube_environment_profile: Optional[pulumi.Input[pulumi.InputType['KubeEnvironmentProfileArgs']]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 maximum_elastic_worker_count: Optional[pulumi.Input[int]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 per_site_scaling: Optional[pulumi.Input[bool]] = None,
                 reserved: Optional[pulumi.Input[bool]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 sku: Optional[pulumi.Input[pulumi.InputType['SkuDescriptionArgs']]] = None,
                 spot_expiration_time: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 target_worker_count: Optional[pulumi.Input[int]] = None,
                 target_worker_size_id: Optional[pulumi.Input[int]] = None,
                 worker_tier_name: Optional[pulumi.Input[str]] = None,
                 zone_redundant: Optional[pulumi.Input[bool]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = AppServicePlanArgs.__new__(AppServicePlanArgs)

            __props__.__dict__["elastic_scale_enabled"] = elastic_scale_enabled
            __props__.__dict__["extended_location"] = extended_location
            __props__.__dict__["free_offer_expiration_time"] = free_offer_expiration_time
            __props__.__dict__["hosting_environment_profile"] = hosting_environment_profile
            if hyper_v is None:
                hyper_v = False
            __props__.__dict__["hyper_v"] = hyper_v
            __props__.__dict__["is_spot"] = is_spot
            if is_xenon is None:
                is_xenon = False
            __props__.__dict__["is_xenon"] = is_xenon
            __props__.__dict__["kind"] = kind
            __props__.__dict__["kube_environment_profile"] = kube_environment_profile
            __props__.__dict__["location"] = location
            __props__.__dict__["maximum_elastic_worker_count"] = maximum_elastic_worker_count
            __props__.__dict__["name"] = name
            if per_site_scaling is None:
                per_site_scaling = False
            __props__.__dict__["per_site_scaling"] = per_site_scaling
            if reserved is None:
                reserved = False
            __props__.__dict__["reserved"] = reserved
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            __props__.__dict__["sku"] = sku
            __props__.__dict__["spot_expiration_time"] = spot_expiration_time
            __props__.__dict__["tags"] = tags
            __props__.__dict__["target_worker_count"] = target_worker_count
            __props__.__dict__["target_worker_size_id"] = target_worker_size_id
            __props__.__dict__["worker_tier_name"] = worker_tier_name
            if zone_redundant is None:
                zone_redundant = False
            __props__.__dict__["zone_redundant"] = zone_redundant
            __props__.__dict__["geo_region"] = None
            __props__.__dict__["maximum_number_of_workers"] = None
            __props__.__dict__["number_of_sites"] = None
            __props__.__dict__["number_of_workers"] = None
            __props__.__dict__["provisioning_state"] = None
            __props__.__dict__["resource_group"] = None
            __props__.__dict__["status"] = None
            __props__.__dict__["subscription"] = None
            __props__.__dict__["type"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-native:web:AppServicePlan"), pulumi.Alias(type_="azure-native:web/v20150801:AppServicePlan"), pulumi.Alias(type_="azure-native:web/v20160901:AppServicePlan"), pulumi.Alias(type_="azure-native:web/v20180201:AppServicePlan"), pulumi.Alias(type_="azure-native:web/v20190801:AppServicePlan"), pulumi.Alias(type_="azure-native:web/v20200601:AppServicePlan"), pulumi.Alias(type_="azure-native:web/v20200901:AppServicePlan"), pulumi.Alias(type_="azure-native:web/v20201001:AppServicePlan"), pulumi.Alias(type_="azure-native:web/v20201201:AppServicePlan"), pulumi.Alias(type_="azure-native:web/v20210101:AppServicePlan"), pulumi.Alias(type_="azure-native:web/v20210115:AppServicePlan"), pulumi.Alias(type_="azure-native:web/v20210201:AppServicePlan"), pulumi.Alias(type_="azure-native:web/v20210301:AppServicePlan")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(AppServicePlan, __self__).__init__(
            'azure-native:web/v20220301:AppServicePlan',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'AppServicePlan':
        """
        Get an existing AppServicePlan resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = AppServicePlanArgs.__new__(AppServicePlanArgs)

        __props__.__dict__["elastic_scale_enabled"] = None
        __props__.__dict__["extended_location"] = None
        __props__.__dict__["free_offer_expiration_time"] = None
        __props__.__dict__["geo_region"] = None
        __props__.__dict__["hosting_environment_profile"] = None
        __props__.__dict__["hyper_v"] = None
        __props__.__dict__["is_spot"] = None
        __props__.__dict__["is_xenon"] = None
        __props__.__dict__["kind"] = None
        __props__.__dict__["kube_environment_profile"] = None
        __props__.__dict__["location"] = None
        __props__.__dict__["maximum_elastic_worker_count"] = None
        __props__.__dict__["maximum_number_of_workers"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["number_of_sites"] = None
        __props__.__dict__["number_of_workers"] = None
        __props__.__dict__["per_site_scaling"] = None
        __props__.__dict__["provisioning_state"] = None
        __props__.__dict__["reserved"] = None
        __props__.__dict__["resource_group"] = None
        __props__.__dict__["sku"] = None
        __props__.__dict__["spot_expiration_time"] = None
        __props__.__dict__["status"] = None
        __props__.__dict__["subscription"] = None
        __props__.__dict__["tags"] = None
        __props__.__dict__["target_worker_count"] = None
        __props__.__dict__["target_worker_size_id"] = None
        __props__.__dict__["type"] = None
        __props__.__dict__["worker_tier_name"] = None
        __props__.__dict__["zone_redundant"] = None
        return AppServicePlan(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="elasticScaleEnabled")
    def elastic_scale_enabled(self) -> pulumi.Output[Optional[bool]]:
        """
        ServerFarm supports ElasticScale. Apps in this plan will scale as if the ServerFarm was ElasticPremium sku
        """
        return pulumi.get(self, "elastic_scale_enabled")

    @property
    @pulumi.getter(name="extendedLocation")
    def extended_location(self) -> pulumi.Output[Optional['outputs.ExtendedLocationResponse']]:
        """
        Extended Location.
        """
        return pulumi.get(self, "extended_location")

    @property
    @pulumi.getter(name="freeOfferExpirationTime")
    def free_offer_expiration_time(self) -> pulumi.Output[Optional[str]]:
        """
        The time when the server farm free offer expires.
        """
        return pulumi.get(self, "free_offer_expiration_time")

    @property
    @pulumi.getter(name="geoRegion")
    def geo_region(self) -> pulumi.Output[str]:
        """
        Geographical location for the App Service plan.
        """
        return pulumi.get(self, "geo_region")

    @property
    @pulumi.getter(name="hostingEnvironmentProfile")
    def hosting_environment_profile(self) -> pulumi.Output[Optional['outputs.HostingEnvironmentProfileResponse']]:
        """
        Specification for the App Service Environment to use for the App Service plan.
        """
        return pulumi.get(self, "hosting_environment_profile")

    @property
    @pulumi.getter(name="hyperV")
    def hyper_v(self) -> pulumi.Output[Optional[bool]]:
        """
        If Hyper-V container app service plan <code>true</code>, <code>false</code> otherwise.
        """
        return pulumi.get(self, "hyper_v")

    @property
    @pulumi.getter(name="isSpot")
    def is_spot(self) -> pulumi.Output[Optional[bool]]:
        """
        If <code>true</code>, this App Service Plan owns spot instances.
        """
        return pulumi.get(self, "is_spot")

    @property
    @pulumi.getter(name="isXenon")
    def is_xenon(self) -> pulumi.Output[Optional[bool]]:
        """
        Obsolete: If Hyper-V container app service plan <code>true</code>, <code>false</code> otherwise.
        """
        return pulumi.get(self, "is_xenon")

    @property
    @pulumi.getter
    def kind(self) -> pulumi.Output[Optional[str]]:
        """
        Kind of resource.
        """
        return pulumi.get(self, "kind")

    @property
    @pulumi.getter(name="kubeEnvironmentProfile")
    def kube_environment_profile(self) -> pulumi.Output[Optional['outputs.KubeEnvironmentProfileResponse']]:
        """
        Specification for the Kubernetes Environment to use for the App Service plan.
        """
        return pulumi.get(self, "kube_environment_profile")

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[str]:
        """
        Resource Location.
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter(name="maximumElasticWorkerCount")
    def maximum_elastic_worker_count(self) -> pulumi.Output[Optional[int]]:
        """
        Maximum number of total workers allowed for this ElasticScaleEnabled App Service Plan
        """
        return pulumi.get(self, "maximum_elastic_worker_count")

    @property
    @pulumi.getter(name="maximumNumberOfWorkers")
    def maximum_number_of_workers(self) -> pulumi.Output[int]:
        """
        Maximum number of instances that can be assigned to this App Service plan.
        """
        return pulumi.get(self, "maximum_number_of_workers")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Resource Name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="numberOfSites")
    def number_of_sites(self) -> pulumi.Output[int]:
        """
        Number of apps assigned to this App Service plan.
        """
        return pulumi.get(self, "number_of_sites")

    @property
    @pulumi.getter(name="numberOfWorkers")
    def number_of_workers(self) -> pulumi.Output[int]:
        """
        The number of instances that are assigned to this App Service plan.
        """
        return pulumi.get(self, "number_of_workers")

    @property
    @pulumi.getter(name="perSiteScaling")
    def per_site_scaling(self) -> pulumi.Output[Optional[bool]]:
        """
        If <code>true</code>, apps assigned to this App Service plan can be scaled independently.
        If <code>false</code>, apps assigned to this App Service plan will scale to all instances of the plan.
        """
        return pulumi.get(self, "per_site_scaling")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> pulumi.Output[str]:
        """
        Provisioning state of the App Service Plan.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter
    def reserved(self) -> pulumi.Output[Optional[bool]]:
        """
        If Linux app service plan <code>true</code>, <code>false</code> otherwise.
        """
        return pulumi.get(self, "reserved")

    @property
    @pulumi.getter(name="resourceGroup")
    def resource_group(self) -> pulumi.Output[str]:
        """
        Resource group of the App Service plan.
        """
        return pulumi.get(self, "resource_group")

    @property
    @pulumi.getter
    def sku(self) -> pulumi.Output[Optional['outputs.SkuDescriptionResponse']]:
        """
        Description of a SKU for a scalable resource.
        """
        return pulumi.get(self, "sku")

    @property
    @pulumi.getter(name="spotExpirationTime")
    def spot_expiration_time(self) -> pulumi.Output[Optional[str]]:
        """
        The time when the server farm expires. Valid only if it is a spot server farm.
        """
        return pulumi.get(self, "spot_expiration_time")

    @property
    @pulumi.getter
    def status(self) -> pulumi.Output[str]:
        """
        App Service plan status.
        """
        return pulumi.get(self, "status")

    @property
    @pulumi.getter
    def subscription(self) -> pulumi.Output[str]:
        """
        App Service plan subscription.
        """
        return pulumi.get(self, "subscription")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        Resource tags.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="targetWorkerCount")
    def target_worker_count(self) -> pulumi.Output[Optional[int]]:
        """
        Scaling worker count.
        """
        return pulumi.get(self, "target_worker_count")

    @property
    @pulumi.getter(name="targetWorkerSizeId")
    def target_worker_size_id(self) -> pulumi.Output[Optional[int]]:
        """
        Scaling worker size ID.
        """
        return pulumi.get(self, "target_worker_size_id")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        Resource type.
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter(name="workerTierName")
    def worker_tier_name(self) -> pulumi.Output[Optional[str]]:
        """
        Target worker tier assigned to the App Service plan.
        """
        return pulumi.get(self, "worker_tier_name")

    @property
    @pulumi.getter(name="zoneRedundant")
    def zone_redundant(self) -> pulumi.Output[Optional[bool]]:
        """
        If <code>true</code>, this App Service Plan will perform availability zone balancing.
        If <code>false</code>, this App Service Plan will not perform availability zone balancing.
        """
        return pulumi.get(self, "zone_redundant")

