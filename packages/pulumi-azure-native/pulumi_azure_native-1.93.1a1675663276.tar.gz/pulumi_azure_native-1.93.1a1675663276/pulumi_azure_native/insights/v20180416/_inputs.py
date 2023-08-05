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
    'AlertingActionArgs',
    'AzNsActionGroupArgs',
    'CriteriaArgs',
    'DimensionArgs',
    'LogMetricTriggerArgs',
    'LogToMetricActionArgs',
    'ScheduleArgs',
    'SourceArgs',
    'TriggerConditionArgs',
]

@pulumi.input_type
class AlertingActionArgs:
    def __init__(__self__, *,
                 odata_type: pulumi.Input[str],
                 severity: pulumi.Input[Union[str, 'AlertSeverity']],
                 trigger: pulumi.Input['TriggerConditionArgs'],
                 azns_action: Optional[pulumi.Input['AzNsActionGroupArgs']] = None,
                 throttling_in_min: Optional[pulumi.Input[int]] = None):
        """
        Specify action need to be taken when rule type is Alert
        :param pulumi.Input[str] odata_type: Specifies the action. Supported values - AlertingAction, LogToMetricAction
               Expected value is 'Microsoft.WindowsAzure.Management.Monitoring.Alerts.Models.Microsoft.AppInsights.Nexus.DataContracts.Resources.ScheduledQueryRules.AlertingAction'.
        :param pulumi.Input[Union[str, 'AlertSeverity']] severity: Severity of the alert
        :param pulumi.Input['TriggerConditionArgs'] trigger: The trigger condition that results in the alert rule being.
        :param pulumi.Input['AzNsActionGroupArgs'] azns_action: Azure action group reference.
        :param pulumi.Input[int] throttling_in_min: time (in minutes) for which Alerts should be throttled or suppressed.
        """
        pulumi.set(__self__, "odata_type", 'Microsoft.WindowsAzure.Management.Monitoring.Alerts.Models.Microsoft.AppInsights.Nexus.DataContracts.Resources.ScheduledQueryRules.AlertingAction')
        pulumi.set(__self__, "severity", severity)
        pulumi.set(__self__, "trigger", trigger)
        if azns_action is not None:
            pulumi.set(__self__, "azns_action", azns_action)
        if throttling_in_min is not None:
            pulumi.set(__self__, "throttling_in_min", throttling_in_min)

    @property
    @pulumi.getter(name="odataType")
    def odata_type(self) -> pulumi.Input[str]:
        """
        Specifies the action. Supported values - AlertingAction, LogToMetricAction
        Expected value is 'Microsoft.WindowsAzure.Management.Monitoring.Alerts.Models.Microsoft.AppInsights.Nexus.DataContracts.Resources.ScheduledQueryRules.AlertingAction'.
        """
        return pulumi.get(self, "odata_type")

    @odata_type.setter
    def odata_type(self, value: pulumi.Input[str]):
        pulumi.set(self, "odata_type", value)

    @property
    @pulumi.getter
    def severity(self) -> pulumi.Input[Union[str, 'AlertSeverity']]:
        """
        Severity of the alert
        """
        return pulumi.get(self, "severity")

    @severity.setter
    def severity(self, value: pulumi.Input[Union[str, 'AlertSeverity']]):
        pulumi.set(self, "severity", value)

    @property
    @pulumi.getter
    def trigger(self) -> pulumi.Input['TriggerConditionArgs']:
        """
        The trigger condition that results in the alert rule being.
        """
        return pulumi.get(self, "trigger")

    @trigger.setter
    def trigger(self, value: pulumi.Input['TriggerConditionArgs']):
        pulumi.set(self, "trigger", value)

    @property
    @pulumi.getter(name="aznsAction")
    def azns_action(self) -> Optional[pulumi.Input['AzNsActionGroupArgs']]:
        """
        Azure action group reference.
        """
        return pulumi.get(self, "azns_action")

    @azns_action.setter
    def azns_action(self, value: Optional[pulumi.Input['AzNsActionGroupArgs']]):
        pulumi.set(self, "azns_action", value)

    @property
    @pulumi.getter(name="throttlingInMin")
    def throttling_in_min(self) -> Optional[pulumi.Input[int]]:
        """
        time (in minutes) for which Alerts should be throttled or suppressed.
        """
        return pulumi.get(self, "throttling_in_min")

    @throttling_in_min.setter
    def throttling_in_min(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "throttling_in_min", value)


