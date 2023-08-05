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
from .get_private_endpoint_connection import *
from .get_server import *
from .get_server_administrator import *
from .get_server_key import *
from .get_server_security_alert_policy import *
from .get_virtual_network_rule import *
from .private_endpoint_connection import *
from .server import *
from .server_administrator import *
from .server_key import *
from .server_security_alert_policy import *
from .virtual_network_rule import *
from ._inputs import *
from . import outputs

# Make subpackages available:
if typing.TYPE_CHECKING:
    import pulumi_azure_native.dbforpostgresql.v20171201 as __v20171201
    v20171201 = __v20171201
    import pulumi_azure_native.dbforpostgresql.v20171201preview as __v20171201preview
    v20171201preview = __v20171201preview
    import pulumi_azure_native.dbforpostgresql.v20180601 as __v20180601
    v20180601 = __v20180601
    import pulumi_azure_native.dbforpostgresql.v20180601privatepreview as __v20180601privatepreview
    v20180601privatepreview = __v20180601privatepreview
    import pulumi_azure_native.dbforpostgresql.v20200101 as __v20200101
    v20200101 = __v20200101
    import pulumi_azure_native.dbforpostgresql.v20200101privatepreview as __v20200101privatepreview
    v20200101privatepreview = __v20200101privatepreview
    import pulumi_azure_native.dbforpostgresql.v20200214preview as __v20200214preview
    v20200214preview = __v20200214preview
    import pulumi_azure_native.dbforpostgresql.v20200214privatepreview as __v20200214privatepreview
    v20200214privatepreview = __v20200214privatepreview
    import pulumi_azure_native.dbforpostgresql.v20201005privatepreview as __v20201005privatepreview
    v20201005privatepreview = __v20201005privatepreview
    import pulumi_azure_native.dbforpostgresql.v20201105preview as __v20201105preview
    v20201105preview = __v20201105preview
    import pulumi_azure_native.dbforpostgresql.v20210410privatepreview as __v20210410privatepreview
    v20210410privatepreview = __v20210410privatepreview
    import pulumi_azure_native.dbforpostgresql.v20210601 as __v20210601
    v20210601 = __v20210601
    import pulumi_azure_native.dbforpostgresql.v20210601preview as __v20210601preview
    v20210601preview = __v20210601preview
    import pulumi_azure_native.dbforpostgresql.v20210615privatepreview as __v20210615privatepreview
    v20210615privatepreview = __v20210615privatepreview
    import pulumi_azure_native.dbforpostgresql.v20220120preview as __v20220120preview
    v20220120preview = __v20220120preview
    import pulumi_azure_native.dbforpostgresql.v20220308preview as __v20220308preview
    v20220308preview = __v20220308preview
    import pulumi_azure_native.dbforpostgresql.v20220308privatepreview as __v20220308privatepreview
    v20220308privatepreview = __v20220308privatepreview
    import pulumi_azure_native.dbforpostgresql.v20221201 as __v20221201
    v20221201 = __v20221201
else:
    v20171201 = _utilities.lazy_import('pulumi_azure_native.dbforpostgresql.v20171201')
    v20171201preview = _utilities.lazy_import('pulumi_azure_native.dbforpostgresql.v20171201preview')
    v20180601 = _utilities.lazy_import('pulumi_azure_native.dbforpostgresql.v20180601')
    v20180601privatepreview = _utilities.lazy_import('pulumi_azure_native.dbforpostgresql.v20180601privatepreview')
    v20200101 = _utilities.lazy_import('pulumi_azure_native.dbforpostgresql.v20200101')
    v20200101privatepreview = _utilities.lazy_import('pulumi_azure_native.dbforpostgresql.v20200101privatepreview')
    v20200214preview = _utilities.lazy_import('pulumi_azure_native.dbforpostgresql.v20200214preview')
    v20200214privatepreview = _utilities.lazy_import('pulumi_azure_native.dbforpostgresql.v20200214privatepreview')
    v20201005privatepreview = _utilities.lazy_import('pulumi_azure_native.dbforpostgresql.v20201005privatepreview')
    v20201105preview = _utilities.lazy_import('pulumi_azure_native.dbforpostgresql.v20201105preview')
    v20210410privatepreview = _utilities.lazy_import('pulumi_azure_native.dbforpostgresql.v20210410privatepreview')
    v20210601 = _utilities.lazy_import('pulumi_azure_native.dbforpostgresql.v20210601')
    v20210601preview = _utilities.lazy_import('pulumi_azure_native.dbforpostgresql.v20210601preview')
    v20210615privatepreview = _utilities.lazy_import('pulumi_azure_native.dbforpostgresql.v20210615privatepreview')
    v20220120preview = _utilities.lazy_import('pulumi_azure_native.dbforpostgresql.v20220120preview')
    v20220308preview = _utilities.lazy_import('pulumi_azure_native.dbforpostgresql.v20220308preview')
    v20220308privatepreview = _utilities.lazy_import('pulumi_azure_native.dbforpostgresql.v20220308privatepreview')
    v20221201 = _utilities.lazy_import('pulumi_azure_native.dbforpostgresql.v20221201')

