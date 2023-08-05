# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from ._enums import *

__all__ = [
    'AuthConfigArgs',
    'BackupArgs',
    'DataEncryptionArgs',
    'HighAvailabilityArgs',
    'MaintenanceWindowArgs',
    'NetworkArgs',
    'SkuArgs',
    'StorageArgs',
    'UserAssignedIdentityArgs',
    'UserIdentityArgs',
]

@pulumi.input_type
class AuthConfigArgs:
    def __init__(__self__, *,
                 active_directory_auth: Optional[pulumi.Input[Union[str, 'ActiveDirectoryAuthEnum']]] = None,
                 password_auth: Optional[pulumi.Input[Union[str, 'PasswordAuthEnum']]] = None,
                 tenant_id: Optional[pulumi.Input[str]] = None):
        """
        Authentication configuration properties of a server
        :param pulumi.Input[Union[str, 'ActiveDirectoryAuthEnum']] active_directory_auth: If Enabled, Azure Active Directory authentication is enabled.
        :param pulumi.Input[Union[str, 'PasswordAuthEnum']] password_auth: If Enabled, Password authentication is enabled.
        :param pulumi.Input[str] tenant_id: Tenant id of the server.
        """
        if active_directory_auth is not None:
            pulumi.set(__self__, "active_directory_auth", active_directory_auth)
        if password_auth is None:
            password_auth = 'Enabled'
        if password_auth is not None:
            pulumi.set(__self__, "password_auth", password_auth)
        if tenant_id is None:
            tenant_id = ''
        if tenant_id is not None:
            pulumi.set(__self__, "tenant_id", tenant_id)

    @property
    @pulumi.getter(name="activeDirectoryAuth")
    def active_directory_auth(self) -> Optional[pulumi.Input[Union[str, 'ActiveDirectoryAuthEnum']]]:
        """
        If Enabled, Azure Active Directory authentication is enabled.
        """
        return pulumi.get(self, "active_directory_auth")

    @active_directory_auth.setter
    def active_directory_auth(self, value: Optional[pulumi.Input[Union[str, 'ActiveDirectoryAuthEnum']]]):
        pulumi.set(self, "active_directory_auth", value)

    @property
    @pulumi.getter(name="passwordAuth")
    def password_auth(self) -> Optional[pulumi.Input[Union[str, 'PasswordAuthEnum']]]:
        """
        If Enabled, Password authentication is enabled.
        """
        return pulumi.get(self, "password_auth")

    @password_auth.setter
    def password_auth(self, value: Optional[pulumi.Input[Union[str, 'PasswordAuthEnum']]]):
        pulumi.set(self, "password_auth", value)

    @property
    @pulumi.getter(name="tenantId")
    def tenant_id(self) -> Optional[pulumi.Input[str]]:
        """
        Tenant id of the server.
        """
        return pulumi.get(self, "tenant_id")

    @tenant_id.setter
    def tenant_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "tenant_id", value)


@pulumi.input_type
class BackupArgs:
    def __init__(__self__, *,
                 backup_retention_days: Optional[pulumi.Input[int]] = None,
                 geo_redundant_backup: Optional[pulumi.Input[Union[str, 'GeoRedundantBackupEnum']]] = None):
        """
        Backup properties of a server
        :param pulumi.Input[int] backup_retention_days: Backup retention days for the server.
        :param pulumi.Input[Union[str, 'GeoRedundantBackupEnum']] geo_redundant_backup: A value indicating whether Geo-Redundant backup is enabled on the server.
        """
        if backup_retention_days is None:
            backup_retention_days = 7
        if backup_retention_days is not None:
            pulumi.set(__self__, "backup_retention_days", backup_retention_days)
        if geo_redundant_backup is None:
            geo_redundant_backup = 'Disabled'
        if geo_redundant_backup is not None:
            pulumi.set(__self__, "geo_redundant_backup", geo_redundant_backup)

    @property
    @pulumi.getter(name="backupRetentionDays")
    def backup_retention_days(self) -> Optional[pulumi.Input[int]]:
        """
        Backup retention days for the server.
        """
        return pulumi.get(self, "backup_retention_days")

    @backup_retention_days.setter
    def backup_retention_days(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "backup_retention_days", value)

    @property
    @pulumi.getter(name="geoRedundantBackup")
    def geo_redundant_backup(self) -> Optional[pulumi.Input[Union[str, 'GeoRedundantBackupEnum']]]:
        """
        A value indicating whether Geo-Redundant backup is enabled on the server.
        """
        return pulumi.get(self, "geo_redundant_backup")

    @geo_redundant_backup.setter
    def geo_redundant_backup(self, value: Optional[pulumi.Input[Union[str, 'GeoRedundantBackupEnum']]]):
        pulumi.set(self, "geo_redundant_backup", value)


