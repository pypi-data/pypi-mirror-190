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
from ._enums import *

__all__ = [
    'AccessReviewInstanceResponse',
    'AccessReviewReviewerResponse',
]

@pulumi.output_type
class AccessReviewInstanceResponse(dict):
    """
    Access Review Instance.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "reviewersType":
            suggest = "reviewers_type"
        elif key == "backupReviewers":
            suggest = "backup_reviewers"
        elif key == "endDateTime":
            suggest = "end_date_time"
        elif key == "startDateTime":
            suggest = "start_date_time"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in AccessReviewInstanceResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        AccessReviewInstanceResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        AccessReviewInstanceResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 id: str,
                 name: str,
                 reviewers_type: str,
                 status: str,
                 type: str,
                 backup_reviewers: Optional[Sequence['outputs.AccessReviewReviewerResponse']] = None,
                 end_date_time: Optional[str] = None,
                 reviewers: Optional[Sequence['outputs.AccessReviewReviewerResponse']] = None,
                 start_date_time: Optional[str] = None):
        """
        Access Review Instance.
        :param str id: The access review instance id.
        :param str name: The access review instance name.
        :param str reviewers_type: This field specifies the type of reviewers for a review. Usually for a review, reviewers are explicitly assigned. However, in some cases, the reviewers may not be assigned and instead be chosen dynamically. For example managers review or self review.
        :param str status: This read-only field specifies the status of an access review instance.
        :param str type: The resource type.
        :param Sequence['AccessReviewReviewerResponse'] backup_reviewers: This is the collection of backup reviewers.
        :param str end_date_time: The DateTime when the review instance is scheduled to end.
        :param Sequence['AccessReviewReviewerResponse'] reviewers: This is the collection of reviewers.
        :param str start_date_time: The DateTime when the review instance is scheduled to be start.
        """
        pulumi.set(__self__, "id", id)
        pulumi.set(__self__, "name", name)
        pulumi.set(__self__, "reviewers_type", reviewers_type)
        pulumi.set(__self__, "status", status)
        pulumi.set(__self__, "type", type)
        if backup_reviewers is not None:
            pulumi.set(__self__, "backup_reviewers", backup_reviewers)
        if end_date_time is not None:
            pulumi.set(__self__, "end_date_time", end_date_time)
        if reviewers is not None:
            pulumi.set(__self__, "reviewers", reviewers)
        if start_date_time is not None:
            pulumi.set(__self__, "start_date_time", start_date_time)

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The access review instance id.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The access review instance name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="reviewersType")
    def reviewers_type(self) -> str:
        """
        This field specifies the type of reviewers for a review. Usually for a review, reviewers are explicitly assigned. However, in some cases, the reviewers may not be assigned and instead be chosen dynamically. For example managers review or self review.
        """
        return pulumi.get(self, "reviewers_type")

    @property
    @pulumi.getter
    def status(self) -> str:
        """
        This read-only field specifies the status of an access review instance.
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
    @pulumi.getter(name="backupReviewers")
    def backup_reviewers(self) -> Optional[Sequence['outputs.AccessReviewReviewerResponse']]:
        """
        This is the collection of backup reviewers.
        """
        return pulumi.get(self, "backup_reviewers")

    @property
    @pulumi.getter(name="endDateTime")
    def end_date_time(self) -> Optional[str]:
        """
        The DateTime when the review instance is scheduled to end.
        """
        return pulumi.get(self, "end_date_time")

    @property
    @pulumi.getter
    def reviewers(self) -> Optional[Sequence['outputs.AccessReviewReviewerResponse']]:
        """
        This is the collection of reviewers.
        """
        return pulumi.get(self, "reviewers")

    @property
    @pulumi.getter(name="startDateTime")
    def start_date_time(self) -> Optional[str]:
        """
        The DateTime when the review instance is scheduled to be start.
        """
        return pulumi.get(self, "start_date_time")


@pulumi.output_type
class AccessReviewReviewerResponse(dict):
    """
    Descriptor for what needs to be reviewed
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "principalType":
            suggest = "principal_type"
        elif key == "principalId":
            suggest = "principal_id"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in AccessReviewReviewerResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        AccessReviewReviewerResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        AccessReviewReviewerResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 principal_type: str,
                 principal_id: Optional[str] = None):
        """
        Descriptor for what needs to be reviewed
        :param str principal_type: The identity type : user/servicePrincipal
        :param str principal_id: The id of the reviewer(user/servicePrincipal)
        """
        pulumi.set(__self__, "principal_type", principal_type)
        if principal_id is not None:
            pulumi.set(__self__, "principal_id", principal_id)

    @property
    @pulumi.getter(name="principalType")
    def principal_type(self) -> str:
        """
        The identity type : user/servicePrincipal
        """
        return pulumi.get(self, "principal_type")

    @property
    @pulumi.getter(name="principalId")
    def principal_id(self) -> Optional[str]:
        """
        The id of the reviewer(user/servicePrincipal)
        """
        return pulumi.get(self, "principal_id")


