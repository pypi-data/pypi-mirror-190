# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

from .. import _utilities
import typing
# Export this package's modules as members:
from ._enums import *
from .configuration import *
from .database import *
from .firewall_rule import *
from .get_configuration import *
from .get_database import *
from .get_firewall_rule import *
from .get_get_private_dns_zone_suffix_execute import *
from .get_private_endpoint_connection import *
from .get_server import *
from .get_server_administrator import *
from .get_server_key import *
from .get_virtual_network_rule import *
from .private_endpoint_connection import *
from .server import *
from .server_administrator import *
from .server_key import *
from .virtual_network_rule import *
from ._inputs import *
from . import outputs

# Make subpackages available:
if typing.TYPE_CHECKING:
    import pulumi_azure_native.dbformysql.v20171201 as __v20171201
    v20171201 = __v20171201
    import pulumi_azure_native.dbformysql.v20171201preview as __v20171201preview
    v20171201preview = __v20171201preview
    import pulumi_azure_native.dbformysql.v20180601 as __v20180601
    v20180601 = __v20180601
    import pulumi_azure_native.dbformysql.v20180601privatepreview as __v20180601privatepreview
    v20180601privatepreview = __v20180601privatepreview
    import pulumi_azure_native.dbformysql.v20200101 as __v20200101
    v20200101 = __v20200101
    import pulumi_azure_native.dbformysql.v20200101privatepreview as __v20200101privatepreview
    v20200101privatepreview = __v20200101privatepreview
    import pulumi_azure_native.dbformysql.v20200701preview as __v20200701preview
    v20200701preview = __v20200701preview
    import pulumi_azure_native.dbformysql.v20200701privatepreview as __v20200701privatepreview
    v20200701privatepreview = __v20200701privatepreview
    import pulumi_azure_native.dbformysql.v20210501 as __v20210501
    v20210501 = __v20210501
    import pulumi_azure_native.dbformysql.v20210501preview as __v20210501preview
    v20210501preview = __v20210501preview
    import pulumi_azure_native.dbformysql.v20211201preview as __v20211201preview
    v20211201preview = __v20211201preview
else:
    v20171201 = _utilities.lazy_import('pulumi_azure_native.dbformysql.v20171201')
    v20171201preview = _utilities.lazy_import('pulumi_azure_native.dbformysql.v20171201preview')
    v20180601 = _utilities.lazy_import('pulumi_azure_native.dbformysql.v20180601')
    v20180601privatepreview = _utilities.lazy_import('pulumi_azure_native.dbformysql.v20180601privatepreview')
    v20200101 = _utilities.lazy_import('pulumi_azure_native.dbformysql.v20200101')
    v20200101privatepreview = _utilities.lazy_import('pulumi_azure_native.dbformysql.v20200101privatepreview')
    v20200701preview = _utilities.lazy_import('pulumi_azure_native.dbformysql.v20200701preview')
    v20200701privatepreview = _utilities.lazy_import('pulumi_azure_native.dbformysql.v20200701privatepreview')
    v20210501 = _utilities.lazy_import('pulumi_azure_native.dbformysql.v20210501')
    v20210501preview = _utilities.lazy_import('pulumi_azure_native.dbformysql.v20210501preview')
    v20211201preview = _utilities.lazy_import('pulumi_azure_native.dbformysql.v20211201preview')