@pulumi.input_type
class DataEncryptionArgs:
    def __init__(__self__, *,
                 primary_key_uri: Optional[pulumi.Input[str]] = None,
                 primary_user_assigned_identity_id: Optional[pulumi.Input[str]] = None,
                 type: Optional[pulumi.Input[Union[str, 'ArmServerKeyType']]] = None):
        """
        Data encryption properties of a server
        :param pulumi.Input[str] primary_key_uri: URI for the key for data encryption for primary server.
        :param pulumi.Input[str] primary_user_assigned_identity_id: Resource Id for the User assigned identity to be used for data encryption for primary server.
        :param pulumi.Input[Union[str, 'ArmServerKeyType']] type: Data encryption type to depict if it is System assigned vs Azure Key vault.
        """
        if primary_key_uri is not None:
            pulumi.set(__self__, "primary_key_uri", primary_key_uri)
        if primary_user_assigned_identity_id is not None:
            pulumi.set(__self__, "primary_user_assigned_identity_id", primary_user_assigned_identity_id)
        if type is not None:
            pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter(name="primaryKeyURI")
    def primary_key_uri(self) -> Optional[pulumi.Input[str]]:
        """
        URI for the key for data encryption for primary server.
        """
        return pulumi.get(self, "primary_key_uri")

    @primary_key_uri.setter
    def primary_key_uri(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "primary_key_uri", value)

    @property
    @pulumi.getter(name="primaryUserAssignedIdentityId")
    def primary_user_assigned_identity_id(self) -> Optional[pulumi.Input[str]]:
        """
        Resource Id for the User assigned identity to be used for data encryption for primary server.
        """
        return pulumi.get(self, "primary_user_assigned_identity_id")

    @primary_user_assigned_identity_id.setter
    def primary_user_assigned_identity_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "primary_user_assigned_identity_id", value)

    @property
    @pulumi.getter
    def type(self) -> Optional[pulumi.Input[Union[str, 'ArmServerKeyType']]]:
        """
        Data encryption type to depict if it is System assigned vs Azure Key vault.
        """
        return pulumi.get(self, "type")

    @type.setter
    def type(self, value: Optional[pulumi.Input[Union[str, 'ArmServerKeyType']]]):
        pulumi.set(self, "type", value)


@pulumi.input_type
class HighAvailabilityArgs:
    def __init__(__self__, *,
                 mode: Optional[pulumi.Input[Union[str, 'HighAvailabilityMode']]] = None,
                 standby_availability_zone: Optional[pulumi.Input[str]] = None):
        """
        High availability properties of a server
        :param pulumi.Input[Union[str, 'HighAvailabilityMode']] mode: The HA mode for the server.
        :param pulumi.Input[str] standby_availability_zone: availability zone information of the standby.
        """
        if mode is None:
            mode = 'Disabled'
        if mode is not None:
            pulumi.set(__self__, "mode", mode)
        if standby_availability_zone is None:
            standby_availability_zone = ''
        if standby_availability_zone is not None:
            pulumi.set(__self__, "standby_availability_zone", standby_availability_zone)

    @property
    @pulumi.getter
    def mode(self) -> Optional[pulumi.Input[Union[str, 'HighAvailabilityMode']]]:
        """
        The HA mode for the server.
        """
        return pulumi.get(self, "mode")

    @mode.setter
    def mode(self, value: Optional[pulumi.Input[Union[str, 'HighAvailabilityMode']]]):
        pulumi.set(self, "mode", value)

    @property
    @pulumi.getter(name="standbyAvailabilityZone")
    def standby_availability_zone(self) -> Optional[pulumi.Input[str]]:
        """
        availability zone information of the standby.
        """
        return pulumi.get(self, "standby_availability_zone")

    @standby_availability_zone.setter
    def standby_availability_zone(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "standby_availability_zone", value)


