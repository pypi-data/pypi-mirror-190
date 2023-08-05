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
    'GetAccessReviewHistoryDefinitionByIdResult',
    'AwaitableGetAccessReviewHistoryDefinitionByIdResult',
    'get_access_review_history_definition_by_id',
    'get_access_review_history_definition_by_id_output',
]

@pulumi.output_type
class GetAccessReviewHistoryDefinitionByIdResult:
    """
    Access Review History Definition.
    """
    def __init__(__self__, created_date_time=None, decisions=None, display_name=None, end_date=None, id=None, instances=None, interval=None, name=None, number_of_occurrences=None, principal_id=None, principal_name=None, principal_type=None, review_history_period_end_date_time=None, review_history_period_start_date_time=None, scopes=None, start_date=None, status=None, type=None, user_principal_name=None):
        if created_date_time and not isinstance(created_date_time, str):
            raise TypeError("Expected argument 'created_date_time' to be a str")
        pulumi.set(__self__, "created_date_time", created_date_time)
        if decisions and not isinstance(decisions, list):
            raise TypeError("Expected argument 'decisions' to be a list")
        pulumi.set(__self__, "decisions", decisions)
        if display_name and not isinstance(display_name, str):
            raise TypeError("Expected argument 'display_name' to be a str")
        pulumi.set(__self__, "display_name", display_name)
        if end_date and not isinstance(end_date, str):
            raise TypeError("Expected argument 'end_date' to be a str")
        pulumi.set(__self__, "end_date", end_date)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if instances and not isinstance(instances, list):
            raise TypeError("Expected argument 'instances' to be a list")
        pulumi.set(__self__, "instances", instances)
        if interval and not isinstance(interval, int):
            raise TypeError("Expected argument 'interval' to be a int")
        pulumi.set(__self__, "interval", interval)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if number_of_occurrences and not isinstance(number_of_occurrences, int):
            raise TypeError("Expected argument 'number_of_occurrences' to be a int")
        pulumi.set(__self__, "number_of_occurrences", number_of_occurrences)
        if principal_id and not isinstance(principal_id, str):
            raise TypeError("Expected argument 'principal_id' to be a str")
        pulumi.set(__self__, "principal_id", principal_id)
        if principal_name and not isinstance(principal_name, str):
            raise TypeError("Expected argument 'principal_name' to be a str")
        pulumi.set(__self__, "principal_name", principal_name)
        if principal_type and not isinstance(principal_type, str):
            raise TypeError("Expected argument 'principal_type' to be a str")
        pulumi.set(__self__, "principal_type", principal_type)
        if review_history_period_end_date_time and not isinstance(review_history_period_end_date_time, str):
            raise TypeError("Expected argument 'review_history_period_end_date_time' to be a str")
        pulumi.set(__self__, "review_history_period_end_date_time", review_history_period_end_date_time)
        if review_history_period_start_date_time and not isinstance(review_history_period_start_date_time, str):
            raise TypeError("Expected argument 'review_history_period_start_date_time' to be a str")
        pulumi.set(__self__, "review_history_period_start_date_time", review_history_period_start_date_time)
        if scopes and not isinstance(scopes, list):
            raise TypeError("Expected argument 'scopes' to be a list")
        pulumi.set(__self__, "scopes", scopes)
        if start_date and not isinstance(start_date, str):
            raise TypeError("Expected argument 'start_date' to be a str")
        pulumi.set(__self__, "start_date", start_date)
        if status and not isinstance(status, str):
            raise TypeError("Expected argument 'status' to be a str")
        pulumi.set(__self__, "status", status)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)
        if user_principal_name and not isinstance(user_principal_name, str):
            raise TypeError("Expected argument 'user_principal_name' to be a str")
        pulumi.set(__self__, "user_principal_name", user_principal_name)

    @property
    @pulumi.getter(name="createdDateTime")
    def created_date_time(self) -> str:
        """
        Date time when history definition was created
        """
        return pulumi.get(self, "created_date_time")

    @property
    @pulumi.getter
    def decisions(self) -> Optional[Sequence[str]]:
        """
        Collection of review decisions which the history data should be filtered on. For example if Approve and Deny are supplied the data will only contain review results in which the decision maker approved or denied a review request.
        """
        return pulumi.get(self, "decisions")

    @property
    @pulumi.getter(name="displayName")
    def display_name(self) -> Optional[str]:
        """
        The display name for the history definition.
        """
        return pulumi.get(self, "display_name")

    @property
    @pulumi.getter(name="endDate")
    def end_date(self) -> Optional[str]:
        """
        The DateTime when the review is scheduled to end. Required if type is endDate
        """
        return pulumi.get(self, "end_date")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The access review history definition id.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def instances(self) -> Optional[Sequence['outputs.AccessReviewHistoryInstanceResponse']]:
        """
        Set of access review history instances for this history definition.
        """
        return pulumi.get(self, "instances")

    @property
    @pulumi.getter
    def interval(self) -> Optional[int]:
        """
        The interval for recurrence. For a quarterly review, the interval is 3 for type : absoluteMonthly.
        """
        return pulumi.get(self, "interval")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The access review history definition unique id.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="numberOfOccurrences")
    def number_of_occurrences(self) -> Optional[int]:
        """
        The number of times to repeat the access review. Required and must be positive if type is numbered.
        """
        return pulumi.get(self, "number_of_occurrences")

    @property
    @pulumi.getter(name="principalId")
    def principal_id(self) -> str:
        """
        The identity id
        """
        return pulumi.get(self, "principal_id")

    @property
    @pulumi.getter(name="principalName")
    def principal_name(self) -> str:
        """
        The identity display name
        """
        return pulumi.get(self, "principal_name")

    @property
    @pulumi.getter(name="principalType")
    def principal_type(self) -> str:
        """
        The identity type : user/servicePrincipal
        """
        return pulumi.get(self, "principal_type")

    @property
    @pulumi.getter(name="reviewHistoryPeriodEndDateTime")
    def review_history_period_end_date_time(self) -> str:
        """
        Date time used when selecting review data, all reviews included in data end on or before this date. For use only with one-time/non-recurring reports.
        """
        return pulumi.get(self, "review_history_period_end_date_time")

    @property
    @pulumi.getter(name="reviewHistoryPeriodStartDateTime")
    def review_history_period_start_date_time(self) -> str:
        """
        Date time used when selecting review data, all reviews included in data start on or after this date. For use only with one-time/non-recurring reports.
        """
        return pulumi.get(self, "review_history_period_start_date_time")

    @property
    @pulumi.getter
    def scopes(self) -> Optional[Sequence['outputs.AccessReviewScopeResponse']]:
        """
        A collection of scopes used when selecting review history data
        """
        return pulumi.get(self, "scopes")

    @property
    @pulumi.getter(name="startDate")
    def start_date(self) -> Optional[str]:
        """
        The DateTime when the review is scheduled to be start. This could be a date in the future. Required on create.
        """
        return pulumi.get(self, "start_date")

    @property
    @pulumi.getter
    def status(self) -> str:
        """
        This read-only field specifies the of the requested review history data. This is either requested, in-progress, done or error.
        """
        return pulumi.get(self, "status")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        The resource type.
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter(name="userPrincipalName")
    def user_principal_name(self) -> str:
        """
        The user principal name(if valid)
        """
        return pulumi.get(self, "user_principal_name")


