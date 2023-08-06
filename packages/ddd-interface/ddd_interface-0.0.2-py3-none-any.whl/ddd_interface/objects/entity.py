import datetime
from typing import List, Optional, Dict, Tuple, Union
from ..domain.entity import Entity
from .value_obj import (
    UDict,
    UInt,
    UStr
)



class DatapipeServerInfo(Entity):
    def __init__(
        self,
        id: UStr,
        secret: UStr,
        endpoint: UStr
    ) -> None:
        self.id = id
        self.secret = secret
        self.endpoint = endpoint



class DatapipeDataInfo(Entity):
    def __init__(
        self,
        bucket: UStr,
        remote_path: UStr,
        local_path: UStr,
        timeout: UInt = 3
    ) -> None:
        self.bucket = bucket
        self.remote_path = remote_path
        self.local_path = local_path
        self.timeout = timeout



class ClusterConfigData(Entity):
    def __init__(
        self,
        data_server: DatapipeServerInfo,
        data: List[DatapipeDataInfo]
    ) -> None:
        self.data_server = data_server
        self.data = data



class ClusterConfig(Entity):
    def __init__(
        self,
        cluster_name: UStr,
        region_id: UStr,
        config_data: Optional[ClusterConfigData] = None,
        entry_point: Optional[List[UStr]] = None,
        timeout: UInt = 20
    ) -> None:
        self.cluster_name = cluster_name
        self.region_id = region_id
        self.config_data = config_data
        self.entry_point = entry_point
        self.timeout = timeout



class Bootstrap(Entity):
    def __init__(
        self,
        cluster_config: ClusterConfig,
        template: UStr = 'normal',
        platform: UStr = 'aliyun',
        patch_setting: Optional[UDict] = None
    ) -> None:
        self.cluster_config = cluster_config
        self.template = template
        self.platform = platform
        self.patch_setting = patch_setting