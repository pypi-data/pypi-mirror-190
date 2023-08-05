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

__all__ = ['ApplicationGroupArgs', 'ApplicationGroup']

@pulumi.input_type
class ApplicationGroupArgs:
    def __init__(__self__, *,
                 client_app_group_identifier: pulumi.Input[str],
                 namespace_name: pulumi.Input[str],
                 resource_group_name: pulumi.Input[str],
                 application_group_name: Optional[pulumi.Input[str]] = None,
                 is_enabled: Optional[pulumi.Input[bool]] = None,
                 policies: Optional[pulumi.Input[Sequence[pulumi.Input['ThrottlingPolicyArgs']]]] = None):
        """
        The set of arguments for constructing a ApplicationGroup resource.
        :param pulumi.Input[str] client_app_group_identifier: The Unique identifier for application group.Supports SAS(SASKeyName=KeyName) or AAD(AADAppID=Guid)
        :param pulumi.Input[str] namespace_name: The Namespace name
        :param pulumi.Input[str] resource_group_name: Name of the resource group within the azure subscription.
        :param pulumi.Input[str] application_group_name: The Application Group name 
        :param pulumi.Input[bool] is_enabled: Determines if Application Group is allowed to create connection with namespace or not. Once the isEnabled is set to false, all the existing connections of application group gets dropped and no new connections will be allowed
        :param pulumi.Input[Sequence[pulumi.Input['ThrottlingPolicyArgs']]] policies: List of group policies that define the behavior of application group. The policies can support resource governance scenarios such as limiting ingress or egress traffic.
        """
        pulumi.set(__self__, "client_app_group_identifier", client_app_group_identifier)
        pulumi.set(__self__, "namespace_name", namespace_name)
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        if application_group_name is not None:
            pulumi.set(__self__, "application_group_name", application_group_name)
        if is_enabled is not None:
            pulumi.set(__self__, "is_enabled", is_enabled)
        if policies is not None:
            pulumi.set(__self__, "policies", policies)

    @property
    @pulumi.getter(name="clientAppGroupIdentifier")
    def client_app_group_identifier(self) -> pulumi.Input[str]:
        """
        The Unique identifier for application group.Supports SAS(SASKeyName=KeyName) or AAD(AADAppID=Guid)
        """
        return pulumi.get(self, "client_app_group_identifier")

    @client_app_group_identifier.setter
    def client_app_group_identifier(self, value: pulumi.Input[str]):
        pulumi.set(self, "client_app_group_identifier", value)

    @property
    @pulumi.getter(name="namespaceName")
    def namespace_name(self) -> pulumi.Input[str]:
        """
        The Namespace name
        """
        return pulumi.get(self, "namespace_name")

    @namespace_name.setter
    def namespace_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "namespace_name", value)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Input[str]:
        """
        Name of the resource group within the azure subscription.
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "resource_group_name", value)

    @property
    @pulumi.getter(name="applicationGroupName")
    def application_group_name(self) -> Optional[pulumi.Input[str]]:
        """
        The Application Group name 
        """
        return pulumi.get(self, "application_group_name")

    @application_group_name.setter
    def application_group_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "application_group_name", value)

    @property
    @pulumi.getter(name="isEnabled")
    def is_enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        Determines if Application Group is allowed to create connection with namespace or not. Once the isEnabled is set to false, all the existing connections of application group gets dropped and no new connections will be allowed
        """
        return pulumi.get(self, "is_enabled")

    @is_enabled.setter
    def is_enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "is_enabled", value)

    @property
    @pulumi.getter
    def policies(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['ThrottlingPolicyArgs']]]]:
        """
        List of group policies that define the behavior of application group. The policies can support resource governance scenarios such as limiting ingress or egress traffic.
        """
        return pulumi.get(self, "policies")

    @policies.setter
    def policies(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['ThrottlingPolicyArgs']]]]):
        pulumi.set(self, "policies", value)


