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
    'GetBlobContainerResult',
    'AwaitableGetBlobContainerResult',
    'get_blob_container',
    'get_blob_container_output',
]

@pulumi.output_type
class GetBlobContainerResult:
    """
    Properties of the blob container, including Id, resource name, resource type, Etag.
    """
    def __init__(__self__, default_encryption_scope=None, deleted=None, deleted_time=None, deny_encryption_scope_override=None, enable_nfs_v3_all_squash=None, enable_nfs_v3_root_squash=None, etag=None, has_immutability_policy=None, has_legal_hold=None, id=None, immutability_policy=None, immutable_storage_with_versioning=None, last_modified_time=None, lease_duration=None, lease_state=None, lease_status=None, legal_hold=None, metadata=None, name=None, public_access=None, remaining_retention_days=None, type=None, version=None):
        if default_encryption_scope and not isinstance(default_encryption_scope, str):
            raise TypeError("Expected argument 'default_encryption_scope' to be a str")
        pulumi.set(__self__, "default_encryption_scope", default_encryption_scope)
        if deleted and not isinstance(deleted, bool):
            raise TypeError("Expected argument 'deleted' to be a bool")
        pulumi.set(__self__, "deleted", deleted)
        if deleted_time and not isinstance(deleted_time, str):
            raise TypeError("Expected argument 'deleted_time' to be a str")
        pulumi.set(__self__, "deleted_time", deleted_time)
        if deny_encryption_scope_override and not isinstance(deny_encryption_scope_override, bool):
            raise TypeError("Expected argument 'deny_encryption_scope_override' to be a bool")
        pulumi.set(__self__, "deny_encryption_scope_override", deny_encryption_scope_override)
        if enable_nfs_v3_all_squash and not isinstance(enable_nfs_v3_all_squash, bool):
            raise TypeError("Expected argument 'enable_nfs_v3_all_squash' to be a bool")
        pulumi.set(__self__, "enable_nfs_v3_all_squash", enable_nfs_v3_all_squash)
        if enable_nfs_v3_root_squash and not isinstance(enable_nfs_v3_root_squash, bool):
            raise TypeError("Expected argument 'enable_nfs_v3_root_squash' to be a bool")
        pulumi.set(__self__, "enable_nfs_v3_root_squash", enable_nfs_v3_root_squash)
        if etag and not isinstance(etag, str):
            raise TypeError("Expected argument 'etag' to be a str")
        pulumi.set(__self__, "etag", etag)
        if has_immutability_policy and not isinstance(has_immutability_policy, bool):
            raise TypeError("Expected argument 'has_immutability_policy' to be a bool")
        pulumi.set(__self__, "has_immutability_policy", has_immutability_policy)
        if has_legal_hold and not isinstance(has_legal_hold, bool):
            raise TypeError("Expected argument 'has_legal_hold' to be a bool")
        pulumi.set(__self__, "has_legal_hold", has_legal_hold)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if immutability_policy and not isinstance(immutability_policy, dict):
            raise TypeError("Expected argument 'immutability_policy' to be a dict")
        pulumi.set(__self__, "immutability_policy", immutability_policy)
        if immutable_storage_with_versioning and not isinstance(immutable_storage_with_versioning, dict):
            raise TypeError("Expected argument 'immutable_storage_with_versioning' to be a dict")
        pulumi.set(__self__, "immutable_storage_with_versioning", immutable_storage_with_versioning)
        if last_modified_time and not isinstance(last_modified_time, str):
            raise TypeError("Expected argument 'last_modified_time' to be a str")
        pulumi.set(__self__, "last_modified_time", last_modified_time)
        if lease_duration and not isinstance(lease_duration, str):
            raise TypeError("Expected argument 'lease_duration' to be a str")
        pulumi.set(__self__, "lease_duration", lease_duration)
        if lease_state and not isinstance(lease_state, str):
            raise TypeError("Expected argument 'lease_state' to be a str")
        pulumi.set(__self__, "lease_state", lease_state)
        if lease_status and not isinstance(lease_status, str):
            raise TypeError("Expected argument 'lease_status' to be a str")
        pulumi.set(__self__, "lease_status", lease_status)
        if legal_hold and not isinstance(legal_hold, dict):
            raise TypeError("Expected argument 'legal_hold' to be a dict")
        pulumi.set(__self__, "legal_hold", legal_hold)
        if metadata and not isinstance(metadata, dict):
            raise TypeError("Expected argument 'metadata' to be a dict")
        pulumi.set(__self__, "metadata", metadata)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if public_access and not isinstance(public_access, str):
            raise TypeError("Expected argument 'public_access' to be a str")
        pulumi.set(__self__, "public_access", public_access)
        if remaining_retention_days and not isinstance(remaining_retention_days, int):
            raise TypeError("Expected argument 'remaining_retention_days' to be a int")
        pulumi.set(__self__, "remaining_retention_days", remaining_retention_days)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)
        if version and not isinstance(version, str):
            raise TypeError("Expected argument 'version' to be a str")
        pulumi.set(__self__, "version", version)

    @property
    @pulumi.getter(name="defaultEncryptionScope")
    def default_encryption_scope(self) -> Optional[str]:
        """
        Default the container to use specified encryption scope for all writes.
        """
        return pulumi.get(self, "default_encryption_scope")

    @property
    @pulumi.getter
    def deleted(self) -> bool:
        """
        Indicates whether the blob container was deleted.
        """
        return pulumi.get(self, "deleted")

    @property
    @pulumi.getter(name="deletedTime")
    def deleted_time(self) -> str:
        """
        Blob container deletion time.
        """
        return pulumi.get(self, "deleted_time")

    @property
    @pulumi.getter(name="denyEncryptionScopeOverride")
    def deny_encryption_scope_override(self) -> Optional[bool]:
        """
        Block override of encryption scope from the container default.
        """
        return pulumi.get(self, "deny_encryption_scope_override")

    @property
    @pulumi.getter(name="enableNfsV3AllSquash")
    def enable_nfs_v3_all_squash(self) -> Optional[bool]:
        """
        Enable NFSv3 all squash on blob container.
        """
        return pulumi.get(self, "enable_nfs_v3_all_squash")

    @property
    @pulumi.getter(name="enableNfsV3RootSquash")
    def enable_nfs_v3_root_squash(self) -> Optional[bool]:
        """
        Enable NFSv3 root squash on blob container.
        """
        return pulumi.get(self, "enable_nfs_v3_root_squash")

    @property
    @pulumi.getter
    def etag(self) -> str:
        """
        Resource Etag.
        """
        return pulumi.get(self, "etag")

    @property
    @pulumi.getter(name="hasImmutabilityPolicy")
    def has_immutability_policy(self) -> bool:
        """
        The hasImmutabilityPolicy public property is set to true by SRP if ImmutabilityPolicy has been created for this container. The hasImmutabilityPolicy public property is set to false by SRP if ImmutabilityPolicy has not been created for this container.
        """
        return pulumi.get(self, "has_immutability_policy")

    @property
    @pulumi.getter(name="hasLegalHold")
    def has_legal_hold(self) -> bool:
        """
        The hasLegalHold public property is set to true by SRP if there are at least one existing tag. The hasLegalHold public property is set to false by SRP if all existing legal hold tags are cleared out. There can be a maximum of 1000 blob containers with hasLegalHold=true for a given account.
        """
        return pulumi.get(self, "has_legal_hold")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Fully qualified resource ID for the resource. Ex - /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/{resourceProviderNamespace}/{resourceType}/{resourceName}
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="immutabilityPolicy")
    def immutability_policy(self) -> 'outputs.ImmutabilityPolicyPropertiesResponse':
        """
        The ImmutabilityPolicy property of the container.
        """
        return pulumi.get(self, "immutability_policy")

    @property
    @pulumi.getter(name="immutableStorageWithVersioning")
    def immutable_storage_with_versioning(self) -> Optional['outputs.ImmutableStorageWithVersioningResponse']:
        """
        The object level immutability property of the container. The property is immutable and can only be set to true at the container creation time. Existing containers must undergo a migration process.
        """
        return pulumi.get(self, "immutable_storage_with_versioning")

    @property
    @pulumi.getter(name="lastModifiedTime")
    def last_modified_time(self) -> str:
        """
        Returns the date and time the container was last modified.
        """
        return pulumi.get(self, "last_modified_time")

    @property
    @pulumi.getter(name="leaseDuration")
    def lease_duration(self) -> str:
        """
        Specifies whether the lease on a container is of infinite or fixed duration, only when the container is leased.
        """
        return pulumi.get(self, "lease_duration")

    @property
    @pulumi.getter(name="leaseState")
    def lease_state(self) -> str:
        """
        Lease state of the container.
        """
        return pulumi.get(self, "lease_state")

    @property
    @pulumi.getter(name="leaseStatus")
    def lease_status(self) -> str:
        """
        The lease status of the container.
        """
        return pulumi.get(self, "lease_status")

    @property
    @pulumi.getter(name="legalHold")
    def legal_hold(self) -> 'outputs.LegalHoldPropertiesResponse':
        """
        The LegalHold property of the container.
        """
        return pulumi.get(self, "legal_hold")

    @property
    @pulumi.getter
    def metadata(self) -> Optional[Mapping[str, str]]:
        """
        A name-value pair to associate with the container as metadata.
        """
        return pulumi.get(self, "metadata")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The name of the resource
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="publicAccess")
    def public_access(self) -> Optional[str]:
        """
        Specifies whether data in the container may be accessed publicly and the level of access.
        """
        return pulumi.get(self, "public_access")

    @property
    @pulumi.getter(name="remainingRetentionDays")
    def remaining_retention_days(self) -> int:
        """
        Remaining retention days for soft deleted blob container.
        """
        return pulumi.get(self, "remaining_retention_days")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        The type of the resource. E.g. "Microsoft.Compute/virtualMachines" or "Microsoft.Storage/storageAccounts"
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter
    def version(self) -> str:
        """
        The version of the deleted blob container.
        """
        return pulumi.get(self, "version")


