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
    'AutoShutdownProfileArgs',
    'ConnectionProfileArgs',
    'CredentialsArgs',
    'ImageReferenceArgs',
    'LabNetworkProfileArgs',
    'LabPlanNetworkProfileArgs',
    'RecurrencePatternArgs',
    'RosterProfileArgs',
    'SecurityProfileArgs',
    'SkuArgs',
    'SupportInfoArgs',
    'VirtualMachineAdditionalCapabilitiesArgs',
    'VirtualMachineProfileArgs',
]

@pulumi.input_type
class AutoShutdownProfileArgs:
    def __init__(__self__, *,
                 disconnect_delay: Optional[pulumi.Input[str]] = None,
                 idle_delay: Optional[pulumi.Input[str]] = None,
                 no_connect_delay: Optional[pulumi.Input[str]] = None,
                 shutdown_on_disconnect: Optional[pulumi.Input['EnableState']] = None,
                 shutdown_on_idle: Optional[pulumi.Input['ShutdownOnIdleMode']] = None,
                 shutdown_when_not_connected: Optional[pulumi.Input['EnableState']] = None):
        """
        Profile for how to handle shutting down virtual machines.
        :param pulumi.Input[str] disconnect_delay: The amount of time a VM will stay running after a user disconnects if this behavior is enabled.
        :param pulumi.Input[str] idle_delay: The amount of time a VM will idle before it is shutdown if this behavior is enabled.
        :param pulumi.Input[str] no_connect_delay: The amount of time a VM will stay running before it is shutdown if no connection is made and this behavior is enabled.
        :param pulumi.Input['EnableState'] shutdown_on_disconnect: Whether shutdown on disconnect is enabled
        :param pulumi.Input['ShutdownOnIdleMode'] shutdown_on_idle: Whether a VM will get shutdown when it has idled for a period of time.
        :param pulumi.Input['EnableState'] shutdown_when_not_connected: Whether a VM will get shutdown when it hasn't been connected to after a period of time.
        """
        if disconnect_delay is not None:
            pulumi.set(__self__, "disconnect_delay", disconnect_delay)
        if idle_delay is not None:
            pulumi.set(__self__, "idle_delay", idle_delay)
        if no_connect_delay is not None:
            pulumi.set(__self__, "no_connect_delay", no_connect_delay)
        if shutdown_on_disconnect is None:
            shutdown_on_disconnect = 'Disabled'
        if shutdown_on_disconnect is not None:
            pulumi.set(__self__, "shutdown_on_disconnect", shutdown_on_disconnect)
        if shutdown_on_idle is None:
            shutdown_on_idle = 'None'
        if shutdown_on_idle is not None:
            pulumi.set(__self__, "shutdown_on_idle", shutdown_on_idle)
        if shutdown_when_not_connected is None:
            shutdown_when_not_connected = 'Disabled'
        if shutdown_when_not_connected is not None:
            pulumi.set(__self__, "shutdown_when_not_connected", shutdown_when_not_connected)

    @property
    @pulumi.getter(name="disconnectDelay")
    def disconnect_delay(self) -> Optional[pulumi.Input[str]]:
        """
        The amount of time a VM will stay running after a user disconnects if this behavior is enabled.
        """
        return pulumi.get(self, "disconnect_delay")

    @disconnect_delay.setter
    def disconnect_delay(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "disconnect_delay", value)

    @property
    @pulumi.getter(name="idleDelay")
    def idle_delay(self) -> Optional[pulumi.Input[str]]:
        """
        The amount of time a VM will idle before it is shutdown if this behavior is enabled.
        """
        return pulumi.get(self, "idle_delay")

    @idle_delay.setter
    def idle_delay(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "idle_delay", value)

    @property
    @pulumi.getter(name="noConnectDelay")
    def no_connect_delay(self) -> Optional[pulumi.Input[str]]:
        """
        The amount of time a VM will stay running before it is shutdown if no connection is made and this behavior is enabled.
        """
        return pulumi.get(self, "no_connect_delay")

    @no_connect_delay.setter
    def no_connect_delay(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "no_connect_delay", value)

    @property
    @pulumi.getter(name="shutdownOnDisconnect")
    def shutdown_on_disconnect(self) -> Optional[pulumi.Input['EnableState']]:
        """
        Whether shutdown on disconnect is enabled
        """
        return pulumi.get(self, "shutdown_on_disconnect")

    @shutdown_on_disconnect.setter
    def shutdown_on_disconnect(self, value: Optional[pulumi.Input['EnableState']]):
        pulumi.set(self, "shutdown_on_disconnect", value)

    @property
    @pulumi.getter(name="shutdownOnIdle")
    def shutdown_on_idle(self) -> Optional[pulumi.Input['ShutdownOnIdleMode']]:
        """
        Whether a VM will get shutdown when it has idled for a period of time.
        """
        return pulumi.get(self, "shutdown_on_idle")

    @shutdown_on_idle.setter
    def shutdown_on_idle(self, value: Optional[pulumi.Input['ShutdownOnIdleMode']]):
        pulumi.set(self, "shutdown_on_idle", value)

    @property
    @pulumi.getter(name="shutdownWhenNotConnected")
    def shutdown_when_not_connected(self) -> Optional[pulumi.Input['EnableState']]:
        """
        Whether a VM will get shutdown when it hasn't been connected to after a period of time.
        """
        return pulumi.get(self, "shutdown_when_not_connected")

    @shutdown_when_not_connected.setter
    def shutdown_when_not_connected(self, value: Optional[pulumi.Input['EnableState']]):
        pulumi.set(self, "shutdown_when_not_connected", value)


