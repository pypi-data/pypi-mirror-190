# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

from enum import Enum

__all__ = [
    'ApplicationType',
    'AvsDataStore',
    'ChownMode',
    'EnableSubvolumes',
    'EncryptionType',
    'EndpointType',
    'NetworkFeatures',
    'QosType',
    'ReplicationSchedule',
    'SecurityStyle',
    'ServiceLevel',
]


class ApplicationType(str, Enum):
    """
    Application Type
    """
    SA_P_HANA = "SAP-HANA"


class AvsDataStore(str, Enum):
    """
    Specifies whether the volume is enabled for Azure VMware Solution (AVS) datastore purpose
    """
    ENABLED = "Enabled"
    """
    avsDataStore is enabled
    """
    DISABLED = "Disabled"
    """
    avsDataStore is disabled
    """


class ChownMode(str, Enum):
    """
    This parameter specifies who is authorized to change the ownership of a file. restricted - Only root user can change the ownership of the file. unrestricted - Non-root users can change ownership of files that they own.
    """
    RESTRICTED = "Restricted"
    UNRESTRICTED = "Unrestricted"


class EnableSubvolumes(str, Enum):
    """
    Flag indicating whether subvolume operations are enabled on the volume
    """
    ENABLED = "Enabled"
    """
    subvolumes are enabled
    """
    DISABLED = "Disabled"
    """
    subvolumes are not enabled
    """


class EncryptionType(str, Enum):
    """
    Encryption type of the capacity pool, set encryption type for data at rest for this pool and all volumes in it. This value can only be set when creating new pool.
    """
    SINGLE = "Single"
    """
    EncryptionType Single, volumes will use single encryption at rest
    """
    DOUBLE = "Double"
    """
    EncryptionType Double, volumes will use double encryption at rest
    """


class EndpointType(str, Enum):
    """
    Indicates whether the local volume is the source or destination for the Volume Replication
    """
    SRC = "src"
    DST = "dst"


class NetworkFeatures(str, Enum):
    """
    Basic network, or Standard features available to the volume.
    """
    BASIC = "Basic"
    """
    Basic network feature.
    """
    STANDARD = "Standard"
    """
    Standard network feature.
    """


class QosType(str, Enum):
    """
    The qos type of the pool
    """
    AUTO = "Auto"
    """
    qos type Auto
    """
    MANUAL = "Manual"
    """
    qos type Manual
    """


class ReplicationSchedule(str, Enum):
    """
    Schedule
    """
    REPLICATION_SCHEDULE_10MINUTELY = "_10minutely"
    HOURLY = "hourly"
    DAILY = "daily"


class SecurityStyle(str, Enum):
    """
    The security style of volume, default unix, defaults to ntfs for dual protocol or CIFS protocol
    """
    NTFS = "ntfs"
    UNIX = "unix"


class ServiceLevel(str, Enum):
    """
    The service level of the file system
    """
    STANDARD = "Standard"
    """
    Standard service level
    """
    PREMIUM = "Premium"
    """
    Premium service level
    """
    ULTRA = "Ultra"
    """
    Ultra service level
    """
    STANDARD_ZRS = "StandardZRS"
    """
    Zone redundant storage service level
    """