class AwaitableGetBlobContainerResult(GetBlobContainerResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetBlobContainerResult(
            default_encryption_scope=self.default_encryption_scope,
            deleted=self.deleted,
            deleted_time=self.deleted_time,
            deny_encryption_scope_override=self.deny_encryption_scope_override,
            enable_nfs_v3_all_squash=self.enable_nfs_v3_all_squash,
            enable_nfs_v3_root_squash=self.enable_nfs_v3_root_squash,
            etag=self.etag,
            has_immutability_policy=self.has_immutability_policy,
            has_legal_hold=self.has_legal_hold,
            id=self.id,
            immutability_policy=self.immutability_policy,
            immutable_storage_with_versioning=self.immutable_storage_with_versioning,
            last_modified_time=self.last_modified_time,
            lease_duration=self.lease_duration,
            lease_state=self.lease_state,
            lease_status=self.lease_status,
            legal_hold=self.legal_hold,
            metadata=self.metadata,
            name=self.name,
            public_access=self.public_access,
            remaining_retention_days=self.remaining_retention_days,
            type=self.type,
            version=self.version)


def get_blob_container(account_name: Optional[str] = None,
                       container_name: Optional[str] = None,
                       resource_group_name: Optional[str] = None,
                       opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetBlobContainerResult:
    """
    Properties of the blob container, including Id, resource name, resource type, Etag.


    :param str account_name: The name of the storage account within the specified resource group. Storage account names must be between 3 and 24 characters in length and use numbers and lower-case letters only.
    :param str container_name: The name of the blob container within the specified storage account. Blob container names must be between 3 and 63 characters in length and use numbers, lower-case letters and dash (-) only. Every dash (-) character must be immediately preceded and followed by a letter or number.
    :param str resource_group_name: The name of the resource group within the user's subscription. The name is case insensitive.
    """
    __args__ = dict()
    __args__['accountName'] = account_name
    __args__['containerName'] = container_name
    __args__['resourceGroupName'] = resource_group_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:storage/v20210901:getBlobContainer', __args__, opts=opts, typ=GetBlobContainerResult).value

    return AwaitableGetBlobContainerResult(
        default_encryption_scope=__ret__.default_encryption_scope,
        deleted=__ret__.deleted,
        deleted_time=__ret__.deleted_time,
        deny_encryption_scope_override=__ret__.deny_encryption_scope_override,
        enable_nfs_v3_all_squash=__ret__.enable_nfs_v3_all_squash,
        enable_nfs_v3_root_squash=__ret__.enable_nfs_v3_root_squash,
        etag=__ret__.etag,
        has_immutability_policy=__ret__.has_immutability_policy,
        has_legal_hold=__ret__.has_legal_hold,
        id=__ret__.id,
        immutability_policy=__ret__.immutability_policy,
        immutable_storage_with_versioning=__ret__.immutable_storage_with_versioning,
        last_modified_time=__ret__.last_modified_time,
        lease_duration=__ret__.lease_duration,
        lease_state=__ret__.lease_state,
        lease_status=__ret__.lease_status,
        legal_hold=__ret__.legal_hold,
        metadata=__ret__.metadata,
        name=__ret__.name,
        public_access=__ret__.public_access,
        remaining_retention_days=__ret__.remaining_retention_days,
        type=__ret__.type,
        version=__ret__.version)


@_utilities.lift_output_func(get_blob_container)
def get_blob_container_output(account_name: Optional[pulumi.Input[str]] = None,
                              container_name: Optional[pulumi.Input[str]] = None,
                              resource_group_name: Optional[pulumi.Input[str]] = None,
                              opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetBlobContainerResult]:
    """
    Properties of the blob container, including Id, resource name, resource type, Etag.


    :param str account_name: The name of the storage account within the specified resource group. Storage account names must be between 3 and 24 characters in length and use numbers and lower-case letters only.
    :param str container_name: The name of the blob container within the specified storage account. Blob container names must be between 3 and 63 characters in length and use numbers, lower-case letters and dash (-) only. Every dash (-) character must be immediately preceded and followed by a letter or number.
    :param str resource_group_name: The name of the resource group within the user's subscription. The name is case insensitive.
    """
    ...