@pulumi.input_type
class ConnectionProfileArgs:
    def __init__(__self__, *,
                 client_rdp_access: Optional[pulumi.Input['ConnectionType']] = None,
                 client_ssh_access: Optional[pulumi.Input['ConnectionType']] = None,
                 web_rdp_access: Optional[pulumi.Input['ConnectionType']] = None,
                 web_ssh_access: Optional[pulumi.Input['ConnectionType']] = None):
        """
        Connection profile for how users connect to lab virtual machines.
        :param pulumi.Input['ConnectionType'] client_rdp_access: The enabled access level for Client Access over RDP.
        :param pulumi.Input['ConnectionType'] client_ssh_access: The enabled access level for Client Access over SSH.
        :param pulumi.Input['ConnectionType'] web_rdp_access: The enabled access level for Web Access over RDP.
        :param pulumi.Input['ConnectionType'] web_ssh_access: The enabled access level for Web Access over SSH.
        """
        if client_rdp_access is None:
            client_rdp_access = 'None'
        if client_rdp_access is not None:
            pulumi.set(__self__, "client_rdp_access", client_rdp_access)
        if client_ssh_access is None:
            client_ssh_access = 'None'
        if client_ssh_access is not None:
            pulumi.set(__self__, "client_ssh_access", client_ssh_access)
        if web_rdp_access is None:
            web_rdp_access = 'None'
        if web_rdp_access is not None:
            pulumi.set(__self__, "web_rdp_access", web_rdp_access)
        if web_ssh_access is None:
            web_ssh_access = 'None'
        if web_ssh_access is not None:
            pulumi.set(__self__, "web_ssh_access", web_ssh_access)

    @property
    @pulumi.getter(name="clientRdpAccess")
    def client_rdp_access(self) -> Optional[pulumi.Input['ConnectionType']]:
        """
        The enabled access level for Client Access over RDP.
        """
        return pulumi.get(self, "client_rdp_access")

    @client_rdp_access.setter
    def client_rdp_access(self, value: Optional[pulumi.Input['ConnectionType']]):
        pulumi.set(self, "client_rdp_access", value)

    @property
    @pulumi.getter(name="clientSshAccess")
    def client_ssh_access(self) -> Optional[pulumi.Input['ConnectionType']]:
        """
        The enabled access level for Client Access over SSH.
        """
        return pulumi.get(self, "client_ssh_access")

    @client_ssh_access.setter
    def client_ssh_access(self, value: Optional[pulumi.Input['ConnectionType']]):
        pulumi.set(self, "client_ssh_access", value)

    @property
    @pulumi.getter(name="webRdpAccess")
    def web_rdp_access(self) -> Optional[pulumi.Input['ConnectionType']]:
        """
        The enabled access level for Web Access over RDP.
        """
        return pulumi.get(self, "web_rdp_access")

    @web_rdp_access.setter
    def web_rdp_access(self, value: Optional[pulumi.Input['ConnectionType']]):
        pulumi.set(self, "web_rdp_access", value)

    @property
    @pulumi.getter(name="webSshAccess")
    def web_ssh_access(self) -> Optional[pulumi.Input['ConnectionType']]:
        """
        The enabled access level for Web Access over SSH.
        """
        return pulumi.get(self, "web_ssh_access")

    @web_ssh_access.setter
    def web_ssh_access(self, value: Optional[pulumi.Input['ConnectionType']]):
        pulumi.set(self, "web_ssh_access", value)


