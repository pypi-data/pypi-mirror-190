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

__all__ = ['OpenShiftClusterArgs', 'OpenShiftCluster']

@pulumi.input_type
class OpenShiftClusterArgs:
    def __init__(__self__, *,
                 resource_group_name: pulumi.Input[str],
                 apiserver_profile: Optional[pulumi.Input['APIServerProfileArgs']] = None,
                 cluster_profile: Optional[pulumi.Input['ClusterProfileArgs']] = None,
                 console_profile: Optional[pulumi.Input['ConsoleProfileArgs']] = None,
                 ingress_profiles: Optional[pulumi.Input[Sequence[pulumi.Input['IngressProfileArgs']]]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 master_profile: Optional[pulumi.Input['MasterProfileArgs']] = None,
                 network_profile: Optional[pulumi.Input['NetworkProfileArgs']] = None,
                 provisioning_state: Optional[pulumi.Input[str]] = None,
                 resource_name: Optional[pulumi.Input[str]] = None,
                 service_principal_profile: Optional[pulumi.Input['ServicePrincipalProfileArgs']] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 worker_profiles: Optional[pulumi.Input[Sequence[pulumi.Input['WorkerProfileArgs']]]] = None):
        """
        The set of arguments for constructing a OpenShiftCluster resource.
        :param pulumi.Input[str] resource_group_name: The name of the resource group. The name is case insensitive.
        :param pulumi.Input['APIServerProfileArgs'] apiserver_profile: The cluster API server profile.
        :param pulumi.Input['ClusterProfileArgs'] cluster_profile: The cluster profile.
        :param pulumi.Input['ConsoleProfileArgs'] console_profile: The console profile.
        :param pulumi.Input[Sequence[pulumi.Input['IngressProfileArgs']]] ingress_profiles: The cluster ingress profiles.
        :param pulumi.Input[str] location: The geo-location where the resource lives
        :param pulumi.Input['MasterProfileArgs'] master_profile: The cluster master profile.
        :param pulumi.Input['NetworkProfileArgs'] network_profile: The cluster network profile.
        :param pulumi.Input[str] provisioning_state: The cluster provisioning state.
        :param pulumi.Input[str] resource_name: The name of the OpenShift cluster resource.
        :param pulumi.Input['ServicePrincipalProfileArgs'] service_principal_profile: The cluster service principal profile.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Resource tags.
        :param pulumi.Input[Sequence[pulumi.Input['WorkerProfileArgs']]] worker_profiles: The cluster worker profiles.
        """
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        if apiserver_profile is not None:
            pulumi.set(__self__, "apiserver_profile", apiserver_profile)
        if cluster_profile is not None:
            pulumi.set(__self__, "cluster_profile", cluster_profile)
        if console_profile is not None:
            pulumi.set(__self__, "console_profile", console_profile)
        if ingress_profiles is not None:
            pulumi.set(__self__, "ingress_profiles", ingress_profiles)
        if location is not None:
            pulumi.set(__self__, "location", location)
        if master_profile is not None:
            pulumi.set(__self__, "master_profile", master_profile)
        if network_profile is not None:
            pulumi.set(__self__, "network_profile", network_profile)
        if provisioning_state is not None:
            pulumi.set(__self__, "provisioning_state", provisioning_state)
        if resource_name is not None:
            pulumi.set(__self__, "resource_name", resource_name)
        if service_principal_profile is not None:
            pulumi.set(__self__, "service_principal_profile", service_principal_profile)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)
        if worker_profiles is not None:
            pulumi.set(__self__, "worker_profiles", worker_profiles)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Input[str]:
        """
        The name of the resource group. The name is case insensitive.
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "resource_group_name", value)

    @property
    @pulumi.getter(name="apiserverProfile")
    def apiserver_profile(self) -> Optional[pulumi.Input['APIServerProfileArgs']]:
        """
        The cluster API server profile.
        """
        return pulumi.get(self, "apiserver_profile")

    @apiserver_profile.setter
    def apiserver_profile(self, value: Optional[pulumi.Input['APIServerProfileArgs']]):
        pulumi.set(self, "apiserver_profile", value)

    @property
    @pulumi.getter(name="clusterProfile")
    def cluster_profile(self) -> Optional[pulumi.Input['ClusterProfileArgs']]:
        """
        The cluster profile.
        """
        return pulumi.get(self, "cluster_profile")

    @cluster_profile.setter
    def cluster_profile(self, value: Optional[pulumi.Input['ClusterProfileArgs']]):
        pulumi.set(self, "cluster_profile", value)

    @property
    @pulumi.getter(name="consoleProfile")
    def console_profile(self) -> Optional[pulumi.Input['ConsoleProfileArgs']]:
        """
        The console profile.
        """
        return pulumi.get(self, "console_profile")

    @console_profile.setter
    def console_profile(self, value: Optional[pulumi.Input['ConsoleProfileArgs']]):
        pulumi.set(self, "console_profile", value)

    @property
    @pulumi.getter(name="ingressProfiles")
    def ingress_profiles(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['IngressProfileArgs']]]]:
        """
        The cluster ingress profiles.
        """
        return pulumi.get(self, "ingress_profiles")

    @ingress_profiles.setter
    def ingress_profiles(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['IngressProfileArgs']]]]):
        pulumi.set(self, "ingress_profiles", value)

    @property
    @pulumi.getter
    def location(self) -> Optional[pulumi.Input[str]]:
        """
        The geo-location where the resource lives
        """
        return pulumi.get(self, "location")

    @location.setter
    def location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "location", value)

    @property
    @pulumi.getter(name="masterProfile")
    def master_profile(self) -> Optional[pulumi.Input['MasterProfileArgs']]:
        """
        The cluster master profile.
        """
        return pulumi.get(self, "master_profile")

    @master_profile.setter
    def master_profile(self, value: Optional[pulumi.Input['MasterProfileArgs']]):
        pulumi.set(self, "master_profile", value)

    @property
    @pulumi.getter(name="networkProfile")
    def network_profile(self) -> Optional[pulumi.Input['NetworkProfileArgs']]:
        """
        The cluster network profile.
        """
        return pulumi.get(self, "network_profile")

    @network_profile.setter
    def network_profile(self, value: Optional[pulumi.Input['NetworkProfileArgs']]):
        pulumi.set(self, "network_profile", value)

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> Optional[pulumi.Input[str]]:
        """
        The cluster provisioning state.
        """
        return pulumi.get(self, "provisioning_state")

    @provisioning_state.setter
    def provisioning_state(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "provisioning_state", value)

    @property
    @pulumi.getter(name="resourceName")
    def resource_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the OpenShift cluster resource.
        """
        return pulumi.get(self, "resource_name")

    @resource_name.setter
    def resource_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "resource_name", value)

    @property
    @pulumi.getter(name="servicePrincipalProfile")
    def service_principal_profile(self) -> Optional[pulumi.Input['ServicePrincipalProfileArgs']]:
        """
        The cluster service principal profile.
        """
        return pulumi.get(self, "service_principal_profile")

    @service_principal_profile.setter
    def service_principal_profile(self, value: Optional[pulumi.Input['ServicePrincipalProfileArgs']]):
        pulumi.set(self, "service_principal_profile", value)

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
    @pulumi.getter(name="workerProfiles")
    def worker_profiles(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['WorkerProfileArgs']]]]:
        """
        The cluster worker profiles.
        """
        return pulumi.get(self, "worker_profiles")

    @worker_profiles.setter
    def worker_profiles(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['WorkerProfileArgs']]]]):
        pulumi.set(self, "worker_profiles", value)


