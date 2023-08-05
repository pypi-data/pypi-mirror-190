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

__all__ = ['ManagementLockAtSubscriptionLevelArgs', 'ManagementLockAtSubscriptionLevel']

@pulumi.input_type
class ManagementLockAtSubscriptionLevelArgs:
    def __init__(__self__, *,
                 level: pulumi.Input[Union[str, 'LockLevel']],
                 lock_name: Optional[pulumi.Input[str]] = None,
                 notes: Optional[pulumi.Input[str]] = None,
                 owners: Optional[pulumi.Input[Sequence[pulumi.Input['ManagementLockOwnerArgs']]]] = None):
        """
        The set of arguments for constructing a ManagementLockAtSubscriptionLevel resource.
        :param pulumi.Input[Union[str, 'LockLevel']] level: The level of the lock. Possible values are: NotSpecified, CanNotDelete, ReadOnly. CanNotDelete means authorized users are able to read and modify the resources, but not delete. ReadOnly means authorized users can only read from a resource, but they can't modify or delete it.
        :param pulumi.Input[str] lock_name: The name of lock. The lock name can be a maximum of 260 characters. It cannot contain <, > %, &, :, \\, ?, /, or any control characters.
        :param pulumi.Input[str] notes: Notes about the lock. Maximum of 512 characters.
        :param pulumi.Input[Sequence[pulumi.Input['ManagementLockOwnerArgs']]] owners: The owners of the lock.
        """
        pulumi.set(__self__, "level", level)
        if lock_name is not None:
            pulumi.set(__self__, "lock_name", lock_name)
        if notes is not None:
            pulumi.set(__self__, "notes", notes)
        if owners is not None:
            pulumi.set(__self__, "owners", owners)

    @property
    @pulumi.getter
    def level(self) -> pulumi.Input[Union[str, 'LockLevel']]:
        """
        The level of the lock. Possible values are: NotSpecified, CanNotDelete, ReadOnly. CanNotDelete means authorized users are able to read and modify the resources, but not delete. ReadOnly means authorized users can only read from a resource, but they can't modify or delete it.
        """
        return pulumi.get(self, "level")

    @level.setter
    def level(self, value: pulumi.Input[Union[str, 'LockLevel']]):
        pulumi.set(self, "level", value)

    @property
    @pulumi.getter(name="lockName")
    def lock_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of lock. The lock name can be a maximum of 260 characters. It cannot contain <, > %, &, :, \\, ?, /, or any control characters.
        """
        return pulumi.get(self, "lock_name")

    @lock_name.setter
    def lock_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "lock_name", value)

    @property
    @pulumi.getter
    def notes(self) -> Optional[pulumi.Input[str]]:
        """
        Notes about the lock. Maximum of 512 characters.
        """
        return pulumi.get(self, "notes")

    @notes.setter
    def notes(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "notes", value)

    @property
    @pulumi.getter
    def owners(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['ManagementLockOwnerArgs']]]]:
        """
        The owners of the lock.
        """
        return pulumi.get(self, "owners")

    @owners.setter
    def owners(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['ManagementLockOwnerArgs']]]]):
        pulumi.set(self, "owners", value)


class ManagementLockAtSubscriptionLevel(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 level: Optional[pulumi.Input[Union[str, 'LockLevel']]] = None,
                 lock_name: Optional[pulumi.Input[str]] = None,
                 notes: Optional[pulumi.Input[str]] = None,
                 owners: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ManagementLockOwnerArgs']]]]] = None,
                 __props__=None):
        """
        The lock information.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Union[str, 'LockLevel']] level: The level of the lock. Possible values are: NotSpecified, CanNotDelete, ReadOnly. CanNotDelete means authorized users are able to read and modify the resources, but not delete. ReadOnly means authorized users can only read from a resource, but they can't modify or delete it.
        :param pulumi.Input[str] lock_name: The name of lock. The lock name can be a maximum of 260 characters. It cannot contain <, > %, &, :, \\, ?, /, or any control characters.
        :param pulumi.Input[str] notes: Notes about the lock. Maximum of 512 characters.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ManagementLockOwnerArgs']]]] owners: The owners of the lock.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: ManagementLockAtSubscriptionLevelArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        The lock information.

        :param str resource_name: The name of the resource.
        :param ManagementLockAtSubscriptionLevelArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ManagementLockAtSubscriptionLevelArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 level: Optional[pulumi.Input[Union[str, 'LockLevel']]] = None,
                 lock_name: Optional[pulumi.Input[str]] = None,
                 notes: Optional[pulumi.Input[str]] = None,
                 owners: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ManagementLockOwnerArgs']]]]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = ManagementLockAtSubscriptionLevelArgs.__new__(ManagementLockAtSubscriptionLevelArgs)

            if level is None and not opts.urn:
                raise TypeError("Missing required property 'level'")
            __props__.__dict__["level"] = level
            __props__.__dict__["lock_name"] = lock_name
            __props__.__dict__["notes"] = notes
            __props__.__dict__["owners"] = owners
            __props__.__dict__["name"] = None
            __props__.__dict__["type"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-native:authorization:ManagementLockAtSubscriptionLevel"), pulumi.Alias(type_="azure-native:authorization/v20150101:ManagementLockAtSubscriptionLevel"), pulumi.Alias(type_="azure-native:authorization/v20160901:ManagementLockAtSubscriptionLevel"), pulumi.Alias(type_="azure-native:authorization/v20200501:ManagementLockAtSubscriptionLevel")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(ManagementLockAtSubscriptionLevel, __self__).__init__(
            'azure-native:authorization/v20170401:ManagementLockAtSubscriptionLevel',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'ManagementLockAtSubscriptionLevel':
        """
        Get an existing ManagementLockAtSubscriptionLevel resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = ManagementLockAtSubscriptionLevelArgs.__new__(ManagementLockAtSubscriptionLevelArgs)

        __props__.__dict__["level"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["notes"] = None
        __props__.__dict__["owners"] = None
        __props__.__dict__["type"] = None
        return ManagementLockAtSubscriptionLevel(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def level(self) -> pulumi.Output[str]:
        """
        The level of the lock. Possible values are: NotSpecified, CanNotDelete, ReadOnly. CanNotDelete means authorized users are able to read and modify the resources, but not delete. ReadOnly means authorized users can only read from a resource, but they can't modify or delete it.
        """
        return pulumi.get(self, "level")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the lock.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def notes(self) -> pulumi.Output[Optional[str]]:
        """
        Notes about the lock. Maximum of 512 characters.
        """
        return pulumi.get(self, "notes")

    @property
    @pulumi.getter
    def owners(self) -> pulumi.Output[Optional[Sequence['outputs.ManagementLockOwnerResponse']]]:
        """
        The owners of the lock.
        """
        return pulumi.get(self, "owners")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        The resource type of the lock - Microsoft.Authorization/locks.
        """
        return pulumi.get(self, "type")