@pulumi.input_type
class CredentialsArgs:
    def __init__(__self__, *,
                 username: pulumi.Input[str],
                 password: Optional[pulumi.Input[str]] = None):
        """
        Credentials for a user on a lab VM.
        :param pulumi.Input[str] username: The username to use when signing in to lab VMs.
        :param pulumi.Input[str] password: The password for the user. This is required for the TemplateVM createOption.
        """
        pulumi.set(__self__, "username", username)
        if password is not None:
            pulumi.set(__self__, "password", password)

    @property
    @pulumi.getter
    def username(self) -> pulumi.Input[str]:
        """
        The username to use when signing in to lab VMs.
        """
        return pulumi.get(self, "username")

    @username.setter
    def username(self, value: pulumi.Input[str]):
        pulumi.set(self, "username", value)

    @property
    @pulumi.getter
    def password(self) -> Optional[pulumi.Input[str]]:
        """
        The password for the user. This is required for the TemplateVM createOption.
        """
        return pulumi.get(self, "password")

    @password.setter
    def password(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "password", value)


@pulumi.input_type
class ImageReferenceArgs:
    def __init__(__self__, *,
                 id: Optional[pulumi.Input[str]] = None,
                 offer: Optional[pulumi.Input[str]] = None,
                 publisher: Optional[pulumi.Input[str]] = None,
                 sku: Optional[pulumi.Input[str]] = None,
                 version: Optional[pulumi.Input[str]] = None):
        """
        Image reference information. Used in the virtual machine profile.
        :param pulumi.Input[str] id: Image resource ID
        :param pulumi.Input[str] offer: The image offer if applicable.
        :param pulumi.Input[str] publisher: The image publisher
        :param pulumi.Input[str] sku: The image SKU
        :param pulumi.Input[str] version: The image version specified on creation.
        """
        if id is not None:
            pulumi.set(__self__, "id", id)
        if offer is not None:
            pulumi.set(__self__, "offer", offer)
        if publisher is not None:
            pulumi.set(__self__, "publisher", publisher)
        if sku is not None:
            pulumi.set(__self__, "sku", sku)
        if version is not None:
            pulumi.set(__self__, "version", version)

    @property
    @pulumi.getter
    def id(self) -> Optional[pulumi.Input[str]]:
        """
        Image resource ID
        """
        return pulumi.get(self, "id")

    @id.setter
    def id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "id", value)

    @property
    @pulumi.getter
    def offer(self) -> Optional[pulumi.Input[str]]:
        """
        The image offer if applicable.
        """
        return pulumi.get(self, "offer")

    @offer.setter
    def offer(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "offer", value)

    @property
    @pulumi.getter
    def publisher(self) -> Optional[pulumi.Input[str]]:
        """
        The image publisher
        """
        return pulumi.get(self, "publisher")

    @publisher.setter
    def publisher(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "publisher", value)

    @property
    @pulumi.getter
    def sku(self) -> Optional[pulumi.Input[str]]:
        """
        The image SKU
        """
        return pulumi.get(self, "sku")

    @sku.setter
    def sku(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "sku", value)

    @property
    @pulumi.getter
    def version(self) -> Optional[pulumi.Input[str]]:
        """
        The image version specified on creation.
        """
        return pulumi.get(self, "version")

    @version.setter
    def version(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "version", value)


