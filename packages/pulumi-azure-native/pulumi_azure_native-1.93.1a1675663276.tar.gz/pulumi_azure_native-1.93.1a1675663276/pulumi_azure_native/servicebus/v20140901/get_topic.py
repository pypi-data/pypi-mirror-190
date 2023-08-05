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
    'GetTopicResult',
    'AwaitableGetTopicResult',
    'get_topic',
    'get_topic_output',
]

warnings.warn("""Version 2014-09-01 will be removed in v2 of the provider.""", DeprecationWarning)

@pulumi.output_type
class GetTopicResult:
    """
    Description of topic resource.
    """
    def __init__(__self__, accessed_at=None, auto_delete_on_idle=None, count_details=None, created_at=None, default_message_time_to_live=None, duplicate_detection_history_time_window=None, enable_batched_operations=None, enable_express=None, enable_partitioning=None, entity_availability_status=None, filtering_messages_before_publishing=None, id=None, is_anonymous_accessible=None, is_express=None, location=None, max_size_in_megabytes=None, name=None, requires_duplicate_detection=None, size_in_bytes=None, status=None, subscription_count=None, support_ordering=None, type=None, updated_at=None):
        if accessed_at and not isinstance(accessed_at, str):
            raise TypeError("Expected argument 'accessed_at' to be a str")
        pulumi.set(__self__, "accessed_at", accessed_at)
        if auto_delete_on_idle and not isinstance(auto_delete_on_idle, str):
            raise TypeError("Expected argument 'auto_delete_on_idle' to be a str")
        pulumi.set(__self__, "auto_delete_on_idle", auto_delete_on_idle)
        if count_details and not isinstance(count_details, dict):
            raise TypeError("Expected argument 'count_details' to be a dict")
        pulumi.set(__self__, "count_details", count_details)
        if created_at and not isinstance(created_at, str):
            raise TypeError("Expected argument 'created_at' to be a str")
        pulumi.set(__self__, "created_at", created_at)
        if default_message_time_to_live and not isinstance(default_message_time_to_live, str):
            raise TypeError("Expected argument 'default_message_time_to_live' to be a str")
        pulumi.set(__self__, "default_message_time_to_live", default_message_time_to_live)
        if duplicate_detection_history_time_window and not isinstance(duplicate_detection_history_time_window, str):
            raise TypeError("Expected argument 'duplicate_detection_history_time_window' to be a str")
        pulumi.set(__self__, "duplicate_detection_history_time_window", duplicate_detection_history_time_window)
        if enable_batched_operations and not isinstance(enable_batched_operations, bool):
            raise TypeError("Expected argument 'enable_batched_operations' to be a bool")
        pulumi.set(__self__, "enable_batched_operations", enable_batched_operations)
        if enable_express and not isinstance(enable_express, bool):
            raise TypeError("Expected argument 'enable_express' to be a bool")
        pulumi.set(__self__, "enable_express", enable_express)
        if enable_partitioning and not isinstance(enable_partitioning, bool):
            raise TypeError("Expected argument 'enable_partitioning' to be a bool")
        pulumi.set(__self__, "enable_partitioning", enable_partitioning)
        if entity_availability_status and not isinstance(entity_availability_status, str):
            raise TypeError("Expected argument 'entity_availability_status' to be a str")
        pulumi.set(__self__, "entity_availability_status", entity_availability_status)
        if filtering_messages_before_publishing and not isinstance(filtering_messages_before_publishing, bool):
            raise TypeError("Expected argument 'filtering_messages_before_publishing' to be a bool")
        pulumi.set(__self__, "filtering_messages_before_publishing", filtering_messages_before_publishing)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if is_anonymous_accessible and not isinstance(is_anonymous_accessible, bool):
            raise TypeError("Expected argument 'is_anonymous_accessible' to be a bool")
        pulumi.set(__self__, "is_anonymous_accessible", is_anonymous_accessible)
        if is_express and not isinstance(is_express, bool):
            raise TypeError("Expected argument 'is_express' to be a bool")
        pulumi.set(__self__, "is_express", is_express)
        if location and not isinstance(location, str):
            raise TypeError("Expected argument 'location' to be a str")
        pulumi.set(__self__, "location", location)
        if max_size_in_megabytes and not isinstance(max_size_in_megabytes, float):
            raise TypeError("Expected argument 'max_size_in_megabytes' to be a float")
        pulumi.set(__self__, "max_size_in_megabytes", max_size_in_megabytes)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if requires_duplicate_detection and not isinstance(requires_duplicate_detection, bool):
            raise TypeError("Expected argument 'requires_duplicate_detection' to be a bool")
        pulumi.set(__self__, "requires_duplicate_detection", requires_duplicate_detection)
        if size_in_bytes and not isinstance(size_in_bytes, float):
            raise TypeError("Expected argument 'size_in_bytes' to be a float")
        pulumi.set(__self__, "size_in_bytes", size_in_bytes)
        if status and not isinstance(status, str):
            raise TypeError("Expected argument 'status' to be a str")
        pulumi.set(__self__, "status", status)
        if subscription_count and not isinstance(subscription_count, int):
            raise TypeError("Expected argument 'subscription_count' to be a int")
        pulumi.set(__self__, "subscription_count", subscription_count)
        if support_ordering and not isinstance(support_ordering, bool):
            raise TypeError("Expected argument 'support_ordering' to be a bool")
        pulumi.set(__self__, "support_ordering", support_ordering)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)
        if updated_at and not isinstance(updated_at, str):
            raise TypeError("Expected argument 'updated_at' to be a str")
        pulumi.set(__self__, "updated_at", updated_at)

    @property
    @pulumi.getter(name="accessedAt")
    def accessed_at(self) -> str:
        """
        Last time the message was sent, or a request was received, for this topic.
        """
        return pulumi.get(self, "accessed_at")

    @property
    @pulumi.getter(name="autoDeleteOnIdle")
    def auto_delete_on_idle(self) -> Optional[str]:
        """
        TimeSpan idle interval after which the topic is automatically deleted. The minimum duration is 5 minutes.
        """
        return pulumi.get(self, "auto_delete_on_idle")

    @property
    @pulumi.getter(name="countDetails")
    def count_details(self) -> 'outputs.MessageCountDetailsResponse':
        """
        Message Count Details.
        """
        return pulumi.get(self, "count_details")

    @property
    @pulumi.getter(name="createdAt")
    def created_at(self) -> str:
        """
        Exact time the message was created.
        """
        return pulumi.get(self, "created_at")

    @property
    @pulumi.getter(name="defaultMessageTimeToLive")
    def default_message_time_to_live(self) -> Optional[str]:
        """
        Default message time to live value. This is the duration after which the message expires, starting from when the message is sent to Service Bus. This is the default value used when TimeToLive is not set on a message itself.
        """
        return pulumi.get(self, "default_message_time_to_live")

    @property
    @pulumi.getter(name="duplicateDetectionHistoryTimeWindow")
    def duplicate_detection_history_time_window(self) -> Optional[str]:
        """
        TimeSpan structure that defines the duration of the duplicate detection history. The default value is 10 minutes.
        """
        return pulumi.get(self, "duplicate_detection_history_time_window")

    @property
    @pulumi.getter(name="enableBatchedOperations")
    def enable_batched_operations(self) -> Optional[bool]:
        """
        Value that indicates whether server-side batched operations are enabled.
        """
        return pulumi.get(self, "enable_batched_operations")

    @property
    @pulumi.getter(name="enableExpress")
    def enable_express(self) -> Optional[bool]:
        """
        Value that indicates whether Express Entities are enabled. An express topic holds a message in memory temporarily before writing it to persistent storage.
        """
        return pulumi.get(self, "enable_express")

    @property
    @pulumi.getter(name="enablePartitioning")
    def enable_partitioning(self) -> Optional[bool]:
        """
        Value that indicates whether the topic to be partitioned across multiple message brokers is enabled.
        """
        return pulumi.get(self, "enable_partitioning")

    @property
    @pulumi.getter(name="entityAvailabilityStatus")
    def entity_availability_status(self) -> Optional[str]:
        """
        Entity availability status for the topic.
        """
        return pulumi.get(self, "entity_availability_status")

    @property
    @pulumi.getter(name="filteringMessagesBeforePublishing")
    def filtering_messages_before_publishing(self) -> Optional[bool]:
        """
        Whether messages should be filtered before publishing.
        """
        return pulumi.get(self, "filtering_messages_before_publishing")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Resource Id
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="isAnonymousAccessible")
    def is_anonymous_accessible(self) -> Optional[bool]:
        """
        Value that indicates whether the message is accessible anonymously.
        """
        return pulumi.get(self, "is_anonymous_accessible")

    @property
    @pulumi.getter(name="isExpress")
    def is_express(self) -> Optional[bool]:
        return pulumi.get(self, "is_express")

    @property
    @pulumi.getter
    def location(self) -> Optional[str]:
        """
        Resource location.
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter(name="maxSizeInMegabytes")
    def max_size_in_megabytes(self) -> Optional[float]:
        """
        Maximum size of the topic in megabytes, which is the size of the memory allocated for the topic.
        """
        return pulumi.get(self, "max_size_in_megabytes")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Resource name
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="requiresDuplicateDetection")
    def requires_duplicate_detection(self) -> Optional[bool]:
        """
        Value indicating if this topic requires duplicate detection.
        """
        return pulumi.get(self, "requires_duplicate_detection")

    @property
    @pulumi.getter(name="sizeInBytes")
    def size_in_bytes(self) -> float:
        """
        Size of the topic, in bytes.
        """
        return pulumi.get(self, "size_in_bytes")

    @property
    @pulumi.getter
    def status(self) -> Optional[str]:
        """
        Enumerates the possible values for the status of a messaging entity.
        """
        return pulumi.get(self, "status")

    @property
    @pulumi.getter(name="subscriptionCount")
    def subscription_count(self) -> int:
        """
        Number of subscriptions.
        """
        return pulumi.get(self, "subscription_count")

    @property
    @pulumi.getter(name="supportOrdering")
    def support_ordering(self) -> Optional[bool]:
        """
        Value that indicates whether the topic supports ordering.
        """
        return pulumi.get(self, "support_ordering")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        Resource type
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter(name="updatedAt")
    def updated_at(self) -> str:
        """
        The exact time the message was updated.
        """
        return pulumi.get(self, "updated_at")


class AwaitableGetTopicResult(GetTopicResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetTopicResult(
            accessed_at=self.accessed_at,
            auto_delete_on_idle=self.auto_delete_on_idle,
            count_details=self.count_details,
            created_at=self.created_at,
            default_message_time_to_live=self.default_message_time_to_live,
            duplicate_detection_history_time_window=self.duplicate_detection_history_time_window,
            enable_batched_operations=self.enable_batched_operations,
            enable_express=self.enable_express,
            enable_partitioning=self.enable_partitioning,
            entity_availability_status=self.entity_availability_status,
            filtering_messages_before_publishing=self.filtering_messages_before_publishing,
            id=self.id,
            is_anonymous_accessible=self.is_anonymous_accessible,
            is_express=self.is_express,
            location=self.location,
            max_size_in_megabytes=self.max_size_in_megabytes,
            name=self.name,
            requires_duplicate_detection=self.requires_duplicate_detection,
            size_in_bytes=self.size_in_bytes,
            status=self.status,
            subscription_count=self.subscription_count,
            support_ordering=self.support_ordering,
            type=self.type,
            updated_at=self.updated_at)


def get_topic(namespace_name: Optional[str] = None,
              resource_group_name: Optional[str] = None,
              topic_name: Optional[str] = None,
              opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetTopicResult:
    """
    Description of topic resource.


    :param str namespace_name: The namespace name
    :param str resource_group_name: Name of the Resource group within the Azure subscription.
    :param str topic_name: The topic name.
    """
    pulumi.log.warn("""get_topic is deprecated: Version 2014-09-01 will be removed in v2 of the provider.""")
    __args__ = dict()
    __args__['namespaceName'] = namespace_name
    __args__['resourceGroupName'] = resource_group_name
    __args__['topicName'] = topic_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:servicebus/v20140901:getTopic', __args__, opts=opts, typ=GetTopicResult).value

    return AwaitableGetTopicResult(
        accessed_at=__ret__.accessed_at,
        auto_delete_on_idle=__ret__.auto_delete_on_idle,
        count_details=__ret__.count_details,
        created_at=__ret__.created_at,
        default_message_time_to_live=__ret__.default_message_time_to_live,
        duplicate_detection_history_time_window=__ret__.duplicate_detection_history_time_window,
        enable_batched_operations=__ret__.enable_batched_operations,
        enable_express=__ret__.enable_express,
        enable_partitioning=__ret__.enable_partitioning,
        entity_availability_status=__ret__.entity_availability_status,
        filtering_messages_before_publishing=__ret__.filtering_messages_before_publishing,
        id=__ret__.id,
        is_anonymous_accessible=__ret__.is_anonymous_accessible,
        is_express=__ret__.is_express,
        location=__ret__.location,
        max_size_in_megabytes=__ret__.max_size_in_megabytes,
        name=__ret__.name,
        requires_duplicate_detection=__ret__.requires_duplicate_detection,
        size_in_bytes=__ret__.size_in_bytes,
        status=__ret__.status,
        subscription_count=__ret__.subscription_count,
        support_ordering=__ret__.support_ordering,
        type=__ret__.type,
        updated_at=__ret__.updated_at)


@_utilities.lift_output_func(get_topic)
def get_topic_output(namespace_name: Optional[pulumi.Input[str]] = None,
                     resource_group_name: Optional[pulumi.Input[str]] = None,
                     topic_name: Optional[pulumi.Input[str]] = None,
                     opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetTopicResult]:
    """
    Description of topic resource.


    :param str namespace_name: The namespace name
    :param str resource_group_name: Name of the Resource group within the Azure subscription.
    :param str topic_name: The topic name.
    """
    pulumi.log.warn("""get_topic is deprecated: Version 2014-09-01 will be removed in v2 of the provider.""")
    ...
