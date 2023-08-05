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
    'CloudToDevicePropertiesArgs',
    'EventHubPropertiesArgs',
    'FeedbackPropertiesArgs',
    'IotHubPropertiesArgs',
    'IotHubSkuInfoArgs',
    'IpFilterRuleArgs',
    'MessagingEndpointPropertiesArgs',
    'OperationsMonitoringPropertiesArgs',
    'SharedAccessSignatureAuthorizationRuleArgs',
    'StorageEndpointPropertiesArgs',
]

@pulumi.input_type
class CloudToDevicePropertiesArgs:
    def __init__(__self__, *,
                 default_ttl_as_iso8601: Optional[pulumi.Input[str]] = None,
                 feedback: Optional[pulumi.Input['FeedbackPropertiesArgs']] = None,
                 max_delivery_count: Optional[pulumi.Input[int]] = None):
        """
        The IoT hub cloud-to-device messaging properties.
        :param pulumi.Input[str] default_ttl_as_iso8601: The default time to live for cloud-to-device messages in the device queue. See: https://docs.microsoft.com/azure/iot-hub/iot-hub-devguide-messaging#cloud-to-device-messages.
        :param pulumi.Input['FeedbackPropertiesArgs'] feedback: The properties of the feedback queue for cloud-to-device messages.
        :param pulumi.Input[int] max_delivery_count: The max delivery count for cloud-to-device messages in the device queue. See: https://docs.microsoft.com/azure/iot-hub/iot-hub-devguide-messaging#cloud-to-device-messages.
        """
        if default_ttl_as_iso8601 is not None:
            pulumi.set(__self__, "default_ttl_as_iso8601", default_ttl_as_iso8601)
        if feedback is not None:
            pulumi.set(__self__, "feedback", feedback)
        if max_delivery_count is not None:
            pulumi.set(__self__, "max_delivery_count", max_delivery_count)

    @property
    @pulumi.getter(name="defaultTtlAsIso8601")
    def default_ttl_as_iso8601(self) -> Optional[pulumi.Input[str]]:
        """
        The default time to live for cloud-to-device messages in the device queue. See: https://docs.microsoft.com/azure/iot-hub/iot-hub-devguide-messaging#cloud-to-device-messages.
        """
        return pulumi.get(self, "default_ttl_as_iso8601")

    @default_ttl_as_iso8601.setter
    def default_ttl_as_iso8601(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "default_ttl_as_iso8601", value)

    @property
    @pulumi.getter
    def feedback(self) -> Optional[pulumi.Input['FeedbackPropertiesArgs']]:
        """
        The properties of the feedback queue for cloud-to-device messages.
        """
        return pulumi.get(self, "feedback")

    @feedback.setter
    def feedback(self, value: Optional[pulumi.Input['FeedbackPropertiesArgs']]):
        pulumi.set(self, "feedback", value)

    @property
    @pulumi.getter(name="maxDeliveryCount")
    def max_delivery_count(self) -> Optional[pulumi.Input[int]]:
        """
        The max delivery count for cloud-to-device messages in the device queue. See: https://docs.microsoft.com/azure/iot-hub/iot-hub-devguide-messaging#cloud-to-device-messages.
        """
        return pulumi.get(self, "max_delivery_count")

    @max_delivery_count.setter
    def max_delivery_count(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "max_delivery_count", value)


