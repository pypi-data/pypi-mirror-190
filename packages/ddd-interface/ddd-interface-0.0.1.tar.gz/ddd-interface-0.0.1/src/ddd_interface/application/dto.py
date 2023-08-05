from pydantic import BaseModel
from typing import List, Optional, Dict



class DatapipeServerInfoDTO(BaseModel):
    id: str
    secret: str
    endpoint: str


class DatapipeDataInfoDTO(BaseModel):
    bucket: str
    remote_path: str
    local_path: str
    timeout: int = 3


class ClusterConfigDataDTO(BaseModel):
    data_server: DatapipeServerInfoDTO
    data: List[DatapipeDataInfoDTO]


class ClusterConfigDTO(BaseModel):
    cluster_name: str
    region_id: str
    config_data: Optional[ClusterConfigDataDTO] = None
    entry_point: Optional[List[str]] = None
    timeout: int = 20


class BootstrapInfoDTO(BaseModel):
    cluster_config: ClusterConfigDTO
    template: str = 'normal'
    platform: str = 'aliyun'
    patch_setting: Dict