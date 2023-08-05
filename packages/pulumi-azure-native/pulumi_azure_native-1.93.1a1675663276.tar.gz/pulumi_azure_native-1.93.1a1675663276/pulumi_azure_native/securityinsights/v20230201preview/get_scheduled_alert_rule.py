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
    'GetScheduledAlertRuleResult',
    'AwaitableGetScheduledAlertRuleResult',
    'get_scheduled_alert_rule',
    'get_scheduled_alert_rule_output',
]

@pulumi.output_type
class GetScheduledAlertRuleResult:
    """
    Represents scheduled alert rule.
    """
    def __init__(__self__, alert_details_override=None, alert_rule_template_name=None, custom_details=None, description=None, display_name=None, enabled=None, entity_mappings=None, etag=None, event_grouping_settings=None, id=None, incident_configuration=None, kind=None, last_modified_utc=None, name=None, query=None, query_frequency=None, query_period=None, sentinel_entities_mappings=None, severity=None, suppression_duration=None, suppression_enabled=None, system_data=None, tactics=None, techniques=None, template_version=None, trigger_operator=None, trigger_threshold=None, type=None):
        if alert_details_override and not isinstance(alert_details_override, dict):
            raise TypeError("Expected argument 'alert_details_override' to be a dict")
        pulumi.set(__self__, "alert_details_override", alert_details_override)
        if alert_rule_template_name and not isinstance(alert_rule_template_name, str):
            raise TypeError("Expected argument 'alert_rule_template_name' to be a str")
        pulumi.set(__self__, "alert_rule_template_name", alert_rule_template_name)
        if custom_details and not isinstance(custom_details, dict):
            raise TypeError("Expected argument 'custom_details' to be a dict")
        pulumi.set(__self__, "custom_details", custom_details)
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, "description", description)
        if display_name and not isinstance(display_name, str):
            raise TypeError("Expected argument 'display_name' to be a str")
        pulumi.set(__self__, "display_name", display_name)
        if enabled and not isinstance(enabled, bool):
            raise TypeError("Expected argument 'enabled' to be a bool")
        pulumi.set(__self__, "enabled", enabled)
        if entity_mappings and not isinstance(entity_mappings, list):
            raise TypeError("Expected argument 'entity_mappings' to be a list")
        pulumi.set(__self__, "entity_mappings", entity_mappings)
        if etag and not isinstance(etag, str):
            raise TypeError("Expected argument 'etag' to be a str")
        pulumi.set(__self__, "etag", etag)
        if event_grouping_settings and not isinstance(event_grouping_settings, dict):
            raise TypeError("Expected argument 'event_grouping_settings' to be a dict")
        pulumi.set(__self__, "event_grouping_settings", event_grouping_settings)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if incident_configuration and not isinstance(incident_configuration, dict):
            raise TypeError("Expected argument 'incident_configuration' to be a dict")
        pulumi.set(__self__, "incident_configuration", incident_configuration)
        if kind and not isinstance(kind, str):
            raise TypeError("Expected argument 'kind' to be a str")
        pulumi.set(__self__, "kind", kind)
        if last_modified_utc and not isinstance(last_modified_utc, str):
            raise TypeError("Expected argument 'last_modified_utc' to be a str")
        pulumi.set(__self__, "last_modified_utc", last_modified_utc)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if query and not isinstance(query, str):
            raise TypeError("Expected argument 'query' to be a str")
        pulumi.set(__self__, "query", query)
        if query_frequency and not isinstance(query_frequency, str):
            raise TypeError("Expected argument 'query_frequency' to be a str")
        pulumi.set(__self__, "query_frequency", query_frequency)
        if query_period and not isinstance(query_period, str):
            raise TypeError("Expected argument 'query_period' to be a str")
        pulumi.set(__self__, "query_period", query_period)
        if sentinel_entities_mappings and not isinstance(sentinel_entities_mappings, list):
            raise TypeError("Expected argument 'sentinel_entities_mappings' to be a list")
        pulumi.set(__self__, "sentinel_entities_mappings", sentinel_entities_mappings)
        if severity and not isinstance(severity, str):
            raise TypeError("Expected argument 'severity' to be a str")
        pulumi.set(__self__, "severity", severity)
        if suppression_duration and not isinstance(suppression_duration, str):
            raise TypeError("Expected argument 'suppression_duration' to be a str")
        pulumi.set(__self__, "suppression_duration", suppression_duration)
        if suppression_enabled and not isinstance(suppression_enabled, bool):
            raise TypeError("Expected argument 'suppression_enabled' to be a bool")
        pulumi.set(__self__, "suppression_enabled", suppression_enabled)
        if system_data and not isinstance(system_data, dict):
            raise TypeError("Expected argument 'system_data' to be a dict")
        pulumi.set(__self__, "system_data", system_data)
        if tactics and not isinstance(tactics, list):
            raise TypeError("Expected argument 'tactics' to be a list")
        pulumi.set(__self__, "tactics", tactics)
        if techniques and not isinstance(techniques, list):
            raise TypeError("Expected argument 'techniques' to be a list")
        pulumi.set(__self__, "techniques", techniques)
        if template_version and not isinstance(template_version, str):
            raise TypeError("Expected argument 'template_version' to be a str")
        pulumi.set(__self__, "template_version", template_version)
        if trigger_operator and not isinstance(trigger_operator, str):
            raise TypeError("Expected argument 'trigger_operator' to be a str")
        pulumi.set(__self__, "trigger_operator", trigger_operator)
        if trigger_threshold and not isinstance(trigger_threshold, int):
            raise TypeError("Expected argument 'trigger_threshold' to be a int")
        pulumi.set(__self__, "trigger_threshold", trigger_threshold)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter(name="alertDetailsOverride")
    def alert_details_override(self) -> Optional['outputs.AlertDetailsOverrideResponse']:
        """
        The alert details override settings
        """
        return pulumi.get(self, "alert_details_override")

    @property
    @pulumi.getter(name="alertRuleTemplateName")
    def alert_rule_template_name(self) -> Optional[str]:
        """
        The Name of the alert rule template used to create this rule.
        """
        return pulumi.get(self, "alert_rule_template_name")

    @property
    @pulumi.getter(name="customDetails")
    def custom_details(self) -> Optional[Mapping[str, str]]:
        """
        Dictionary of string key-value pairs of columns to be attached to the alert
        """
        return pulumi.get(self, "custom_details")

    @property
    @pulumi.getter
    def description(self) -> Optional[str]:
        """
        The description of the alert rule.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="displayName")
    def display_name(self) -> str:
        """
        The display name for alerts created by this alert rule.
        """
        return pulumi.get(self, "display_name")

    @property
    @pulumi.getter
    def enabled(self) -> bool:
        """
        Determines whether this alert rule is enabled or disabled.
        """
        return pulumi.get(self, "enabled")

    @property
    @pulumi.getter(name="entityMappings")
    def entity_mappings(self) -> Optional[Sequence['outputs.EntityMappingResponse']]:
        """
        Array of the entity mappings of the alert rule
        """
        return pulumi.get(self, "entity_mappings")

    @property
    @pulumi.getter
    def etag(self) -> Optional[str]:
        """
        Etag of the azure resource
        """
        return pulumi.get(self, "etag")

    @property
    @pulumi.getter(name="eventGroupingSettings")
    def event_grouping_settings(self) -> Optional['outputs.EventGroupingSettingsResponse']:
        """
        The event grouping settings.
        """
        return pulumi.get(self, "event_grouping_settings")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Fully qualified resource ID for the resource. Ex - /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/{resourceProviderNamespace}/{resourceType}/{resourceName}
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="incidentConfiguration")
    def incident_configuration(self) -> Optional['outputs.IncidentConfigurationResponse']:
        """
        The settings of the incidents that created from alerts triggered by this analytics rule
        """
        return pulumi.get(self, "incident_configuration")

    @property
    @pulumi.getter
    def kind(self) -> str:
        """
        The kind of the alert rule
        Expected value is 'Scheduled'.
        """
        return pulumi.get(self, "kind")

    @property
    @pulumi.getter(name="lastModifiedUtc")
    def last_modified_utc(self) -> str:
        """
        The last time that this alert rule has been modified.
        """
        return pulumi.get(self, "last_modified_utc")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The name of the resource
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def query(self) -> str:
        """
        The query that creates alerts for this rule.
        """
        return pulumi.get(self, "query")

    @property
    @pulumi.getter(name="queryFrequency")
    def query_frequency(self) -> str:
        """
        The frequency (in ISO 8601 duration format) for this alert rule to run.
        """
        return pulumi.get(self, "query_frequency")

    @property
    @pulumi.getter(name="queryPeriod")
    def query_period(self) -> str:
        """
        The period (in ISO 8601 duration format) that this alert rule looks at.
        """
        return pulumi.get(self, "query_period")

    @property
    @pulumi.getter(name="sentinelEntitiesMappings")
    def sentinel_entities_mappings(self) -> Optional[Sequence['outputs.SentinelEntityMappingResponse']]:
        """
        Array of the sentinel entity mappings of the alert rule
        """
        return pulumi.get(self, "sentinel_entities_mappings")

    @property
    @pulumi.getter
    def severity(self) -> str:
        """
        The severity for alerts created by this alert rule.
        """
        return pulumi.get(self, "severity")

    @property
    @pulumi.getter(name="suppressionDuration")
    def suppression_duration(self) -> str:
        """
        The suppression (in ISO 8601 duration format) to wait since last time this alert rule been triggered.
        """
        return pulumi.get(self, "suppression_duration")

    @property
    @pulumi.getter(name="suppressionEnabled")
    def suppression_enabled(self) -> bool:
        """
        Determines whether the suppression for this alert rule is enabled or disabled.
        """
        return pulumi.get(self, "suppression_enabled")

    @property
    @pulumi.getter(name="systemData")
    def system_data(self) -> 'outputs.SystemDataResponse':
        """
        Azure Resource Manager metadata containing createdBy and modifiedBy information.
        """
        return pulumi.get(self, "system_data")

    @property
    @pulumi.getter
    def tactics(self) -> Optional[Sequence[str]]:
        """
        The tactics of the alert rule
        """
        return pulumi.get(self, "tactics")

    @property
    @pulumi.getter
    def techniques(self) -> Optional[Sequence[str]]:
        """
        The techniques of the alert rule
        """
        return pulumi.get(self, "techniques")

    @property
    @pulumi.getter(name="templateVersion")
    def template_version(self) -> Optional[str]:
        """
        The version of the alert rule template used to create this rule - in format <a.b.c>, where all are numbers, for example 0 <1.0.2>
        """
        return pulumi.get(self, "template_version")

    @property
    @pulumi.getter(name="triggerOperator")
    def trigger_operator(self) -> str:
        """
        The operation against the threshold that triggers alert rule.
        """
        return pulumi.get(self, "trigger_operator")

    @property
    @pulumi.getter(name="triggerThreshold")
    def trigger_threshold(self) -> int:
        """
        The threshold triggers this alert rule.
        """
        return pulumi.get(self, "trigger_threshold")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        The type of the resource. E.g. "Microsoft.Compute/virtualMachines" or "Microsoft.Storage/storageAccounts"
        """
        return pulumi.get(self, "type")