@pulumi.input_type
class LabNetworkProfileArgs:
    def __init__(__self__, *,
                 load_balancer_id: Optional[pulumi.Input[str]] = None,
                 public_ip_id: Optional[pulumi.Input[str]] = None,
                 subnet_id: Optional[pulumi.Input[str]] = None):
        """
        Profile for how to handle networking for Labs.
        :param pulumi.Input[str] load_balancer_id: The external load balancer resource id
        :param pulumi.Input[str] public_ip_id: The external public IP resource id
        :param pulumi.Input[str] subnet_id: The external subnet resource id
        """
        if load_balancer_id is not None:
            pulumi.set(__self__, "load_balancer_id", load_balancer_id)
        if public_ip_id is not None:
            pulumi.set(__self__, "public_ip_id", public_ip_id)
        if subnet_id is not None:
            pulumi.set(__self__, "subnet_id", subnet_id)

    @property
    @pulumi.getter(name="loadBalancerId")
    def load_balancer_id(self) -> Optional[pulumi.Input[str]]:
        """
        The external load balancer resource id
        """
        return pulumi.get(self, "load_balancer_id")

    @load_balancer_id.setter
    def load_balancer_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "load_balancer_id", value)

    @property
    @pulumi.getter(name="publicIpId")
    def public_ip_id(self) -> Optional[pulumi.Input[str]]:
        """
        The external public IP resource id
        """
        return pulumi.get(self, "public_ip_id")

    @public_ip_id.setter
    def public_ip_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "public_ip_id", value)

    @property
    @pulumi.getter(name="subnetId")
    def subnet_id(self) -> Optional[pulumi.Input[str]]:
        """
        The external subnet resource id
        """
        return pulumi.get(self, "subnet_id")

    @subnet_id.setter
    def subnet_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "subnet_id", value)


@pulumi.input_type
class LabPlanNetworkProfileArgs:
    def __init__(__self__, *,
                 subnet_id: Optional[pulumi.Input[str]] = None):
        """
        Profile for how to handle networking for Lab Plans.
        :param pulumi.Input[str] subnet_id: The external subnet resource id
        """
        if subnet_id is not None:
            pulumi.set(__self__, "subnet_id", subnet_id)

    @property
    @pulumi.getter(name="subnetId")
    def subnet_id(self) -> Optional[pulumi.Input[str]]:
        """
        The external subnet resource id
        """
        return pulumi.get(self, "subnet_id")

    @subnet_id.setter
    def subnet_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "subnet_id", value)


@pulumi.input_type
class RecurrencePatternArgs:
    def __init__(__self__, *,
                 expiration_date: pulumi.Input[str],
                 frequency: pulumi.Input['RecurrenceFrequency'],
                 interval: Optional[pulumi.Input[int]] = None,
                 week_days: Optional[pulumi.Input[Sequence[pulumi.Input['WeekDay']]]] = None):
        """
        Recurrence pattern of a lab schedule.
        :param pulumi.Input[str] expiration_date: When the recurrence will expire. This date is inclusive.
        :param pulumi.Input['RecurrenceFrequency'] frequency: The frequency of the recurrence.
        :param pulumi.Input[int] interval: The interval to invoke the schedule on. For example, interval = 2 and RecurrenceFrequency.Daily will run every 2 days. When no interval is supplied, an interval of 1 is used.
        :param pulumi.Input[Sequence[pulumi.Input['WeekDay']]] week_days: The week days the schedule runs. Used for when the Frequency is set to Weekly.
        """
        pulumi.set(__self__, "expiration_date", expiration_date)
        pulumi.set(__self__, "frequency", frequency)
        if interval is not None:
            pulumi.set(__self__, "interval", interval)
        if week_days is not None:
            pulumi.set(__self__, "week_days", week_days)

    @property
    @pulumi.getter(name="expirationDate")
    def expiration_date(self) -> pulumi.Input[str]:
        """
        When the recurrence will expire. This date is inclusive.
        """
        return pulumi.get(self, "expiration_date")

    @expiration_date.setter
    def expiration_date(self, value: pulumi.Input[str]):
        pulumi.set(self, "expiration_date", value)

    @property
    @pulumi.getter
    def frequency(self) -> pulumi.Input['RecurrenceFrequency']:
        """
        The frequency of the recurrence.
        """
        return pulumi.get(self, "frequency")

    @frequency.setter
    def frequency(self, value: pulumi.Input['RecurrenceFrequency']):
        pulumi.set(self, "frequency", value)

    @property
    @pulumi.getter
    def interval(self) -> Optional[pulumi.Input[int]]:
        """
        The interval to invoke the schedule on. For example, interval = 2 and RecurrenceFrequency.Daily will run every 2 days. When no interval is supplied, an interval of 1 is used.
        """
        return pulumi.get(self, "interval")

    @interval.setter
    def interval(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "interval", value)

    @property
    @pulumi.getter(name="weekDays")
    def week_days(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['WeekDay']]]]:
        """
        The week days the schedule runs. Used for when the Frequency is set to Weekly.
        """
        return pulumi.get(self, "week_days")

    @week_days.setter
    def week_days(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['WeekDay']]]]):
        pulumi.set(self, "week_days", value)