@pulumi.input_type
class EventHubPropertiesArgs:
    def __init__(__self__, *,
                 partition_count: Optional[pulumi.Input[int]] = None,
                 retention_time_in_days: Optional[pulumi.Input[float]] = None):
        """
        The properties of the provisioned Event Hub-compatible endpoint used by the IoT hub.
        :param pulumi.Input[int] partition_count: The number of partitions for receiving device-to-cloud messages in the Event Hub-compatible endpoint. See: https://docs.microsoft.com/azure/iot-hub/iot-hub-devguide-messaging#device-to-cloud-messages.
        :param pulumi.Input[float] retention_time_in_days: The retention time for device-to-cloud messages in days. See: https://docs.microsoft.com/azure/iot-hub/iot-hub-devguide-messaging#device-to-cloud-messages
        """
        if partition_count is not None:
            pulumi.set(__self__, "partition_count", partition_count)
        if retention_time_in_days is not None:
            pulumi.set(__self__, "retention_time_in_days", retention_time_in_days)

    @property
    @pulumi.getter(name="partitionCount")
    def partition_count(self) -> Optional[pulumi.Input[int]]:
        """
        The number of partitions for receiving device-to-cloud messages in the Event Hub-compatible endpoint. See: https://docs.microsoft.com/azure/iot-hub/iot-hub-devguide-messaging#device-to-cloud-messages.
        """
        return pulumi.get(self, "partition_count")

    @partition_count.setter
    def partition_count(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "partition_count", value)

    @property
    @pulumi.getter(name="retentionTimeInDays")
    def retention_time_in_days(self) -> Optional[pulumi.Input[float]]:
        """
        The retention time for device-to-cloud messages in days. See: https://docs.microsoft.com/azure/iot-hub/iot-hub-devguide-messaging#device-to-cloud-messages
        """
        return pulumi.get(self, "retention_time_in_days")

    @retention_time_in_days.setter
    def retention_time_in_days(self, value: Optional[pulumi.Input[float]]):
        pulumi.set(self, "retention_time_in_days", value)


@pulumi.input_type
class FeedbackPropertiesArgs:
    def __init__(__self__, *,
                 lock_duration_as_iso8601: Optional[pulumi.Input[str]] = None,
                 max_delivery_count: Optional[pulumi.Input[int]] = None,
                 ttl_as_iso8601: Optional[pulumi.Input[str]] = None):
        """
        The properties of the feedback queue for cloud-to-device messages.
        :param pulumi.Input[str] lock_duration_as_iso8601: The lock duration for the feedback queue. See: https://docs.microsoft.com/azure/iot-hub/iot-hub-devguide-messaging#cloud-to-device-messages.
        :param pulumi.Input[int] max_delivery_count: The number of times the IoT hub attempts to deliver a message on the feedback queue. See: https://docs.microsoft.com/azure/iot-hub/iot-hub-devguide-messaging#cloud-to-device-messages.
        :param pulumi.Input[str] ttl_as_iso8601: The period of time for which a message is available to consume before it is expired by the IoT hub. See: https://docs.microsoft.com/azure/iot-hub/iot-hub-devguide-messaging#cloud-to-device-messages.
        """
        if lock_duration_as_iso8601 is not None:
            pulumi.set(__self__, "lock_duration_as_iso8601", lock_duration_as_iso8601)
        if max_delivery_count is not None:
            pulumi.set(__self__, "max_delivery_count", max_delivery_count)
        if ttl_as_iso8601 is not None:
            pulumi.set(__self__, "ttl_as_iso8601", ttl_as_iso8601)

    @property
    @pulumi.getter(name="lockDurationAsIso8601")
    def lock_duration_as_iso8601(self) -> Optional[pulumi.Input[str]]:
        """
        The lock duration for the feedback queue. See: https://docs.microsoft.com/azure/iot-hub/iot-hub-devguide-messaging#cloud-to-device-messages.
        """
        return pulumi.get(self, "lock_duration_as_iso8601")

    @lock_duration_as_iso8601.setter
    def lock_duration_as_iso8601(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "lock_duration_as_iso8601", value)

    @property
    @pulumi.getter(name="maxDeliveryCount")
    def max_delivery_count(self) -> Optional[pulumi.Input[int]]:
        """
        The number of times the IoT hub attempts to deliver a message on the feedback queue. See: https://docs.microsoft.com/azure/iot-hub/iot-hub-devguide-messaging#cloud-to-device-messages.
        """
        return pulumi.get(self, "max_delivery_count")

    @max_delivery_count.setter
    def max_delivery_count(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "max_delivery_count", value)

    @property
    @pulumi.getter(name="ttlAsIso8601")
    def ttl_as_iso8601(self) -> Optional[pulumi.Input[str]]:
        """
        The period of time for which a message is available to consume before it is expired by the IoT hub. See: https://docs.microsoft.com/azure/iot-hub/iot-hub-devguide-messaging#cloud-to-device-messages.
        """
        return pulumi.get(self, "ttl_as_iso8601")

    @ttl_as_iso8601.setter
    def ttl_as_iso8601(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "ttl_as_iso8601", value)