class AwaitableGetAccessReviewHistoryDefinitionByIdResult(GetAccessReviewHistoryDefinitionByIdResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetAccessReviewHistoryDefinitionByIdResult(
            created_date_time=self.created_date_time,
            decisions=self.decisions,
            display_name=self.display_name,
            end_date=self.end_date,
            id=self.id,
            instances=self.instances,
            interval=self.interval,
            name=self.name,
            number_of_occurrences=self.number_of_occurrences,
            principal_id=self.principal_id,
            principal_name=self.principal_name,
            principal_type=self.principal_type,
            review_history_period_end_date_time=self.review_history_period_end_date_time,
            review_history_period_start_date_time=self.review_history_period_start_date_time,
            scopes=self.scopes,
            start_date=self.start_date,
            status=self.status,
            type=self.type,
            user_principal_name=self.user_principal_name)


def get_access_review_history_definition_by_id(history_definition_id: Optional[str] = None,
                                               opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetAccessReviewHistoryDefinitionByIdResult:
    """
    Access Review History Definition.


    :param str history_definition_id: The id of the access review history definition.
    """
    __args__ = dict()
    __args__['historyDefinitionId'] = history_definition_id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:authorization/v20211201preview:getAccessReviewHistoryDefinitionById', __args__, opts=opts, typ=GetAccessReviewHistoryDefinitionByIdResult).value

    return AwaitableGetAccessReviewHistoryDefinitionByIdResult(
        created_date_time=__ret__.created_date_time,
        decisions=__ret__.decisions,
        display_name=__ret__.display_name,
        end_date=__ret__.end_date,
        id=__ret__.id,
        instances=__ret__.instances,
        interval=__ret__.interval,
        name=__ret__.name,
        number_of_occurrences=__ret__.number_of_occurrences,
        principal_id=__ret__.principal_id,
        principal_name=__ret__.principal_name,
        principal_type=__ret__.principal_type,
        review_history_period_end_date_time=__ret__.review_history_period_end_date_time,
        review_history_period_start_date_time=__ret__.review_history_period_start_date_time,
        scopes=__ret__.scopes,
        start_date=__ret__.start_date,
        status=__ret__.status,
        type=__ret__.type,
        user_principal_name=__ret__.user_principal_name)


@_utilities.lift_output_func(get_access_review_history_definition_by_id)
def get_access_review_history_definition_by_id_output(history_definition_id: Optional[pulumi.Input[str]] = None,
                                                      opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetAccessReviewHistoryDefinitionByIdResult]:
    """
    Access Review History Definition.


    :param str history_definition_id: The id of the access review history definition.
    """
    ...