class AwaitableGetScheduledAlertRuleResult(GetScheduledAlertRuleResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetScheduledAlertRuleResult(
            alert_details_override=self.alert_details_override,
            alert_rule_template_name=self.alert_rule_template_name,
            custom_details=self.custom_details,
            description=self.description,
            display_name=self.display_name,
            enabled=self.enabled,
            entity_mappings=self.entity_mappings,
            etag=self.etag,
            event_grouping_settings=self.event_grouping_settings,
            id=self.id,
            incident_configuration=self.incident_configuration,
            kind=self.kind,
            last_modified_utc=self.last_modified_utc,
            name=self.name,
            query=self.query,
            query_frequency=self.query_frequency,
            query_period=self.query_period,
            sentinel_entities_mappings=self.sentinel_entities_mappings,
            severity=self.severity,
            suppression_duration=self.suppression_duration,
            suppression_enabled=self.suppression_enabled,
            system_data=self.system_data,
            tactics=self.tactics,
            techniques=self.techniques,
            template_version=self.template_version,
            trigger_operator=self.trigger_operator,
            trigger_threshold=self.trigger_threshold,
            type=self.type)


def get_scheduled_alert_rule(resource_group_name: Optional[str] = None,
                             rule_id: Optional[str] = None,
                             workspace_name: Optional[str] = None,
                             opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetScheduledAlertRuleResult:
    """
    Represents scheduled alert rule.


    :param str resource_group_name: The name of the resource group. The name is case insensitive.
    :param str rule_id: Alert rule ID
    :param str workspace_name: The name of the workspace.
    """
    __args__ = dict()
    __args__['resourceGroupName'] = resource_group_name
    __args__['ruleId'] = rule_id
    __args__['workspaceName'] = workspace_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:securityinsights/v20230201preview:getScheduledAlertRule', __args__, opts=opts, typ=GetScheduledAlertRuleResult).value

    return AwaitableGetScheduledAlertRuleResult(
        alert_details_override=__ret__.alert_details_override,
        alert_rule_template_name=__ret__.alert_rule_template_name,
        custom_details=__ret__.custom_details,
        description=__ret__.description,
        display_name=__ret__.display_name,
        enabled=__ret__.enabled,
        entity_mappings=__ret__.entity_mappings,
        etag=__ret__.etag,
        event_grouping_settings=__ret__.event_grouping_settings,
        id=__ret__.id,
        incident_configuration=__ret__.incident_configuration,
        kind=__ret__.kind,
        last_modified_utc=__ret__.last_modified_utc,
        name=__ret__.name,
        query=__ret__.query,
        query_frequency=__ret__.query_frequency,
        query_period=__ret__.query_period,
        sentinel_entities_mappings=__ret__.sentinel_entities_mappings,
        severity=__ret__.severity,
        suppression_duration=__ret__.suppression_duration,
        suppression_enabled=__ret__.suppression_enabled,
        system_data=__ret__.system_data,
        tactics=__ret__.tactics,
        techniques=__ret__.techniques,
        template_version=__ret__.template_version,
        trigger_operator=__ret__.trigger_operator,
        trigger_threshold=__ret__.trigger_threshold,
        type=__ret__.type)


@_utilities.lift_output_func(get_scheduled_alert_rule)
def get_scheduled_alert_rule_output(resource_group_name: Optional[pulumi.Input[str]] = None,
                                    rule_id: Optional[pulumi.Input[str]] = None,
                                    workspace_name: Optional[pulumi.Input[str]] = None,
                                    opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetScheduledAlertRuleResult]:
    """
    Represents scheduled alert rule.


    :param str resource_group_name: The name of the resource group. The name is case insensitive.
    :param str rule_id: Alert rule ID
    :param str workspace_name: The name of the workspace.
    """
    ...
