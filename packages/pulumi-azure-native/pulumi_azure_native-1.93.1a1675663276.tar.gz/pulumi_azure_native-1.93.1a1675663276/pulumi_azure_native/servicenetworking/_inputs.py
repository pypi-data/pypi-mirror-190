# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
from ._enums import *

__all__ = [
    'AssociationSubnetArgs',
    'FrontendPropertiesIPAddressArgs',
]

@pulumi.input_type
class AssociationSubnetArgs:
    def __init__(__self__, *,
                 id: pulumi.Input[str]):
        """
        Association Subnet.
        :param pulumi.Input[str] id: Association ID.
        """
        pulumi.set(__self__, "id", id)

    @property
    @pulumi.getter
    def id(self) -> pulumi.Input[str]:
        """
        Association ID.
        """
        return pulumi.get(self, "id")

    @id.setter
    def id(self, value: pulumi.Input[str]):
        pulumi.set(self, "id", value)


@pulumi.input_type
class FrontendPropertiesIPAddressArgs:
    def __init__(__self__, *,
                 id: pulumi.Input[str]):
        """
        Frontend IP Address.
        :param pulumi.Input[str] id: IP Address.
        """
        pulumi.set(__self__, "id", id)

    @property
    @pulumi.getter
    def id(self) -> pulumi.Input[str]:
        """
        IP Address.
        """
        return pulumi.get(self, "id")

    @id.setter
    def id(self, value: pulumi.Input[str]):
        pulumi.set(self, "id", value)