class OpenShiftCluster(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 apiserver_profile: Optional[pulumi.Input[pulumi.InputType['APIServerProfileArgs']]] = None,
                 cluster_profile: Optional[pulumi.Input[pulumi.InputType['ClusterProfileArgs']]] = None,
                 console_profile: Optional[pulumi.Input[pulumi.InputType['ConsoleProfileArgs']]] = None,
                 ingress_profiles: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['IngressProfileArgs']]]]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 master_profile: Optional[pulumi.Input[pulumi.InputType['MasterProfileArgs']]] = None,
                 network_profile: Optional[pulumi.Input[pulumi.InputType['NetworkProfileArgs']]] = None,
                 provisioning_state: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 resource_name_: Optional[pulumi.Input[str]] = None,
                 service_principal_profile: Optional[pulumi.Input[pulumi.InputType['ServicePrincipalProfileArgs']]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 worker_profiles: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['WorkerProfileArgs']]]]] = None,
                 __props__=None):
        """
        OpenShiftCluster represents an Azure Red Hat OpenShift cluster.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[pulumi.InputType['APIServerProfileArgs']] apiserver_profile: The cluster API server profile.
        :param pulumi.Input[pulumi.InputType['ClusterProfileArgs']] cluster_profile: The cluster profile.
        :param pulumi.Input[pulumi.InputType['ConsoleProfileArgs']] console_profile: The console profile.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['IngressProfileArgs']]]] ingress_profiles: The cluster ingress profiles.
        :param pulumi.Input[str] location: The geo-location where the resource lives
        :param pulumi.Input[pulumi.InputType['MasterProfileArgs']] master_profile: The cluster master profile.
        :param pulumi.Input[pulumi.InputType['NetworkProfileArgs']] network_profile: The cluster network profile.
        :param pulumi.Input[str] provisioning_state: The cluster provisioning state.
        :param pulumi.Input[str] resource_group_name: The name of the resource group. The name is case insensitive.
        :param pulumi.Input[str] resource_name_: The name of the OpenShift cluster resource.
        :param pulumi.Input[pulumi.InputType['ServicePrincipalProfileArgs']] service_principal_profile: The cluster service principal profile.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Resource tags.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['WorkerProfileArgs']]]] worker_profiles: The cluster worker profiles.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: OpenShiftClusterArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        OpenShiftCluster represents an Azure Red Hat OpenShift cluster.

        :param str resource_name: The name of the resource.
        :param OpenShiftClusterArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(OpenShiftClusterArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 apiserver_profile: Optional[pulumi.Input[pulumi.InputType['APIServerProfileArgs']]] = None,
                 cluster_profile: Optional[pulumi.Input[pulumi.InputType['ClusterProfileArgs']]] = None,
                 console_profile: Optional[pulumi.Input[pulumi.InputType['ConsoleProfileArgs']]] = None,
                 ingress_profiles: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['IngressProfileArgs']]]]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 master_profile: Optional[pulumi.Input[pulumi.InputType['MasterProfileArgs']]] = None,
                 network_profile: Optional[pulumi.Input[pulumi.InputType['NetworkProfileArgs']]] = None,
                 provisioning_state: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 resource_name_: Optional[pulumi.Input[str]] = None,
                 service_principal_profile: Optional[pulumi.Input[pulumi.InputType['ServicePrincipalProfileArgs']]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 worker_profiles: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['WorkerProfileArgs']]]]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = OpenShiftClusterArgs.__new__(OpenShiftClusterArgs)

            __props__.__dict__["apiserver_profile"] = apiserver_profile
            __props__.__dict__["cluster_profile"] = cluster_profile
            __props__.__dict__["console_profile"] = console_profile
            __props__.__dict__["ingress_profiles"] = ingress_profiles
            __props__.__dict__["location"] = location
            __props__.__dict__["master_profile"] = master_profile
            __props__.__dict__["network_profile"] = network_profile
            __props__.__dict__["provisioning_state"] = provisioning_state
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            __props__.__dict__["resource_name"] = resource_name_
            __props__.__dict__["service_principal_profile"] = service_principal_profile
            __props__.__dict__["tags"] = tags
            __props__.__dict__["worker_profiles"] = worker_profiles
            __props__.__dict__["name"] = None
            __props__.__dict__["system_data"] = None
            __props__.__dict__["type"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-native:redhatopenshift:OpenShiftCluster"), pulumi.Alias(type_="azure-native:redhatopenshift/v20200430:OpenShiftCluster"), pulumi.Alias(type_="azure-native:redhatopenshift/v20210901preview:OpenShiftCluster"), pulumi.Alias(type_="azure-native:redhatopenshift/v20220904:OpenShiftCluster")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(OpenShiftCluster, __self__).__init__(
            'azure-native:redhatopenshift/v20220401:OpenShiftCluster',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'OpenShiftCluster':
        """
        Get an existing OpenShiftCluster resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = OpenShiftClusterArgs.__new__(OpenShiftClusterArgs)

        __props__.__dict__["apiserver_profile"] = None
        __props__.__dict__["cluster_profile"] = None
        __props__.__dict__["console_profile"] = None
        __props__.__dict__["ingress_profiles"] = None
        __props__.__dict__["location"] = None
        __props__.__dict__["master_profile"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["network_profile"] = None
        __props__.__dict__["provisioning_state"] = None
        __props__.__dict__["service_principal_profile"] = None
        __props__.__dict__["system_data"] = None
        __props__.__dict__["tags"] = None
        __props__.__dict__["type"] = None
        __props__.__dict__["worker_profiles"] = None
        return OpenShiftCluster(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="apiserverProfile")
    def apiserver_profile(self) -> pulumi.Output[Optional['outputs.APIServerProfileResponse']]:
        """
        The cluster API server profile.
        """
        return pulumi.get(self, "apiserver_profile")

    @property
    @pulumi.getter(name="clusterProfile")
    def cluster_profile(self) -> pulumi.Output[Optional['outputs.ClusterProfileResponse']]:
        """
        The cluster profile.
        """
        return pulumi.get(self, "cluster_profile")

    @property
    @pulumi.getter(name="consoleProfile")
    def console_profile(self) -> pulumi.Output[Optional['outputs.ConsoleProfileResponse']]:
        """
        The console profile.
        """
        return pulumi.get(self, "console_profile")

    @property
    @pulumi.getter(name="ingressProfiles")
    def ingress_profiles(self) -> pulumi.Output[Optional[Sequence['outputs.IngressProfileResponse']]]:
        """
        The cluster ingress profiles.
        """
        return pulumi.get(self, "ingress_profiles")

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[str]:
        """
        The geo-location where the resource lives
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter(name="masterProfile")
    def master_profile(self) -> pulumi.Output[Optional['outputs.MasterProfileResponse']]:
        """
        The cluster master profile.
        """
        return pulumi.get(self, "master_profile")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the resource
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="networkProfile")
    def network_profile(self) -> pulumi.Output[Optional['outputs.NetworkProfileResponse']]:
        """
        The cluster network profile.
        """
        return pulumi.get(self, "network_profile")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> pulumi.Output[Optional[str]]:
        """
        The cluster provisioning state.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter(name="servicePrincipalProfile")
    def service_principal_profile(self) -> pulumi.Output[Optional['outputs.ServicePrincipalProfileResponse']]:
        """
        The cluster service principal profile.
        """
        return pulumi.get(self, "service_principal_profile")

    @property
    @pulumi.getter(name="systemData")
    def system_data(self) -> pulumi.Output['outputs.SystemDataResponse']:
        """
        The system meta data relating to this resource.
        """
        return pulumi.get(self, "system_data")

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
        The type of the resource. E.g. "Microsoft.Compute/virtualMachines" or "Microsoft.Storage/storageAccounts"
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter(name="workerProfiles")
    def worker_profiles(self) -> pulumi.Output[Optional[Sequence['outputs.WorkerProfileResponse']]]:
        """
        The cluster worker profiles.
        """
        return pulumi.get(self, "worker_profiles")

