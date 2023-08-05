# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

from .. import _utilities
import typing
# Export this package's modules as members:
from ._enums import *
from .configuration_assignment import *
from .configuration_assignment_parent import *
from .get_configuration_assignment import *
from .get_configuration_assignment_parent import *
from .get_maintenance_configuration import *
from .maintenance_configuration import *
from . import outputs

# Make subpackages available:
if typing.TYPE_CHECKING:
    import pulumi_azure_native.maintenance.v20180601preview as __v20180601preview
    v20180601preview = __v20180601preview
    import pulumi_azure_native.maintenance.v20200401 as __v20200401
    v20200401 = __v20200401
    import pulumi_azure_native.maintenance.v20200701preview as __v20200701preview
    v20200701preview = __v20200701preview
    import pulumi_azure_native.maintenance.v20210401preview as __v20210401preview
    v20210401preview = __v20210401preview
    import pulumi_azure_native.maintenance.v20210501 as __v20210501
    v20210501 = __v20210501
    import pulumi_azure_native.maintenance.v20210901preview as __v20210901preview
    v20210901preview = __v20210901preview
    import pulumi_azure_native.maintenance.v20220701preview as __v20220701preview
    v20220701preview = __v20220701preview
    import pulumi_azure_native.maintenance.v20221101preview as __v20221101preview
    v20221101preview = __v20221101preview
else:
    v20180601preview = _utilities.lazy_import('pulumi_azure_native.maintenance.v20180601preview')
    v20200401 = _utilities.lazy_import('pulumi_azure_native.maintenance.v20200401')
    v20200701preview = _utilities.lazy_import('pulumi_azure_native.maintenance.v20200701preview')
    v20210401preview = _utilities.lazy_import('pulumi_azure_native.maintenance.v20210401preview')
    v20210501 = _utilities.lazy_import('pulumi_azure_native.maintenance.v20210501')
    v20210901preview = _utilities.lazy_import('pulumi_azure_native.maintenance.v20210901preview')
    v20220701preview = _utilities.lazy_import('pulumi_azure_native.maintenance.v20220701preview')
    v20221101preview = _utilities.lazy_import('pulumi_azure_native.maintenance.v20221101preview')

