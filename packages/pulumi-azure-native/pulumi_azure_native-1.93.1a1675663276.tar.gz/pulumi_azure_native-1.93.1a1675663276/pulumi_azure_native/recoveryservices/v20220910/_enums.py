# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

from enum import Enum

__all__ = [
    'AgentAutoUpdateStatus',
    'AlertsState',
    'AutomationAccountAuthenticationType',
    'DiskAccountType',
    'ExtendedLocationType',
    'FailoverDeploymentModel',
    'ImmutabilityState',
    'InfrastructureEncryptionState',
    'LicenseType',
    'PossibleOperationsDirections',
    'RecoveryPlanActionLocation',
    'RecoveryPlanGroupType',
    'ReplicationProtectedItemOperation',
    'ResourceIdentityType',
    'SetMultiVmSyncStatus',
    'SkuName',
    'SqlServerLicenseType',
]


class AgentAutoUpdateStatus(str, Enum):
    """
    A value indicating whether the auto update is enabled.
    """
    DISABLED = "Disabled"
    ENABLED = "Enabled"


class AlertsState(str, Enum):
    ENABLED = "Enabled"
    DISABLED = "Disabled"


class AutomationAccountAuthenticationType(str, Enum):
    """
    A value indicating the type authentication to use for automation Account.
    """
    RUN_AS_ACCOUNT = "RunAsAccount"
    SYSTEM_ASSIGNED_IDENTITY = "SystemAssignedIdentity"


class DiskAccountType(str, Enum):
    """
    The disk type.
    """
    STANDARD_LRS = "Standard_LRS"
    PREMIUM_LRS = "Premium_LRS"
    STANDARD_SS_D_LRS = "StandardSSD_LRS"


class ExtendedLocationType(str, Enum):
    """
    The extended location type.
    """
    EDGE_ZONE = "EdgeZone"


class FailoverDeploymentModel(str, Enum):
    """
    The failover deployment model.
    """
    NOT_APPLICABLE = "NotApplicable"
    CLASSIC = "Classic"
    RESOURCE_MANAGER = "ResourceManager"


class ImmutabilityState(str, Enum):
    DISABLED = "Disabled"
    UNLOCKED = "Unlocked"
    LOCKED = "Locked"


class InfrastructureEncryptionState(str, Enum):
    """
    Enabling/Disabling the Double Encryption state
    """
    ENABLED = "Enabled"
    DISABLED = "Disabled"


class LicenseType(str, Enum):
    """
    The license type.
    """
    NOT_SPECIFIED = "NotSpecified"
    NO_LICENSE_TYPE = "NoLicenseType"
    WINDOWS_SERVER = "WindowsServer"


class PossibleOperationsDirections(str, Enum):
    PRIMARY_TO_RECOVERY = "PrimaryToRecovery"
    RECOVERY_TO_PRIMARY = "RecoveryToPrimary"


class RecoveryPlanActionLocation(str, Enum):
    """
    The fabric location.
    """
    PRIMARY = "Primary"
    RECOVERY = "Recovery"


class RecoveryPlanGroupType(str, Enum):
    """
    The group type.
    """
    SHUTDOWN = "Shutdown"
    BOOT = "Boot"
    FAILOVER = "Failover"


class ReplicationProtectedItemOperation(str, Enum):
    REVERSE_REPLICATE = "ReverseReplicate"
    COMMIT = "Commit"
    PLANNED_FAILOVER = "PlannedFailover"
    UNPLANNED_FAILOVER = "UnplannedFailover"
    DISABLE_PROTECTION = "DisableProtection"
    TEST_FAILOVER = "TestFailover"
    TEST_FAILOVER_CLEANUP = "TestFailoverCleanup"
    FAILBACK = "Failback"
    FINALIZE_FAILBACK = "FinalizeFailback"
    CANCEL_FAILOVER = "CancelFailover"
    CHANGE_PIT = "ChangePit"
    REPAIR_REPLICATION = "RepairReplication"
    SWITCH_PROTECTION = "SwitchProtection"
    COMPLETE_MIGRATION = "CompleteMigration"


class ResourceIdentityType(str, Enum):
    """
    The type of managed identity used. The type 'SystemAssigned, UserAssigned' includes both an implicitly created identity and a set of user-assigned identities. The type 'None' will remove any identities.
    """
    SYSTEM_ASSIGNED = "SystemAssigned"
    NONE = "None"
    USER_ASSIGNED = "UserAssigned"
    SYSTEM_ASSIGNED_USER_ASSIGNED = "SystemAssigned, UserAssigned"


class SetMultiVmSyncStatus(str, Enum):
    """
    A value indicating whether multi-VM sync has to be enabled. Value should be 'Enabled' or 'Disabled'.
    """
    ENABLE = "Enable"
    DISABLE = "Disable"


class SkuName(str, Enum):
    """
    Name of SKU is RS0 (Recovery Services 0th version) and the tier is standard tier. They do not have affect on backend storage redundancy or any other vault settings. To manage storage redundancy, use the backupstorageconfig
    """
    STANDARD = "Standard"
    RS0 = "RS0"


class SqlServerLicenseType(str, Enum):
    """
    The SQL Server license type.
    """
    NOT_SPECIFIED = "NotSpecified"
    NO_LICENSE_TYPE = "NoLicenseType"
    PAYG = "PAYG"
    AHUB = "AHUB"