@pulumi.input_type
class IotHubPropertiesArgs:
    def __init__(__self__, *,
                 authorization_policies: Optional[pulumi.Input[Sequence[pulumi.Input['SharedAccessSignatureAuthorizationRuleArgs']]]] = None,
                 cloud_to_device: Optional[pulumi.Input['CloudToDevicePropertiesArgs']] = None,
                 comments: Optional[pulumi.Input[str]] = None,
                 enable_file_upload_notifications: Optional[pulumi.Input[bool]] = None,
                 event_hub_endpoints: Optional[pulumi.Input[Mapping[str, pulumi.Input['EventHubPropertiesArgs']]]] = None,
                 features: Optional[pulumi.Input[Union[str, 'Capabilities']]] = None,
                 ip_filter_rules: Optional[pulumi.Input[Sequence[pulumi.Input['IpFilterRuleArgs']]]] = None,
                 messaging_endpoints: Optional[pulumi.Input[Mapping[str, pulumi.Input['MessagingEndpointPropertiesArgs']]]] = None,
                 operations_monitoring_properties: Optional[pulumi.Input['OperationsMonitoringPropertiesArgs']] = None,
                 storage_endpoints: Optional[pulumi.Input[Mapping[str, pulumi.Input['StorageEndpointPropertiesArgs']]]] = None):
        """
        The properties of an IoT hub.
        :param pulumi.Input[Sequence[pulumi.Input['SharedAccessSignatureAuthorizationRuleArgs']]] authorization_policies: The shared access policies you can use to secure a connection to the IoT hub.
        :param pulumi.Input['CloudToDevicePropertiesArgs'] cloud_to_device: The IoT hub cloud-to-device messaging properties.
        :param pulumi.Input[str] comments: Comments.
        :param pulumi.Input[bool] enable_file_upload_notifications: If True, file upload notifications are enabled.
        :param pulumi.Input[Mapping[str, pulumi.Input['EventHubPropertiesArgs']]] event_hub_endpoints: The Event Hub-compatible endpoint properties. The possible keys to this dictionary are events and operationsMonitoringEvents. Both of these keys have to be present in the dictionary while making create or update calls for the IoT hub.
        :param pulumi.Input[Union[str, 'Capabilities']] features: The capabilities and features enabled for the IoT hub.
        :param pulumi.Input[Sequence[pulumi.Input['IpFilterRuleArgs']]] ip_filter_rules: The IP filter rules.
        :param pulumi.Input[Mapping[str, pulumi.Input['MessagingEndpointPropertiesArgs']]] messaging_endpoints: The messaging endpoint properties for the file upload notification queue.
        :param pulumi.Input['OperationsMonitoringPropertiesArgs'] operations_monitoring_properties: The operations monitoring properties for the IoT hub. The possible keys to the dictionary are Connections, DeviceTelemetry, C2DCommands, DeviceIdentityOperations, FileUploadOperations.
        :param pulumi.Input[Mapping[str, pulumi.Input['StorageEndpointPropertiesArgs']]] storage_endpoints: The list of Azure Storage endpoints where you can upload files. Currently you can configure only one Azure Storage account and that MUST have its key as $default. Specifying more than one storage account causes an error to be thrown. Not specifying a value for this property when the enableFileUploadNotifications property is set to True, causes an error to be thrown.
        """
        if authorization_policies is not None:
            pulumi.set(__self__, "authorization_policies", authorization_policies)
        if cloud_to_device is not None:
            pulumi.set(__self__, "cloud_to_device", cloud_to_device)
        if comments is not None:
            pulumi.set(__self__, "comments", comments)
        if enable_file_upload_notifications is not None:
            pulumi.set(__self__, "enable_file_upload_notifications", enable_file_upload_notifications)
        if event_hub_endpoints is not None:
            pulumi.set(__self__, "event_hub_endpoints", event_hub_endpoints)
        if features is not None:
            pulumi.set(__self__, "features", features)
        if ip_filter_rules is not None:
            pulumi.set(__self__, "ip_filter_rules", ip_filter_rules)
        if messaging_endpoints is not None:
            pulumi.set(__self__, "messaging_endpoints", messaging_endpoints)
        if operations_monitoring_properties is not None:
            pulumi.set(__self__, "operations_monitoring_properties", operations_monitoring_properties)
        if storage_endpoints is not None:
            pulumi.set(__self__, "storage_endpoints", storage_endpoints)

    @property
    @pulumi.getter(name="authorizationPolicies")
    def authorization_policies(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['SharedAccessSignatureAuthorizationRuleArgs']]]]:
        """
        The shared access policies you can use to secure a connection to the IoT hub.
        """
        return pulumi.get(self, "authorization_policies")

    @authorization_policies.setter
    def authorization_policies(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['SharedAccessSignatureAuthorizationRuleArgs']]]]):
        pulumi.set(self, "authorization_policies", value)

    @property
    @pulumi.getter(name="cloudToDevice")
    def cloud_to_device(self) -> Optional[pulumi.Input['CloudToDevicePropertiesArgs']]:
        """
        The IoT hub cloud-to-device messaging properties.
        """
        return pulumi.get(self, "cloud_to_device")

    @cloud_to_device.setter
    def cloud_to_device(self, value: Optional[pulumi.Input['CloudToDevicePropertiesArgs']]):
        pulumi.set(self, "cloud_to_device", value)

    @property
    @pulumi.getter
    def comments(self) -> Optional[pulumi.Input[str]]:
        """
        Comments.
        """
        return pulumi.get(self, "comments")

    @comments.setter
    def comments(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "comments", value)

    @property
    @pulumi.getter(name="enableFileUploadNotifications")
    def enable_file_upload_notifications(self) -> Optional[pulumi.Input[bool]]:
        """
        If True, file upload notifications are enabled.
        """
        return pulumi.get(self, "enable_file_upload_notifications")

    @enable_file_upload_notifications.setter
    def enable_file_upload_notifications(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "enable_file_upload_notifications", value)

    @property
    @pulumi.getter(name="eventHubEndpoints")
    def event_hub_endpoints(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input['EventHubPropertiesArgs']]]]:
        """
        The Event Hub-compatible endpoint properties. The possible keys to this dictionary are events and operationsMonitoringEvents. Both of these keys have to be present in the dictionary while making create or update calls for the IoT hub.
        """
        return pulumi.get(self, "event_hub_endpoints")

    @event_hub_endpoints.setter
    def event_hub_endpoints(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input['EventHubPropertiesArgs']]]]):
        pulumi.set(self, "event_hub_endpoints", value)

    @property
    @pulumi.getter
    def features(self) -> Optional[pulumi.Input[Union[str, 'Capabilities']]]:
        """
        The capabilities and features enabled for the IoT hub.
        """
        return pulumi.get(self, "features")

    @features.setter
    def features(self, value: Optional[pulumi.Input[Union[str, 'Capabilities']]]):
        pulumi.set(self, "features", value)

    @property
    @pulumi.getter(name="ipFilterRules")
    def ip_filter_rules(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['IpFilterRuleArgs']]]]:
        """
        The IP filter rules.
        """
        return pulumi.get(self, "ip_filter_rules")

    @ip_filter_rules.setter
    def ip_filter_rules(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['IpFilterRuleArgs']]]]):
        pulumi.set(self, "ip_filter_rules", value)

    @property
    @pulumi.getter(name="messagingEndpoints")
    def messaging_endpoints(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input['MessagingEndpointPropertiesArgs']]]]:
        """
        The messaging endpoint properties for the file upload notification queue.
        """
        return pulumi.get(self, "messaging_endpoints")

    @messaging_endpoints.setter
    def messaging_endpoints(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input['MessagingEndpointPropertiesArgs']]]]):
        pulumi.set(self, "messaging_endpoints", value)

    @property
    @pulumi.getter(name="operationsMonitoringProperties")
    def operations_monitoring_properties(self) -> Optional[pulumi.Input['OperationsMonitoringPropertiesArgs']]:
        """
        The operations monitoring properties for the IoT hub. The possible keys to the dictionary are Connections, DeviceTelemetry, C2DCommands, DeviceIdentityOperations, FileUploadOperations.
        """
        return pulumi.get(self, "operations_monitoring_properties")

    @operations_monitoring_properties.setter
    def operations_monitoring_properties(self, value: Optional[pulumi.Input['OperationsMonitoringPropertiesArgs']]):
        pulumi.set(self, "operations_monitoring_properties", value)

    @property
    @pulumi.getter(name="storageEndpoints")
    def storage_endpoints(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input['StorageEndpointPropertiesArgs']]]]:
        """
        The list of Azure Storage endpoints where you can upload files. Currently you can configure only one Azure Storage account and that MUST have its key as $default. Specifying more than one storage account causes an error to be thrown. Not specifying a value for this property when the enableFileUploadNotifications property is set to True, causes an error to be thrown.
        """
        return pulumi.get(self, "storage_endpoints")

    @storage_endpoints.setter
    def storage_endpoints(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input['StorageEndpointPropertiesArgs']]]]):
        pulumi.set(self, "storage_endpoints", value)