@pulumi.input_type
class RosterProfileArgs:
    def __init__(__self__, *,
                 active_directory_group_id: Optional[pulumi.Input[str]] = None,
                 lms_instance: Optional[pulumi.Input[str]] = None,
                 lti_client_id: Optional[pulumi.Input[str]] = None,
                 lti_context_id: Optional[pulumi.Input[str]] = None,
                 lti_roster_endpoint: Optional[pulumi.Input[str]] = None):
        """
        The lab user list management profile.
        :param pulumi.Input[str] active_directory_group_id: The AAD group ID which this lab roster is populated from. Having this set enables AAD sync mode.
        :param pulumi.Input[str] lms_instance: The base URI identifying the lms instance.
        :param pulumi.Input[str] lti_client_id: The unique id of the azure lab services tool in the lms.
        :param pulumi.Input[str] lti_context_id: The unique context identifier for the lab in the lms.
        :param pulumi.Input[str] lti_roster_endpoint: The uri of the names and roles service endpoint on the lms for the class attached to this lab.
        """
        if active_directory_group_id is not None:
            pulumi.set(__self__, "active_directory_group_id", active_directory_group_id)
        if lms_instance is not None:
            pulumi.set(__self__, "lms_instance", lms_instance)
        if lti_client_id is not None:
            pulumi.set(__self__, "lti_client_id", lti_client_id)
        if lti_context_id is not None:
            pulumi.set(__self__, "lti_context_id", lti_context_id)
        if lti_roster_endpoint is not None:
            pulumi.set(__self__, "lti_roster_endpoint", lti_roster_endpoint)

    @property
    @pulumi.getter(name="activeDirectoryGroupId")
    def active_directory_group_id(self) -> Optional[pulumi.Input[str]]:
        """
        The AAD group ID which this lab roster is populated from. Having this set enables AAD sync mode.
        """
        return pulumi.get(self, "active_directory_group_id")

    @active_directory_group_id.setter
    def active_directory_group_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "active_directory_group_id", value)

    @property
    @pulumi.getter(name="lmsInstance")
    def lms_instance(self) -> Optional[pulumi.Input[str]]:
        """
        The base URI identifying the lms instance.
        """
        return pulumi.get(self, "lms_instance")

    @lms_instance.setter
    def lms_instance(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "lms_instance", value)

    @property
    @pulumi.getter(name="ltiClientId")
    def lti_client_id(self) -> Optional[pulumi.Input[str]]:
        """
        The unique id of the azure lab services tool in the lms.
        """
        return pulumi.get(self, "lti_client_id")

    @lti_client_id.setter
    def lti_client_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "lti_client_id", value)

    @property
    @pulumi.getter(name="ltiContextId")
    def lti_context_id(self) -> Optional[pulumi.Input[str]]:
        """
        The unique context identifier for the lab in the lms.
        """
        return pulumi.get(self, "lti_context_id")

    @lti_context_id.setter
    def lti_context_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "lti_context_id", value)

    @property
    @pulumi.getter(name="ltiRosterEndpoint")
    def lti_roster_endpoint(self) -> Optional[pulumi.Input[str]]:
        """
        The uri of the names and roles service endpoint on the lms for the class attached to this lab.
        """
        return pulumi.get(self, "lti_roster_endpoint")

    @lti_roster_endpoint.setter
    def lti_roster_endpoint(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "lti_roster_endpoint", value)