class ApplicationGroup(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 application_group_name: Optional[pulumi.Input[str]] = None,
                 client_app_group_identifier: Optional[pulumi.Input[str]] = None,
                 is_enabled: Optional[pulumi.Input[bool]] = None,
                 namespace_name: Optional[pulumi.Input[str]] = None,
                 policies: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ThrottlingPolicyArgs']]]]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        The Application Group object

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] application_group_name: The Application Group name 
        :param pulumi.Input[str] client_app_group_identifier: The Unique identifier for application group.Supports SAS(SASKeyName=KeyName) or AAD(AADAppID=Guid)
        :param pulumi.Input[bool] is_enabled: Determines if Application Group is allowed to create connection with namespace or not. Once the isEnabled is set to false, all the existing connections of application group gets dropped and no new connections will be allowed
        :param pulumi.Input[str] namespace_name: The Namespace name
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ThrottlingPolicyArgs']]]] policies: List of group policies that define the behavior of application group. The policies can support resource governance scenarios such as limiting ingress or egress traffic.
        :param pulumi.Input[str] resource_group_name: Name of the resource group within the azure subscription.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: ApplicationGroupArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        The Application Group object

        :param str resource_name: The name of the resource.
        :param ApplicationGroupArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ApplicationGroupArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 application_group_name: Optional[pulumi.Input[str]] = None,
                 client_app_group_identifier: Optional[pulumi.Input[str]] = None,
                 is_enabled: Optional[pulumi.Input[bool]] = None,
                 namespace_name: Optional[pulumi.Input[str]] = None,
                 policies: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ThrottlingPolicyArgs']]]]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = ApplicationGroupArgs.__new__(ApplicationGroupArgs)

            __props__.__dict__["application_group_name"] = application_group_name
            if client_app_group_identifier is None and not opts.urn:
                raise TypeError("Missing required property 'client_app_group_identifier'")
            __props__.__dict__["client_app_group_identifier"] = client_app_group_identifier
            __props__.__dict__["is_enabled"] = is_enabled
            if namespace_name is None and not opts.urn:
                raise TypeError("Missing required property 'namespace_name'")
            __props__.__dict__["namespace_name"] = namespace_name
            __props__.__dict__["policies"] = policies
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            __props__.__dict__["location"] = None
            __props__.__dict__["name"] = None
            __props__.__dict__["system_data"] = None
            __props__.__dict__["type"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-native:eventhub:ApplicationGroup"), pulumi.Alias(type_="azure-native:eventhub/v20221001preview:ApplicationGroup")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(ApplicationGroup, __self__).__init__(
            'azure-native:eventhub/v20220101preview:ApplicationGroup',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'ApplicationGroup':
        """
        Get an existing ApplicationGroup resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = ApplicationGroupArgs.__new__(ApplicationGroupArgs)

        __props__.__dict__["client_app_group_identifier"] = None
        __props__.__dict__["is_enabled"] = None
        __props__.__dict__["location"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["policies"] = None
        __props__.__dict__["system_data"] = None
        __props__.__dict__["type"] = None
        return ApplicationGroup(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="clientAppGroupIdentifier")
    def client_app_group_identifier(self) -> pulumi.Output[str]:
        """
        The Unique identifier for application group.Supports SAS(SASKeyName=KeyName) or AAD(AADAppID=Guid)
        """
        return pulumi.get(self, "client_app_group_identifier")

    @property
    @pulumi.getter(name="isEnabled")
    def is_enabled(self) -> pulumi.Output[Optional[bool]]:
        """
        Determines if Application Group is allowed to create connection with namespace or not. Once the isEnabled is set to false, all the existing connections of application group gets dropped and no new connections will be allowed
        """
        return pulumi.get(self, "is_enabled")

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[str]:
        """
        The geo-location where the resource lives
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the resource
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def policies(self) -> pulumi.Output[Optional[Sequence['outputs.ThrottlingPolicyResponse']]]:
        """
        List of group policies that define the behavior of application group. The policies can support resource governance scenarios such as limiting ingress or egress traffic.
        """
        return pulumi.get(self, "policies")

    @property
    @pulumi.getter(name="systemData")
    def system_data(self) -> pulumi.Output['outputs.SystemDataResponse']:
        """
        The system meta data relating to this resource.
        """
        return pulumi.get(self, "system_data")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        The type of the resource. E.g. "Microsoft.EventHub/Namespaces" or "Microsoft.EventHub/Namespaces/EventHubs"
        """
        return pulumi.get(self, "type")

