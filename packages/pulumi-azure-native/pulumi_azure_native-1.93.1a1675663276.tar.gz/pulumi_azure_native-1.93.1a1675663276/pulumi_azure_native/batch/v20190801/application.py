# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities

__all__ = ['ApplicationArgs', 'Application']

@pulumi.input_type
class ApplicationArgs:
    def __init__(__self__, *,
                 account_name: pulumi.Input[str],
                 resource_group_name: pulumi.Input[str],
                 allow_updates: Optional[pulumi.Input[bool]] = None,
                 application_name: Optional[pulumi.Input[str]] = None,
                 default_version: Optional[pulumi.Input[str]] = None,
                 display_name: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a Application resource.
        :param pulumi.Input[str] account_name: The name of the Batch account.
        :param pulumi.Input[str] resource_group_name: The name of the resource group that contains the Batch account.
        :param pulumi.Input[bool] allow_updates: A value indicating whether packages within the application may be overwritten using the same version string.
        :param pulumi.Input[str] application_name: The name of the application. This must be unique within the account.
        :param pulumi.Input[str] default_version: The package to use if a client requests the application but does not specify a version. This property can only be set to the name of an existing package.
        :param pulumi.Input[str] display_name: The display name for the application.
        """
        pulumi.set(__self__, "account_name", account_name)
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        if allow_updates is not None:
            pulumi.set(__self__, "allow_updates", allow_updates)
        if application_name is not None:
            pulumi.set(__self__, "application_name", application_name)
        if default_version is not None:
            pulumi.set(__self__, "default_version", default_version)
        if display_name is not None:
            pulumi.set(__self__, "display_name", display_name)

    @property
    @pulumi.getter(name="accountName")
    def account_name(self) -> pulumi.Input[str]:
        """
        The name of the Batch account.
        """
        return pulumi.get(self, "account_name")

    @account_name.setter
    def account_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "account_name", value)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Input[str]:
        """
        The name of the resource group that contains the Batch account.
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "resource_group_name", value)

    @property
    @pulumi.getter(name="allowUpdates")
    def allow_updates(self) -> Optional[pulumi.Input[bool]]:
        """
        A value indicating whether packages within the application may be overwritten using the same version string.
        """
        return pulumi.get(self, "allow_updates")

    @allow_updates.setter
    def allow_updates(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "allow_updates", value)

    @property
    @pulumi.getter(name="applicationName")
    def application_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the application. This must be unique within the account.
        """
        return pulumi.get(self, "application_name")

    @application_name.setter
    def application_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "application_name", value)

    @property
    @pulumi.getter(name="defaultVersion")
    def default_version(self) -> Optional[pulumi.Input[str]]:
        """
        The package to use if a client requests the application but does not specify a version. This property can only be set to the name of an existing package.
        """
        return pulumi.get(self, "default_version")

    @default_version.setter
    def default_version(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "default_version", value)

    @property
    @pulumi.getter(name="displayName")
    def display_name(self) -> Optional[pulumi.Input[str]]:
        """
        The display name for the application.
        """
        return pulumi.get(self, "display_name")

    @display_name.setter
    def display_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "display_name", value)


warnings.warn("""Version 2019-08-01 will be removed in v2 of the provider.""", DeprecationWarning)


class Application(pulumi.CustomResource):
    warnings.warn("""Version 2019-08-01 will be removed in v2 of the provider.""", DeprecationWarning)

    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 account_name: Optional[pulumi.Input[str]] = None,
                 allow_updates: Optional[pulumi.Input[bool]] = None,
                 application_name: Optional[pulumi.Input[str]] = None,
                 default_version: Optional[pulumi.Input[str]] = None,
                 display_name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Contains information about an application in a Batch account.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] account_name: The name of the Batch account.
        :param pulumi.Input[bool] allow_updates: A value indicating whether packages within the application may be overwritten using the same version string.
        :param pulumi.Input[str] application_name: The name of the application. This must be unique within the account.
        :param pulumi.Input[str] default_version: The package to use if a client requests the application but does not specify a version. This property can only be set to the name of an existing package.
        :param pulumi.Input[str] display_name: The display name for the application.
        :param pulumi.Input[str] resource_group_name: The name of the resource group that contains the Batch account.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: ApplicationArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Contains information about an application in a Batch account.

        :param str resource_name: The name of the resource.
        :param ApplicationArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ApplicationArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 account_name: Optional[pulumi.Input[str]] = None,
                 allow_updates: Optional[pulumi.Input[bool]] = None,
                 application_name: Optional[pulumi.Input[str]] = None,
                 default_version: Optional[pulumi.Input[str]] = None,
                 display_name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        pulumi.log.warn("""Application is deprecated: Version 2019-08-01 will be removed in v2 of the provider.""")
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = ApplicationArgs.__new__(ApplicationArgs)

            if account_name is None and not opts.urn:
                raise TypeError("Missing required property 'account_name'")
            __props__.__dict__["account_name"] = account_name
            __props__.__dict__["allow_updates"] = allow_updates
            __props__.__dict__["application_name"] = application_name
            __props__.__dict__["default_version"] = default_version
            __props__.__dict__["display_name"] = display_name
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            __props__.__dict__["etag"] = None
            __props__.__dict__["name"] = None
            __props__.__dict__["type"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-native:batch:Application"), pulumi.Alias(type_="azure-native:batch/v20151201:Application"), pulumi.Alias(type_="azure-native:batch/v20170101:Application"), pulumi.Alias(type_="azure-native:batch/v20170501:Application"), pulumi.Alias(type_="azure-native:batch/v20170901:Application"), pulumi.Alias(type_="azure-native:batch/v20181201:Application"), pulumi.Alias(type_="azure-native:batch/v20190401:Application"), pulumi.Alias(type_="azure-native:batch/v20200301:Application"), pulumi.Alias(type_="azure-native:batch/v20200501:Application"), pulumi.Alias(type_="azure-native:batch/v20200901:Application"), pulumi.Alias(type_="azure-native:batch/v20210101:Application"), pulumi.Alias(type_="azure-native:batch/v20210601:Application"), pulumi.Alias(type_="azure-native:batch/v20220101:Application"), pulumi.Alias(type_="azure-native:batch/v20220601:Application"), pulumi.Alias(type_="azure-native:batch/v20221001:Application")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(Application, __self__).__init__(
            'azure-native:batch/v20190801:Application',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'Application':
        """
        Get an existing Application resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = ApplicationArgs.__new__(ApplicationArgs)

        __props__.__dict__["allow_updates"] = None
        __props__.__dict__["default_version"] = None
        __props__.__dict__["display_name"] = None
        __props__.__dict__["etag"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["type"] = None
        return Application(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="allowUpdates")
    def allow_updates(self) -> pulumi.Output[Optional[bool]]:
        """
        A value indicating whether packages within the application may be overwritten using the same version string.
        """
        return pulumi.get(self, "allow_updates")

    @property
    @pulumi.getter(name="defaultVersion")
    def default_version(self) -> pulumi.Output[Optional[str]]:
        """
        The package to use if a client requests the application but does not specify a version. This property can only be set to the name of an existing package.
        """
        return pulumi.get(self, "default_version")

    @property
    @pulumi.getter(name="displayName")
    def display_name(self) -> pulumi.Output[Optional[str]]:
        """
        The display name for the application.
        """
        return pulumi.get(self, "display_name")

    @property
    @pulumi.getter
    def etag(self) -> pulumi.Output[str]:
        """
        The ETag of the resource, used for concurrency statements.
        """
        return pulumi.get(self, "etag")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the resource.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        The type of the resource.
        """
        return pulumi.get(self, "type")