@pulumi.input_type
class MaintenanceWindowArgs:
    def __init__(__self__, *,
                 custom_window: Optional[pulumi.Input[str]] = None,
                 day_of_week: Optional[pulumi.Input[int]] = None,
                 start_hour: Optional[pulumi.Input[int]] = None,
                 start_minute: Optional[pulumi.Input[int]] = None):
        """
        Maintenance window properties of a server.
        :param pulumi.Input[str] custom_window: indicates whether custom window is enabled or disabled
        :param pulumi.Input[int] day_of_week: day of week for maintenance window
        :param pulumi.Input[int] start_hour: start hour for maintenance window
        :param pulumi.Input[int] start_minute: start minute for maintenance window
        """
        if custom_window is None:
            custom_window = 'Disabled'
        if custom_window is not None:
            pulumi.set(__self__, "custom_window", custom_window)
        if day_of_week is None:
            day_of_week = 0
        if day_of_week is not None:
            pulumi.set(__self__, "day_of_week", day_of_week)
        if start_hour is None:
            start_hour = 0
        if start_hour is not None:
            pulumi.set(__self__, "start_hour", start_hour)
        if start_minute is None:
            start_minute = 0
        if start_minute is not None:
            pulumi.set(__self__, "start_minute", start_minute)

    @property
    @pulumi.getter(name="customWindow")
    def custom_window(self) -> Optional[pulumi.Input[str]]:
        """
        indicates whether custom window is enabled or disabled
        """
        return pulumi.get(self, "custom_window")

    @custom_window.setter
    def custom_window(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "custom_window", value)

    @property
    @pulumi.getter(name="dayOfWeek")
    def day_of_week(self) -> Optional[pulumi.Input[int]]:
        """
        day of week for maintenance window
        """
        return pulumi.get(self, "day_of_week")

    @day_of_week.setter
    def day_of_week(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "day_of_week", value)

    @property
    @pulumi.getter(name="startHour")
    def start_hour(self) -> Optional[pulumi.Input[int]]:
        """
        start hour for maintenance window
        """
        return pulumi.get(self, "start_hour")

    @start_hour.setter
    def start_hour(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "start_hour", value)

    @property
    @pulumi.getter(name="startMinute")
    def start_minute(self) -> Optional[pulumi.Input[int]]:
        """
        start minute for maintenance window
        """
        return pulumi.get(self, "start_minute")

    @start_minute.setter
    def start_minute(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "start_minute", value)


@pulumi.input_type
class NetworkArgs:
    def __init__(__self__, *,
                 delegated_subnet_resource_id: Optional[pulumi.Input[str]] = None,
                 private_dns_zone_arm_resource_id: Optional[pulumi.Input[str]] = None):
        """
        Network properties of a server
        :param pulumi.Input[str] delegated_subnet_resource_id: delegated subnet arm resource id.
        :param pulumi.Input[str] private_dns_zone_arm_resource_id: private dns zone arm resource id.
        """
        if delegated_subnet_resource_id is None:
            delegated_subnet_resource_id = ''
        if delegated_subnet_resource_id is not None:
            pulumi.set(__self__, "delegated_subnet_resource_id", delegated_subnet_resource_id)
        if private_dns_zone_arm_resource_id is None:
            private_dns_zone_arm_resource_id = ''
        if private_dns_zone_arm_resource_id is not None:
            pulumi.set(__self__, "private_dns_zone_arm_resource_id", private_dns_zone_arm_resource_id)

    @property
    @pulumi.getter(name="delegatedSubnetResourceId")
    def delegated_subnet_resource_id(self) -> Optional[pulumi.Input[str]]:
        """
        delegated subnet arm resource id.
        """
        return pulumi.get(self, "delegated_subnet_resource_id")

    @delegated_subnet_resource_id.setter
    def delegated_subnet_resource_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "delegated_subnet_resource_id", value)

    @property
    @pulumi.getter(name="privateDnsZoneArmResourceId")
    def private_dns_zone_arm_resource_id(self) -> Optional[pulumi.Input[str]]:
        """
        private dns zone arm resource id.
        """
        return pulumi.get(self, "private_dns_zone_arm_resource_id")

    @private_dns_zone_arm_resource_id.setter
    def private_dns_zone_arm_resource_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "private_dns_zone_arm_resource_id", value)


