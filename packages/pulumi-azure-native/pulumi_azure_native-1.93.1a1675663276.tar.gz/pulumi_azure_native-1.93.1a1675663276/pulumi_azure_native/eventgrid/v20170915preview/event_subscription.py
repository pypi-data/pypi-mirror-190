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
from ._inputs import *

__all__ = ['EventSubscriptionArgs', 'EventSubscription']

@pulumi.input_type
class EventSubscriptionArgs:
    def __init__(__self__, *,
                 scope: pulumi.Input[str],
                 destination: Optional[pulumi.Input[Union['EventHubEventSubscriptionDestinationArgs', 'WebHookEventSubscriptionDestinationArgs']]] = None,
                 event_subscription_name: Optional[pulumi.Input[str]] = None,
                 filter: Optional[pulumi.Input['EventSubscriptionFilterArgs']] = None,
                 labels: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None):
        """
        The set of arguments for constructing a EventSubscription resource.
        :param pulumi.Input[str] scope: The scope of the resource to which the event subscription needs to be created. The scope can be a subscription, or a resource group, or a top level resource belonging to a resource provider namespace, or an EventGrid topic. For example, use '/subscriptions/{subscriptionId}/' for a subscription, '/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}' for a resource group, and '/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/{resourceProviderNamespace}/{resourceType}/{resourceName}' for a resource, and '/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.EventGrid/topics/{topicName}' for an EventGrid topic.
        :param pulumi.Input[Union['EventHubEventSubscriptionDestinationArgs', 'WebHookEventSubscriptionDestinationArgs']] destination: Information about the destination where events have to be delivered for the event subscription.
        :param pulumi.Input[str] event_subscription_name: Name of the event subscription to be created. Event subscription names must be between 3 and 64 characters in length and use alphanumeric letters only.
        :param pulumi.Input['EventSubscriptionFilterArgs'] filter: Information about the filter for the event subscription.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] labels: List of user defined labels.
        """
        pulumi.set(__self__, "scope", scope)
        if destination is not None:
            pulumi.set(__self__, "destination", destination)
        if event_subscription_name is not None:
            pulumi.set(__self__, "event_subscription_name", event_subscription_name)
        if filter is not None:
            pulumi.set(__self__, "filter", filter)
        if labels is not None:
            pulumi.set(__self__, "labels", labels)

    @property
    @pulumi.getter
    def scope(self) -> pulumi.Input[str]:
        """
        The scope of the resource to which the event subscription needs to be created. The scope can be a subscription, or a resource group, or a top level resource belonging to a resource provider namespace, or an EventGrid topic. For example, use '/subscriptions/{subscriptionId}/' for a subscription, '/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}' for a resource group, and '/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/{resourceProviderNamespace}/{resourceType}/{resourceName}' for a resource, and '/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.EventGrid/topics/{topicName}' for an EventGrid topic.
        """
        return pulumi.get(self, "scope")

    @scope.setter
    def scope(self, value: pulumi.Input[str]):
        pulumi.set(self, "scope", value)

    @property
    @pulumi.getter
    def destination(self) -> Optional[pulumi.Input[Union['EventHubEventSubscriptionDestinationArgs', 'WebHookEventSubscriptionDestinationArgs']]]:
        """
        Information about the destination where events have to be delivered for the event subscription.
        """
        return pulumi.get(self, "destination")

    @destination.setter
    def destination(self, value: Optional[pulumi.Input[Union['EventHubEventSubscriptionDestinationArgs', 'WebHookEventSubscriptionDestinationArgs']]]):
        pulumi.set(self, "destination", value)

    @property
    @pulumi.getter(name="eventSubscriptionName")
    def event_subscription_name(self) -> Optional[pulumi.Input[str]]:
        """
        Name of the event subscription to be created. Event subscription names must be between 3 and 64 characters in length and use alphanumeric letters only.
        """
        return pulumi.get(self, "event_subscription_name")

    @event_subscription_name.setter
    def event_subscription_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "event_subscription_name", value)

    @property
    @pulumi.getter
    def filter(self) -> Optional[pulumi.Input['EventSubscriptionFilterArgs']]:
        """
        Information about the filter for the event subscription.
        """
        return pulumi.get(self, "filter")

    @filter.setter
    def filter(self, value: Optional[pulumi.Input['EventSubscriptionFilterArgs']]):
        pulumi.set(self, "filter", value)

    @property
    @pulumi.getter
    def labels(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        List of user defined labels.
        """
        return pulumi.get(self, "labels")

    @labels.setter
    def labels(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "labels", value)


warnings.warn("""Version 2017-09-15-preview will be removed in v2 of the provider.""", DeprecationWarning)


class EventSubscription(pulumi.CustomResource):
    warnings.warn("""Version 2017-09-15-preview will be removed in v2 of the provider.""", DeprecationWarning)

    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 destination: Optional[pulumi.Input[Union[pulumi.InputType['EventHubEventSubscriptionDestinationArgs'], pulumi.InputType['WebHookEventSubscriptionDestinationArgs']]]] = None,
                 event_subscription_name: Optional[pulumi.Input[str]] = None,
                 filter: Optional[pulumi.Input[pulumi.InputType['EventSubscriptionFilterArgs']]] = None,
                 labels: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 scope: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Event Subscription

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Union[pulumi.InputType['EventHubEventSubscriptionDestinationArgs'], pulumi.InputType['WebHookEventSubscriptionDestinationArgs']]] destination: Information about the destination where events have to be delivered for the event subscription.
        :param pulumi.Input[str] event_subscription_name: Name of the event subscription to be created. Event subscription names must be between 3 and 64 characters in length and use alphanumeric letters only.
        :param pulumi.Input[pulumi.InputType['EventSubscriptionFilterArgs']] filter: Information about the filter for the event subscription.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] labels: List of user defined labels.
        :param pulumi.Input[str] scope: The scope of the resource to which the event subscription needs to be created. The scope can be a subscription, or a resource group, or a top level resource belonging to a resource provider namespace, or an EventGrid topic. For example, use '/subscriptions/{subscriptionId}/' for a subscription, '/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}' for a resource group, and '/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/{resourceProviderNamespace}/{resourceType}/{resourceName}' for a resource, and '/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.EventGrid/topics/{topicName}' for an EventGrid topic.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: EventSubscriptionArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Event Subscription

        :param str resource_name: The name of the resource.
        :param EventSubscriptionArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(EventSubscriptionArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 destination: Optional[pulumi.Input[Union[pulumi.InputType['EventHubEventSubscriptionDestinationArgs'], pulumi.InputType['WebHookEventSubscriptionDestinationArgs']]]] = None,
                 event_subscription_name: Optional[pulumi.Input[str]] = None,
                 filter: Optional[pulumi.Input[pulumi.InputType['EventSubscriptionFilterArgs']]] = None,
                 labels: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 scope: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        pulumi.log.warn("""EventSubscription is deprecated: Version 2017-09-15-preview will be removed in v2 of the provider.""")
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = EventSubscriptionArgs.__new__(EventSubscriptionArgs)

            __props__.__dict__["destination"] = destination
            __props__.__dict__["event_subscription_name"] = event_subscription_name
            __props__.__dict__["filter"] = filter
            __props__.__dict__["labels"] = labels
            if scope is None and not opts.urn:
                raise TypeError("Missing required property 'scope'")
            __props__.__dict__["scope"] = scope
            __props__.__dict__["name"] = None
            __props__.__dict__["provisioning_state"] = None
            __props__.__dict__["topic"] = None
            __props__.__dict__["type"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-native:eventgrid:EventSubscription"), pulumi.Alias(type_="azure-native:eventgrid/v20170615preview:EventSubscription"), pulumi.Alias(type_="azure-native:eventgrid/v20180101:EventSubscription"), pulumi.Alias(type_="azure-native:eventgrid/v20180501preview:EventSubscription"), pulumi.Alias(type_="azure-native:eventgrid/v20180915preview:EventSubscription"), pulumi.Alias(type_="azure-native:eventgrid/v20190101:EventSubscription"), pulumi.Alias(type_="azure-native:eventgrid/v20190201preview:EventSubscription"), pulumi.Alias(type_="azure-native:eventgrid/v20190601:EventSubscription"), pulumi.Alias(type_="azure-native:eventgrid/v20200101preview:EventSubscription"), pulumi.Alias(type_="azure-native:eventgrid/v20200401preview:EventSubscription"), pulumi.Alias(type_="azure-native:eventgrid/v20200601:EventSubscription"), pulumi.Alias(type_="azure-native:eventgrid/v20201015preview:EventSubscription"), pulumi.Alias(type_="azure-native:eventgrid/v20210601preview:EventSubscription"), pulumi.Alias(type_="azure-native:eventgrid/v20211015preview:EventSubscription"), pulumi.Alias(type_="azure-native:eventgrid/v20211201:EventSubscription"), pulumi.Alias(type_="azure-native:eventgrid/v20220615:EventSubscription")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(EventSubscription, __self__).__init__(
            'azure-native:eventgrid/v20170915preview:EventSubscription',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'EventSubscription':
        """
        Get an existing EventSubscription resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = EventSubscriptionArgs.__new__(EventSubscriptionArgs)

        __props__.__dict__["destination"] = None
        __props__.__dict__["filter"] = None
        __props__.__dict__["labels"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["provisioning_state"] = None
        __props__.__dict__["topic"] = None
        __props__.__dict__["type"] = None
        return EventSubscription(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def destination(self) -> pulumi.Output[Optional[Any]]:
        """
        Information about the destination where events have to be delivered for the event subscription.
        """
        return pulumi.get(self, "destination")

    @property
    @pulumi.getter
    def filter(self) -> pulumi.Output[Optional['outputs.EventSubscriptionFilterResponse']]:
        """
        Information about the filter for the event subscription.
        """
        return pulumi.get(self, "filter")

    @property
    @pulumi.getter
    def labels(self) -> pulumi.Output[Optional[Sequence[str]]]:
        """
        List of user defined labels.
        """
        return pulumi.get(self, "labels")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Name of the resource
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> pulumi.Output[str]:
        """
        Provisioning state of the event subscription.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter
    def topic(self) -> pulumi.Output[str]:
        """
        Name of the topic of the event subscription.
        """
        return pulumi.get(self, "topic")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        Type of the resource
        """
        return pulumi.get(self, "type")