@pulumi.input_type
class AzNsActionGroupArgs:
    def __init__(__self__, *,
                 action_group: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 custom_webhook_payload: Optional[pulumi.Input[str]] = None,
                 email_subject: Optional[pulumi.Input[str]] = None):
        """
        Azure action group
        :param pulumi.Input[Sequence[pulumi.Input[str]]] action_group: Azure Action Group reference.
        :param pulumi.Input[str] custom_webhook_payload: Custom payload to be sent for all webhook URI in Azure action group
        :param pulumi.Input[str] email_subject: Custom subject override for all email ids in Azure action group
        """
        if action_group is not None:
            pulumi.set(__self__, "action_group", action_group)
        if custom_webhook_payload is not None:
            pulumi.set(__self__, "custom_webhook_payload", custom_webhook_payload)
        if email_subject is not None:
            pulumi.set(__self__, "email_subject", email_subject)

    @property
    @pulumi.getter(name="actionGroup")
    def action_group(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        Azure Action Group reference.
        """
        return pulumi.get(self, "action_group")

    @action_group.setter
    def action_group(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "action_group", value)

    @property
    @pulumi.getter(name="customWebhookPayload")
    def custom_webhook_payload(self) -> Optional[pulumi.Input[str]]:
        """
        Custom payload to be sent for all webhook URI in Azure action group
        """
        return pulumi.get(self, "custom_webhook_payload")

    @custom_webhook_payload.setter
    def custom_webhook_payload(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "custom_webhook_payload", value)

    @property
    @pulumi.getter(name="emailSubject")
    def email_subject(self) -> Optional[pulumi.Input[str]]:
        """
        Custom subject override for all email ids in Azure action group
        """
        return pulumi.get(self, "email_subject")

    @email_subject.setter
    def email_subject(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "email_subject", value)


@pulumi.input_type
class CriteriaArgs:
    def __init__(__self__, *,
                 metric_name: pulumi.Input[str],
                 dimensions: Optional[pulumi.Input[Sequence[pulumi.Input['DimensionArgs']]]] = None):
        """
        Specifies the criteria for converting log to metric.
        :param pulumi.Input[str] metric_name: Name of the metric
        :param pulumi.Input[Sequence[pulumi.Input['DimensionArgs']]] dimensions: List of Dimensions for creating metric
        """
        pulumi.set(__self__, "metric_name", metric_name)
        if dimensions is not None:
            pulumi.set(__self__, "dimensions", dimensions)

    @property
    @pulumi.getter(name="metricName")
    def metric_name(self) -> pulumi.Input[str]:
        """
        Name of the metric
        """
        return pulumi.get(self, "metric_name")

    @metric_name.setter
    def metric_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "metric_name", value)

    @property
    @pulumi.getter
    def dimensions(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['DimensionArgs']]]]:
        """
        List of Dimensions for creating metric
        """
        return pulumi.get(self, "dimensions")

    @dimensions.setter
    def dimensions(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['DimensionArgs']]]]):
        pulumi.set(self, "dimensions", value)


@pulumi.input_type
class DimensionArgs:
    def __init__(__self__, *,
                 name: pulumi.Input[str],
                 operator: pulumi.Input[Union[str, 'Operator']],
                 values: pulumi.Input[Sequence[pulumi.Input[str]]]):
        """
        Specifies the criteria for converting log to metric.
        :param pulumi.Input[str] name: Name of the dimension
        :param pulumi.Input[Union[str, 'Operator']] operator: Operator for dimension values
        :param pulumi.Input[Sequence[pulumi.Input[str]]] values: List of dimension values
        """
        pulumi.set(__self__, "name", name)
        pulumi.set(__self__, "operator", operator)
        pulumi.set(__self__, "values", values)

    @property
    @pulumi.getter
    def name(self) -> pulumi.Input[str]:
        """
        Name of the dimension
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: pulumi.Input[str]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def operator(self) -> pulumi.Input[Union[str, 'Operator']]:
        """
        Operator for dimension values
        """
        return pulumi.get(self, "operator")

    @operator.setter
    def operator(self, value: pulumi.Input[Union[str, 'Operator']]):
        pulumi.set(self, "operator", value)

    @property
    @pulumi.getter
    def values(self) -> pulumi.Input[Sequence[pulumi.Input[str]]]:
        """
        List of dimension values
        """
        return pulumi.get(self, "values")

    @values.setter
    def values(self, value: pulumi.Input[Sequence[pulumi.Input[str]]]):
        pulumi.set(self, "values", value)


@pulumi.input_type
class LogMetricTriggerArgs:
    def __init__(__self__, *,
                 metric_column: Optional[pulumi.Input[str]] = None,
                 metric_trigger_type: Optional[pulumi.Input[Union[str, 'MetricTriggerType']]] = None,
                 threshold: Optional[pulumi.Input[float]] = None,
                 threshold_operator: Optional[pulumi.Input[Union[str, 'ConditionalOperator']]] = None):
        """
        A log metrics trigger descriptor.
        :param pulumi.Input[str] metric_column: Evaluation of metric on a particular column
        :param pulumi.Input[Union[str, 'MetricTriggerType']] metric_trigger_type: Metric Trigger Type - 'Consecutive' or 'Total'
        :param pulumi.Input[float] threshold: The threshold of the metric trigger.
        :param pulumi.Input[Union[str, 'ConditionalOperator']] threshold_operator: Evaluation operation for Metric -'GreaterThan' or 'LessThan' or 'Equal'.
        """
        if metric_column is not None:
            pulumi.set(__self__, "metric_column", metric_column)
        if metric_trigger_type is not None:
            pulumi.set(__self__, "metric_trigger_type", metric_trigger_type)
        if threshold is not None:
            pulumi.set(__self__, "threshold", threshold)
        if threshold_operator is not None:
            pulumi.set(__self__, "threshold_operator", threshold_operator)

    @property
    @pulumi.getter(name="metricColumn")
    def metric_column(self) -> Optional[pulumi.Input[str]]:
        """
        Evaluation of metric on a particular column
        """
        return pulumi.get(self, "metric_column")

    @metric_column.setter
    def metric_column(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "metric_column", value)

    @property
    @pulumi.getter(name="metricTriggerType")
    def metric_trigger_type(self) -> Optional[pulumi.Input[Union[str, 'MetricTriggerType']]]:
        """
        Metric Trigger Type - 'Consecutive' or 'Total'
        """
        return pulumi.get(self, "metric_trigger_type")

    @metric_trigger_type.setter
    def metric_trigger_type(self, value: Optional[pulumi.Input[Union[str, 'MetricTriggerType']]]):
        pulumi.set(self, "metric_trigger_type", value)

    @property
    @pulumi.getter
    def threshold(self) -> Optional[pulumi.Input[float]]:
        """
        The threshold of the metric trigger.
        """
        return pulumi.get(self, "threshold")

    @threshold.setter
    def threshold(self, value: Optional[pulumi.Input[float]]):
        pulumi.set(self, "threshold", value)

    @property
    @pulumi.getter(name="thresholdOperator")
    def threshold_operator(self) -> Optional[pulumi.Input[Union[str, 'ConditionalOperator']]]:
        """
        Evaluation operation for Metric -'GreaterThan' or 'LessThan' or 'Equal'.
        """
        return pulumi.get(self, "threshold_operator")

    @threshold_operator.setter
    def threshold_operator(self, value: Optional[pulumi.Input[Union[str, 'ConditionalOperator']]]):
        pulumi.set(self, "threshold_operator", value)


@pulumi.input_type
class LogToMetricActionArgs:
    def __init__(__self__, *,
                 criteria: pulumi.Input[Sequence[pulumi.Input['CriteriaArgs']]],
                 odata_type: pulumi.Input[str]):
        """
        Specify action need to be taken when rule type is converting log to metric
        :param pulumi.Input[Sequence[pulumi.Input['CriteriaArgs']]] criteria: Criteria of Metric
        :param pulumi.Input[str] odata_type: Specifies the action. Supported values - AlertingAction, LogToMetricAction
               Expected value is 'Microsoft.WindowsAzure.Management.Monitoring.Alerts.Models.Microsoft.AppInsights.Nexus.DataContracts.Resources.ScheduledQueryRules.LogToMetricAction'.
        """
        pulumi.set(__self__, "criteria", criteria)
        pulumi.set(__self__, "odata_type", 'Microsoft.WindowsAzure.Management.Monitoring.Alerts.Models.Microsoft.AppInsights.Nexus.DataContracts.Resources.ScheduledQueryRules.LogToMetricAction')

    @property
    @pulumi.getter
    def criteria(self) -> pulumi.Input[Sequence[pulumi.Input['CriteriaArgs']]]:
        """
        Criteria of Metric
        """
        return pulumi.get(self, "criteria")

    @criteria.setter
    def criteria(self, value: pulumi.Input[Sequence[pulumi.Input['CriteriaArgs']]]):
        pulumi.set(self, "criteria", value)

    @property
    @pulumi.getter(name="odataType")
    def odata_type(self) -> pulumi.Input[str]:
        """
        Specifies the action. Supported values - AlertingAction, LogToMetricAction
        Expected value is 'Microsoft.WindowsAzure.Management.Monitoring.Alerts.Models.Microsoft.AppInsights.Nexus.DataContracts.Resources.ScheduledQueryRules.LogToMetricAction'.
        """
        return pulumi.get(self, "odata_type")

    @odata_type.setter
    def odata_type(self, value: pulumi.Input[str]):
        pulumi.set(self, "odata_type", value)


@pulumi.input_type
class ScheduleArgs:
    def __init__(__self__, *,
                 frequency_in_minutes: pulumi.Input[int],
                 time_window_in_minutes: pulumi.Input[int]):
        """
        Defines how often to run the search and the time interval.
        :param pulumi.Input[int] frequency_in_minutes: frequency (in minutes) at which rule condition should be evaluated.
        :param pulumi.Input[int] time_window_in_minutes: Time window for which data needs to be fetched for query (should be greater than or equal to frequencyInMinutes).
        """
        pulumi.set(__self__, "frequency_in_minutes", frequency_in_minutes)
        pulumi.set(__self__, "time_window_in_minutes", time_window_in_minutes)

    @property
    @pulumi.getter(name="frequencyInMinutes")
    def frequency_in_minutes(self) -> pulumi.Input[int]:
        """
        frequency (in minutes) at which rule condition should be evaluated.
        """
        return pulumi.get(self, "frequency_in_minutes")

    @frequency_in_minutes.setter
    def frequency_in_minutes(self, value: pulumi.Input[int]):
        pulumi.set(self, "frequency_in_minutes", value)

    @property
    @pulumi.getter(name="timeWindowInMinutes")
    def time_window_in_minutes(self) -> pulumi.Input[int]:
        """
        Time window for which data needs to be fetched for query (should be greater than or equal to frequencyInMinutes).
        """
        return pulumi.get(self, "time_window_in_minutes")

    @time_window_in_minutes.setter
    def time_window_in_minutes(self, value: pulumi.Input[int]):
        pulumi.set(self, "time_window_in_minutes", value)


@pulumi.input_type
class SourceArgs:
    def __init__(__self__, *,
                 data_source_id: pulumi.Input[str],
                 authorized_resources: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 query: Optional[pulumi.Input[str]] = None,
                 query_type: Optional[pulumi.Input[Union[str, 'QueryType']]] = None):
        """
        Specifies the log search query.
        :param pulumi.Input[str] data_source_id: The resource uri over which log search query is to be run.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] authorized_resources: List of  Resource referred into query
        :param pulumi.Input[str] query: Log search query. Required for action type - AlertingAction
        :param pulumi.Input[Union[str, 'QueryType']] query_type: Set value to 'ResultCount' .
        """
        pulumi.set(__self__, "data_source_id", data_source_id)
        if authorized_resources is not None:
            pulumi.set(__self__, "authorized_resources", authorized_resources)
        if query is not None:
            pulumi.set(__self__, "query", query)
        if query_type is not None:
            pulumi.set(__self__, "query_type", query_type)

    @property
    @pulumi.getter(name="dataSourceId")
    def data_source_id(self) -> pulumi.Input[str]:
        """
        The resource uri over which log search query is to be run.
        """
        return pulumi.get(self, "data_source_id")

    @data_source_id.setter
    def data_source_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "data_source_id", value)

    @property
    @pulumi.getter(name="authorizedResources")
    def authorized_resources(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        List of  Resource referred into query
        """
        return pulumi.get(self, "authorized_resources")

    @authorized_resources.setter
    def authorized_resources(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "authorized_resources", value)

    @property
    @pulumi.getter
    def query(self) -> Optional[pulumi.Input[str]]:
        """
        Log search query. Required for action type - AlertingAction
        """
        return pulumi.get(self, "query")

    @query.setter
    def query(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "query", value)

    @property
    @pulumi.getter(name="queryType")
    def query_type(self) -> Optional[pulumi.Input[Union[str, 'QueryType']]]:
        """
        Set value to 'ResultCount' .
        """
        return pulumi.get(self, "query_type")

    @query_type.setter
    def query_type(self, value: Optional[pulumi.Input[Union[str, 'QueryType']]]):
        pulumi.set(self, "query_type", value)


@pulumi.input_type
class TriggerConditionArgs:
    def __init__(__self__, *,
                 threshold: pulumi.Input[float],
                 threshold_operator: pulumi.Input[Union[str, 'ConditionalOperator']],
                 metric_trigger: Optional[pulumi.Input['LogMetricTriggerArgs']] = None):
        """
        The condition that results in the Log Search rule.
        :param pulumi.Input[float] threshold: Result or count threshold based on which rule should be triggered.
        :param pulumi.Input[Union[str, 'ConditionalOperator']] threshold_operator: Evaluation operation for rule - 'GreaterThan' or 'LessThan.
        :param pulumi.Input['LogMetricTriggerArgs'] metric_trigger: Trigger condition for metric query rule
        """
        pulumi.set(__self__, "threshold", threshold)
        pulumi.set(__self__, "threshold_operator", threshold_operator)
        if metric_trigger is not None:
            pulumi.set(__self__, "metric_trigger", metric_trigger)

    @property
    @pulumi.getter
    def threshold(self) -> pulumi.Input[float]:
        """
        Result or count threshold based on which rule should be triggered.
        """
        return pulumi.get(self, "threshold")

    @threshold.setter
    def threshold(self, value: pulumi.Input[float]):
        pulumi.set(self, "threshold", value)

    @property
    @pulumi.getter(name="thresholdOperator")
    def threshold_operator(self) -> pulumi.Input[Union[str, 'ConditionalOperator']]:
        """
        Evaluation operation for rule - 'GreaterThan' or 'LessThan.
        """
        return pulumi.get(self, "threshold_operator")

    @threshold_operator.setter
    def threshold_operator(self, value: pulumi.Input[Union[str, 'ConditionalOperator']]):
        pulumi.set(self, "threshold_operator", value)

    @property
    @pulumi.getter(name="metricTrigger")
    def metric_trigger(self) -> Optional[pulumi.Input['LogMetricTriggerArgs']]:
        """
        Trigger condition for metric query rule
        """
        return pulumi.get(self, "metric_trigger")

    @metric_trigger.setter
    def metric_trigger(self, value: Optional[pulumi.Input['LogMetricTriggerArgs']]):
        pulumi.set(self, "metric_trigger", value)