@pulumi.input_type
class SkuArgs:
    def __init__(__self__, *,
                 name: pulumi.Input[str],
                 tier: pulumi.Input[Union[str, 'SkuTier']]):
        """
        Sku information related properties of a server.
        :param pulumi.Input[str] name: The name of the sku, typically, tier + family + cores, e.g. Standard_D4s_v3.
        :param pulumi.Input[Union[str, 'SkuTier']] tier: The tier of the particular SKU, e.g. Burstable.
        """
        pulumi.set(__self__, "name", name)
        pulumi.set(__self__, "tier", tier)

    @property
    @pulumi.getter
    def name(self) -> pulumi.Input[str]:
        """
        The name of the sku, typically, tier + family + cores, e.g. Standard_D4s_v3.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: pulumi.Input[str]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def tier(self) -> pulumi.Input[Union[str, 'SkuTier']]:
        """
        The tier of the particular SKU, e.g. Burstable.
        """
        return pulumi.get(self, "tier")

    @tier.setter
    def tier(self, value: pulumi.Input[Union[str, 'SkuTier']]):
        pulumi.set(self, "tier", value)


@pulumi.input_type
class StorageArgs:
    def __init__(__self__, *,
                 storage_size_gb: Optional[pulumi.Input[int]] = None):
        """
        Storage properties of a server
        :param pulumi.Input[int] storage_size_gb: Max storage allowed for a server.
        """
        if storage_size_gb is not None:
            pulumi.set(__self__, "storage_size_gb", storage_size_gb)

    @property
    @pulumi.getter(name="storageSizeGB")
    def storage_size_gb(self) -> Optional[pulumi.Input[int]]:
        """
        Max storage allowed for a server.
        """
        return pulumi.get(self, "storage_size_gb")

    @storage_size_gb.setter
    def storage_size_gb(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "storage_size_gb", value)


@pulumi.input_type
class UserAssignedIdentityArgs:
    def __init__(__self__, *,
                 type: pulumi.Input[Union[str, 'IdentityType']],
                 user_assigned_identities: Optional[pulumi.Input[Mapping[str, pulumi.Input['UserIdentityArgs']]]] = None):
        """
        Information describing the identities associated with this application.
        :param pulumi.Input[Union[str, 'IdentityType']] type: the types of identities associated with this resource; currently restricted to 'SystemAssigned and UserAssigned'
        :param pulumi.Input[Mapping[str, pulumi.Input['UserIdentityArgs']]] user_assigned_identities: represents user assigned identities map.
        """
        pulumi.set(__self__, "type", type)
        if user_assigned_identities is not None:
            pulumi.set(__self__, "user_assigned_identities", user_assigned_identities)

    @property
    @pulumi.getter
    def type(self) -> pulumi.Input[Union[str, 'IdentityType']]:
        """
        the types of identities associated with this resource; currently restricted to 'SystemAssigned and UserAssigned'
        """
        return pulumi.get(self, "type")

    @type.setter
    def type(self, value: pulumi.Input[Union[str, 'IdentityType']]):
        pulumi.set(self, "type", value)

    @property
    @pulumi.getter(name="userAssignedIdentities")
    def user_assigned_identities(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input['UserIdentityArgs']]]]:
        """
        represents user assigned identities map.
        """
        return pulumi.get(self, "user_assigned_identities")

    @user_assigned_identities.setter
    def user_assigned_identities(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input['UserIdentityArgs']]]]):
        pulumi.set(self, "user_assigned_identities", value)


@pulumi.input_type
class UserIdentityArgs:
    def __init__(__self__, *,
                 client_id: Optional[pulumi.Input[str]] = None,
                 principal_id: Optional[pulumi.Input[str]] = None):
        """
        Describes a single user-assigned identity associated with the application.
        :param pulumi.Input[str] client_id: the client identifier of the Service Principal which this identity represents.
        :param pulumi.Input[str] principal_id: the object identifier of the Service Principal which this identity represents.
        """
        if client_id is not None:
            pulumi.set(__self__, "client_id", client_id)
        if principal_id is not None:
            pulumi.set(__self__, "principal_id", principal_id)

    @property
    @pulumi.getter(name="clientId")
    def client_id(self) -> Optional[pulumi.Input[str]]:
        """
        the client identifier of the Service Principal which this identity represents.
        """
        return pulumi.get(self, "client_id")

    @client_id.setter
    def client_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "client_id", value)

    @property
    @pulumi.getter(name="principalId")
    def principal_id(self) -> Optional[pulumi.Input[str]]:
        """
        the object identifier of the Service Principal which this identity represents.
        """
        return pulumi.get(self, "principal_id")

    @principal_id.setter
    def principal_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "principal_id", value)