@pulumi.input_type
class SecurityProfileArgs:
    def __init__(__self__, *,
                 open_access: Optional[pulumi.Input['EnableState']] = None):
        """
        The lab security profile.
        :param pulumi.Input['EnableState'] open_access: Whether any user or only specified users can register to a lab.
        """
        if open_access is not None:
            pulumi.set(__self__, "open_access", open_access)

    @property
    @pulumi.getter(name="openAccess")
    def open_access(self) -> Optional[pulumi.Input['EnableState']]:
        """
        Whether any user or only specified users can register to a lab.
        """
        return pulumi.get(self, "open_access")

    @open_access.setter
    def open_access(self, value: Optional[pulumi.Input['EnableState']]):
        pulumi.set(self, "open_access", value)


@pulumi.input_type
class SkuArgs:
    def __init__(__self__, *,
                 name: pulumi.Input[str],
                 capacity: Optional[pulumi.Input[int]] = None,
                 family: Optional[pulumi.Input[str]] = None,
                 size: Optional[pulumi.Input[str]] = None,
                 tier: Optional[pulumi.Input['SkuTier']] = None):
        """
        The resource model definition representing SKU
        :param pulumi.Input[str] name: The name of the SKU. Ex - P3. It is typically a letter+number code
        :param pulumi.Input[int] capacity: If the SKU supports scale out/in then the capacity integer should be included. If scale out/in is not possible for the resource this may be omitted.
        :param pulumi.Input[str] family: If the service has different generations of hardware, for the same SKU, then that can be captured here.
        :param pulumi.Input[str] size: The SKU size. When the name field is the combination of tier and some other value, this would be the standalone code. 
        :param pulumi.Input['SkuTier'] tier: This field is required to be implemented by the Resource Provider if the service has more than one tier, but is not required on a PUT.
        """
        pulumi.set(__self__, "name", name)
        if capacity is not None:
            pulumi.set(__self__, "capacity", capacity)
        if family is not None:
            pulumi.set(__self__, "family", family)
        if size is not None:
            pulumi.set(__self__, "size", size)
        if tier is not None:
            pulumi.set(__self__, "tier", tier)

    @property
    @pulumi.getter
    def name(self) -> pulumi.Input[str]:
        """
        The name of the SKU. Ex - P3. It is typically a letter+number code
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: pulumi.Input[str]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def capacity(self) -> Optional[pulumi.Input[int]]:
        """
        If the SKU supports scale out/in then the capacity integer should be included. If scale out/in is not possible for the resource this may be omitted.
        """
        return pulumi.get(self, "capacity")

    @capacity.setter
    def capacity(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "capacity", value)

    @property
    @pulumi.getter
    def family(self) -> Optional[pulumi.Input[str]]:
        """
        If the service has different generations of hardware, for the same SKU, then that can be captured here.
        """
        return pulumi.get(self, "family")

    @family.setter
    def family(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "family", value)

    @property
    @pulumi.getter
    def size(self) -> Optional[pulumi.Input[str]]:
        """
        The SKU size. When the name field is the combination of tier and some other value, this would be the standalone code. 
        """
        return pulumi.get(self, "size")

    @size.setter
    def size(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "size", value)

    @property
    @pulumi.getter
    def tier(self) -> Optional[pulumi.Input['SkuTier']]:
        """
        This field is required to be implemented by the Resource Provider if the service has more than one tier, but is not required on a PUT.
        """
        return pulumi.get(self, "tier")

    @tier.setter
    def tier(self, value: Optional[pulumi.Input['SkuTier']]):
        pulumi.set(self, "tier", value)


@pulumi.input_type
class SupportInfoArgs:
    def __init__(__self__, *,
                 email: Optional[pulumi.Input[str]] = None,
                 instructions: Optional[pulumi.Input[str]] = None,
                 phone: Optional[pulumi.Input[str]] = None,
                 url: Optional[pulumi.Input[str]] = None):
        """
        Support contact information and instructions.
        :param pulumi.Input[str] email: Support contact email address.
        :param pulumi.Input[str] instructions: Support instructions.
        :param pulumi.Input[str] phone: Support contact phone number.
        :param pulumi.Input[str] url: Support web address.
        """
        if email is not None:
            pulumi.set(__self__, "email", email)
        if instructions is not None:
            pulumi.set(__self__, "instructions", instructions)
        if phone is not None:
            pulumi.set(__self__, "phone", phone)
        if url is not None:
            pulumi.set(__self__, "url", url)

    @property
    @pulumi.getter
    def email(self) -> Optional[pulumi.Input[str]]:
        """
        Support contact email address.
        """
        return pulumi.get(self, "email")

    @email.setter
    def email(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "email", value)

    @property
    @pulumi.getter
    def instructions(self) -> Optional[pulumi.Input[str]]:
        """
        Support instructions.
        """
        return pulumi.get(self, "instructions")

    @instructions.setter
    def instructions(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "instructions", value)

    @property
    @pulumi.getter
    def phone(self) -> Optional[pulumi.Input[str]]:
        """
        Support contact phone number.
        """
        return pulumi.get(self, "phone")

    @phone.setter
    def phone(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "phone", value)

    @property
    @pulumi.getter
    def url(self) -> Optional[pulumi.Input[str]]:
        """
        Support web address.
        """
        return pulumi.get(self, "url")

    @url.setter
    def url(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "url", value)


@pulumi.input_type
class VirtualMachineAdditionalCapabilitiesArgs:
    def __init__(__self__, *,
                 install_gpu_drivers: Optional[pulumi.Input['EnableState']] = None):
        """
        The additional capabilities for a lab VM.
        :param pulumi.Input['EnableState'] install_gpu_drivers: Flag to pre-install dedicated GPU drivers.
        """
        if install_gpu_drivers is None:
            install_gpu_drivers = 'Disabled'
        if install_gpu_drivers is not None:
            pulumi.set(__self__, "install_gpu_drivers", install_gpu_drivers)

    @property
    @pulumi.getter(name="installGpuDrivers")
    def install_gpu_drivers(self) -> Optional[pulumi.Input['EnableState']]:
        """
        Flag to pre-install dedicated GPU drivers.
        """
        return pulumi.get(self, "install_gpu_drivers")

    @install_gpu_drivers.setter
    def install_gpu_drivers(self, value: Optional[pulumi.Input['EnableState']]):
        pulumi.set(self, "install_gpu_drivers", value)


@pulumi.input_type
class VirtualMachineProfileArgs:
    def __init__(__self__, *,
                 admin_user: pulumi.Input['CredentialsArgs'],
                 create_option: pulumi.Input['CreateOption'],
                 image_reference: pulumi.Input['ImageReferenceArgs'],
                 sku: pulumi.Input['SkuArgs'],
                 usage_quota: pulumi.Input[str],
                 additional_capabilities: Optional[pulumi.Input['VirtualMachineAdditionalCapabilitiesArgs']] = None,
                 non_admin_user: Optional[pulumi.Input['CredentialsArgs']] = None,
                 use_shared_password: Optional[pulumi.Input['EnableState']] = None):
        """
        The base virtual machine configuration for a lab.
        :param pulumi.Input['CredentialsArgs'] admin_user: Credentials for the admin user on the VM.
        :param pulumi.Input['CreateOption'] create_option: Indicates what lab virtual machines are created from.
        :param pulumi.Input['ImageReferenceArgs'] image_reference: The image configuration for lab virtual machines.
        :param pulumi.Input['SkuArgs'] sku: The SKU for the lab. Defines the type of virtual machines used in the lab.
        :param pulumi.Input[str] usage_quota: The initial quota alloted to each lab user. Must be a time span between 0 and 9999 hours.
        :param pulumi.Input['VirtualMachineAdditionalCapabilitiesArgs'] additional_capabilities: Additional VM capabilities.
        :param pulumi.Input['CredentialsArgs'] non_admin_user: Credentials for the non-admin user on the VM, if one exists.
        :param pulumi.Input['EnableState'] use_shared_password: Enabling this option will use the same password for all user VMs.
        """
        pulumi.set(__self__, "admin_user", admin_user)
        pulumi.set(__self__, "create_option", create_option)
        pulumi.set(__self__, "image_reference", image_reference)
        pulumi.set(__self__, "sku", sku)
        pulumi.set(__self__, "usage_quota", usage_quota)
        if additional_capabilities is not None:
            pulumi.set(__self__, "additional_capabilities", additional_capabilities)
        if non_admin_user is not None:
            pulumi.set(__self__, "non_admin_user", non_admin_user)
        if use_shared_password is None:
            use_shared_password = 'Disabled'
        if use_shared_password is not None:
            pulumi.set(__self__, "use_shared_password", use_shared_password)

    @property
    @pulumi.getter(name="adminUser")
    def admin_user(self) -> pulumi.Input['CredentialsArgs']:
        """
        Credentials for the admin user on the VM.
        """
        return pulumi.get(self, "admin_user")

    @admin_user.setter
    def admin_user(self, value: pulumi.Input['CredentialsArgs']):
        pulumi.set(self, "admin_user", value)

    @property
    @pulumi.getter(name="createOption")
    def create_option(self) -> pulumi.Input['CreateOption']:
        """
        Indicates what lab virtual machines are created from.
        """
        return pulumi.get(self, "create_option")

    @create_option.setter
    def create_option(self, value: pulumi.Input['CreateOption']):
        pulumi.set(self, "create_option", value)

    @property
    @pulumi.getter(name="imageReference")
    def image_reference(self) -> pulumi.Input['ImageReferenceArgs']:
        """
        The image configuration for lab virtual machines.
        """
        return pulumi.get(self, "image_reference")

    @image_reference.setter
    def image_reference(self, value: pulumi.Input['ImageReferenceArgs']):
        pulumi.set(self, "image_reference", value)

    @property
    @pulumi.getter
    def sku(self) -> pulumi.Input['SkuArgs']:
        """
        The SKU for the lab. Defines the type of virtual machines used in the lab.
        """
        return pulumi.get(self, "sku")

    @sku.setter
    def sku(self, value: pulumi.Input['SkuArgs']):
        pulumi.set(self, "sku", value)

    @property
    @pulumi.getter(name="usageQuota")
    def usage_quota(self) -> pulumi.Input[str]:
        """
        The initial quota alloted to each lab user. Must be a time span between 0 and 9999 hours.
        """
        return pulumi.get(self, "usage_quota")

    @usage_quota.setter
    def usage_quota(self, value: pulumi.Input[str]):
        pulumi.set(self, "usage_quota", value)

    @property
    @pulumi.getter(name="additionalCapabilities")
    def additional_capabilities(self) -> Optional[pulumi.Input['VirtualMachineAdditionalCapabilitiesArgs']]:
        """
        Additional VM capabilities.
        """
        return pulumi.get(self, "additional_capabilities")

    @additional_capabilities.setter
    def additional_capabilities(self, value: Optional[pulumi.Input['VirtualMachineAdditionalCapabilitiesArgs']]):
        pulumi.set(self, "additional_capabilities", value)

    @property
    @pulumi.getter(name="nonAdminUser")
    def non_admin_user(self) -> Optional[pulumi.Input['CredentialsArgs']]:
        """
        Credentials for the non-admin user on the VM, if one exists.
        """
        return pulumi.get(self, "non_admin_user")

    @non_admin_user.setter
    def non_admin_user(self, value: Optional[pulumi.Input['CredentialsArgs']]):
        pulumi.set(self, "non_admin_user", value)

    @property
    @pulumi.getter(name="useSharedPassword")
    def use_shared_password(self) -> Optional[pulumi.Input['EnableState']]:
        """
        Enabling this option will use the same password for all user VMs.
        """
        return pulumi.get(self, "use_shared_password")

    @use_shared_password.setter
    def use_shared_password(self, value: Optional[pulumi.Input['EnableState']]):
        pulumi.set(self, "use_shared_password", value)