@pulumi.input_type
class IotHubSkuInfoArgs:
    def __init__(__self__, *,
                 capacity: pulumi.Input[float],
                 name: pulumi.Input[Union[str, 'IotHubSku']]):
        """
        Information about the SKU of the IoT hub.
        :param pulumi.Input[float] capacity: The number of provisioned IoT Hub units. See: https://docs.microsoft.com/azure/azure-subscription-service-limits#iot-hub-limits.
        :param pulumi.Input[Union[str, 'IotHubSku']] name: The name of the SKU.
        """
        pulumi.set(__self__, "capacity", capacity)
        pulumi.set(__self__, "name", name)

    @property
    @pulumi.getter
    def capacity(self) -> pulumi.Input[float]:
        """
        The number of provisioned IoT Hub units. See: https://docs.microsoft.com/azure/azure-subscription-service-limits#iot-hub-limits.
        """
        return pulumi.get(self, "capacity")

    @capacity.setter
    def capacity(self, value: pulumi.Input[float]):
        pulumi.set(self, "capacity", value)

    @property
    @pulumi.getter
    def name(self) -> pulumi.Input[Union[str, 'IotHubSku']]:
        """
        The name of the SKU.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: pulumi.Input[Union[str, 'IotHubSku']]):
        pulumi.set(self, "name", value)


@pulumi.input_type
class IpFilterRuleArgs:
    def __init__(__self__, *,
                 action: pulumi.Input['IpFilterActionType'],
                 filter_name: pulumi.Input[str],
                 ip_mask: pulumi.Input[str]):
        """
        The IP filter rules for the IoT hub.
        :param pulumi.Input['IpFilterActionType'] action: The desired action for requests captured by this rule.
        :param pulumi.Input[str] filter_name: The name of the IP filter rule.
        :param pulumi.Input[str] ip_mask: A string that contains the IP address range in CIDR notation for the rule.
        """
        pulumi.set(__self__, "action", action)
        pulumi.set(__self__, "filter_name", filter_name)
        pulumi.set(__self__, "ip_mask", ip_mask)

    @property
    @pulumi.getter
    def action(self) -> pulumi.Input['IpFilterActionType']:
        """
        The desired action for requests captured by this rule.
        """
        return pulumi.get(self, "action")

    @action.setter
    def action(self, value: pulumi.Input['IpFilterActionType']):
        pulumi.set(self, "action", value)

    @property
    @pulumi.getter(name="filterName")
    def filter_name(self) -> pulumi.Input[str]:
        """
        The name of the IP filter rule.
        """
        return pulumi.get(self, "filter_name")

    @filter_name.setter
    def filter_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "filter_name", value)

    @property
    @pulumi.getter(name="ipMask")
    def ip_mask(self) -> pulumi.Input[str]:
        """
        A string that contains the IP address range in CIDR notation for the rule.
        """
        return pulumi.get(self, "ip_mask")

    @ip_mask.setter
    def ip_mask(self, value: pulumi.Input[str]):
        pulumi.set(self, "ip_mask", value)


@pulumi.input_type
class MessagingEndpointPropertiesArgs:
    def __init__(__self__, *,
                 lock_duration_as_iso8601: Optional[pulumi.Input[str]] = None,
                 max_delivery_count: Optional[pulumi.Input[int]] = None,
                 ttl_as_iso8601: Optional[pulumi.Input[str]] = None):
        """
        The properties of the messaging endpoints used by this IoT hub.
        :param pulumi.Input[str] lock_duration_as_iso8601: The lock duration. See: https://docs.microsoft.com/en-us/azure/iot-hub/iot-hub-devguide-file-upload.
        :param pulumi.Input[int] max_delivery_count: The number of times the IoT hub attempts to deliver a message. See: https://docs.microsoft.com/en-us/azure/iot-hub/iot-hub-devguide-file-upload.
        :param pulumi.Input[str] ttl_as_iso8601: The period of time for which a message is available to consume before it is expired by the IoT hub. See: https://docs.microsoft.com/en-us/azure/iot-hub/iot-hub-devguide-file-upload.
        """
        if lock_duration_as_iso8601 is not None:
            pulumi.set(__self__, "lock_duration_as_iso8601", lock_duration_as_iso8601)
        if max_delivery_count is not None:
            pulumi.set(__self__, "max_delivery_count", max_delivery_count)
        if ttl_as_iso8601 is not None:
            pulumi.set(__self__, "ttl_as_iso8601", ttl_as_iso8601)

    @property
    @pulumi.getter(name="lockDurationAsIso8601")
    def lock_duration_as_iso8601(self) -> Optional[pulumi.Input[str]]:
        """
        The lock duration. See: https://docs.microsoft.com/en-us/azure/iot-hub/iot-hub-devguide-file-upload.
        """
        return pulumi.get(self, "lock_duration_as_iso8601")

    @lock_duration_as_iso8601.setter
    def lock_duration_as_iso8601(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "lock_duration_as_iso8601", value)

    @property
    @pulumi.getter(name="maxDeliveryCount")
    def max_delivery_count(self) -> Optional[pulumi.Input[int]]:
        """
        The number of times the IoT hub attempts to deliver a message. See: https://docs.microsoft.com/en-us/azure/iot-hub/iot-hub-devguide-file-upload.
        """
        return pulumi.get(self, "max_delivery_count")

    @max_delivery_count.setter
    def max_delivery_count(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "max_delivery_count", value)

    @property
    @pulumi.getter(name="ttlAsIso8601")
    def ttl_as_iso8601(self) -> Optional[pulumi.Input[str]]:
        """
        The period of time for which a message is available to consume before it is expired by the IoT hub. See: https://docs.microsoft.com/en-us/azure/iot-hub/iot-hub-devguide-file-upload.
        """
        return pulumi.get(self, "ttl_as_iso8601")

    @ttl_as_iso8601.setter
    def ttl_as_iso8601(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "ttl_as_iso8601", value)


@pulumi.input_type
class OperationsMonitoringPropertiesArgs:
    def __init__(__self__, *,
                 events: Optional[pulumi.Input[Mapping[str, pulumi.Input[Union[str, 'OperationMonitoringLevel']]]]] = None):
        """
        The operations monitoring properties for the IoT hub. The possible keys to the dictionary are Connections, DeviceTelemetry, C2DCommands, DeviceIdentityOperations, FileUploadOperations.
        """
        if events is not None:
            pulumi.set(__self__, "events", events)

    @property
    @pulumi.getter
    def events(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[Union[str, 'OperationMonitoringLevel']]]]]:
        return pulumi.get(self, "events")

    @events.setter
    def events(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[Union[str, 'OperationMonitoringLevel']]]]]):
        pulumi.set(self, "events", value)


@pulumi.input_type
class SharedAccessSignatureAuthorizationRuleArgs:
    def __init__(__self__, *,
                 key_name: pulumi.Input[str],
                 rights: pulumi.Input['AccessRights'],
                 primary_key: Optional[pulumi.Input[str]] = None,
                 secondary_key: Optional[pulumi.Input[str]] = None):
        """
        The properties of an IoT hub shared access policy.
        :param pulumi.Input[str] key_name: The name of the shared access policy.
        :param pulumi.Input['AccessRights'] rights: The permissions assigned to the shared access policy.
        :param pulumi.Input[str] primary_key: The primary key.
        :param pulumi.Input[str] secondary_key: The secondary key.
        """
        pulumi.set(__self__, "key_name", key_name)
        pulumi.set(__self__, "rights", rights)
        if primary_key is not None:
            pulumi.set(__self__, "primary_key", primary_key)
        if secondary_key is not None:
            pulumi.set(__self__, "secondary_key", secondary_key)

    @property
    @pulumi.getter(name="keyName")
    def key_name(self) -> pulumi.Input[str]:
        """
        The name of the shared access policy.
        """
        return pulumi.get(self, "key_name")

    @key_name.setter
    def key_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "key_name", value)

    @property
    @pulumi.getter
    def rights(self) -> pulumi.Input['AccessRights']:
        """
        The permissions assigned to the shared access policy.
        """
        return pulumi.get(self, "rights")

    @rights.setter
    def rights(self, value: pulumi.Input['AccessRights']):
        pulumi.set(self, "rights", value)

    @property
    @pulumi.getter(name="primaryKey")
    def primary_key(self) -> Optional[pulumi.Input[str]]:
        """
        The primary key.
        """
        return pulumi.get(self, "primary_key")

    @primary_key.setter
    def primary_key(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "primary_key", value)

    @property
    @pulumi.getter(name="secondaryKey")
    def secondary_key(self) -> Optional[pulumi.Input[str]]:
        """
        The secondary key.
        """
        return pulumi.get(self, "secondary_key")

    @secondary_key.setter
    def secondary_key(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "secondary_key", value)


@pulumi.input_type
class StorageEndpointPropertiesArgs:
    def __init__(__self__, *,
                 connection_string: pulumi.Input[str],
                 container_name: pulumi.Input[str],
                 sas_ttl_as_iso8601: Optional[pulumi.Input[str]] = None):
        """
        The properties of the Azure Storage endpoint for file upload.
        :param pulumi.Input[str] connection_string: The connection string for the Azure Storage account to which files are uploaded.
        :param pulumi.Input[str] container_name: The name of the root container where you upload files. The container need not exist but should be creatable using the connectionString specified.
        :param pulumi.Input[str] sas_ttl_as_iso8601: The period of time for which the SAS URI generated by IoT Hub for file upload is valid. See: https://docs.microsoft.com/azure/iot-hub/iot-hub-devguide-file-upload#file-upload-notification-configuration-options.
        """
        pulumi.set(__self__, "connection_string", connection_string)
        pulumi.set(__self__, "container_name", container_name)
        if sas_ttl_as_iso8601 is not None:
            pulumi.set(__self__, "sas_ttl_as_iso8601", sas_ttl_as_iso8601)

    @property
    @pulumi.getter(name="connectionString")
    def connection_string(self) -> pulumi.Input[str]:
        """
        The connection string for the Azure Storage account to which files are uploaded.
        """
        return pulumi.get(self, "connection_string")

    @connection_string.setter
    def connection_string(self, value: pulumi.Input[str]):
        pulumi.set(self, "connection_string", value)

    @property
    @pulumi.getter(name="containerName")
    def container_name(self) -> pulumi.Input[str]:
        """
        The name of the root container where you upload files. The container need not exist but should be creatable using the connectionString specified.
        """
        return pulumi.get(self, "container_name")

    @container_name.setter
    def container_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "container_name", value)

    @property
    @pulumi.getter(name="sasTtlAsIso8601")
    def sas_ttl_as_iso8601(self) -> Optional[pulumi.Input[str]]:
        """
        The period of time for which the SAS URI generated by IoT Hub for file upload is valid. See: https://docs.microsoft.com/azure/iot-hub/iot-hub-devguide-file-upload#file-upload-notification-configuration-options.
        """
        return pulumi.get(self, "sas_ttl_as_iso8601")

    @sas_ttl_as_iso8601.setter
    def sas_ttl_as_iso8601(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "sas_ttl_as_iso8601", value)


