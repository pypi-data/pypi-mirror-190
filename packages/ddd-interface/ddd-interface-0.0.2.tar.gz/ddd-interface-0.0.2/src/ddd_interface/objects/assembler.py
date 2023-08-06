from typing import List, Optional, Dict, Tuple, Union
from ..application.assembler import Assembler
from .entity import (
    Bootstrap,
    ClusterConfig,
    ClusterConfigData,
    DatapipeDataInfo,
    DatapipeServerInfo
)
from .dto import (
    BootstrapDTO,
    ClusterConfigDTO,
    ClusterConfigDataDTO,
    DatapipeDataInfoDTO,
    DatapipeServerInfoDTO
)
from .value_obj import (
    UDict,
    UInt,
    UStr
)



class DatapipeServerInfoAssembler(Assembler):
    def to_entity(self, dto: DatapipeServerInfoDTO):
        return DatapipeServerInfo(
            id = UStr(dto.id),
            secret = UStr(dto.secret),
            endpoint = UStr(dto.endpoint)
        )
    def to_dto(self, x:DatapipeServerInfo):
        return DatapipeServerInfoDTO(
            id = x.id.get_value(),
            secret = x.secret.get_value(),
            endpoint = x.endpoint.get_value()
        )
datapipe_server_info_assembler=DatapipeServerInfoAssembler()



class DatapipeDataInfoAssembler(Assembler):
    def to_entity(self, dto: DatapipeDataInfoDTO):
        return DatapipeDataInfo(
            bucket = UStr(dto.bucket),
            remote_path = UStr(dto.remote_path),
            local_path = UStr(dto.local_path),
            timeout = UInt(dto.timeout)
        )
    def to_dto(self, x:DatapipeDataInfo):
        return DatapipeDataInfoDTO(
            bucket = x.bucket.get_value(),
            remote_path = x.remote_path.get_value(),
            local_path = x.local_path.get_value(),
            timeout = x.timeout.get_value()
        )
datapipe_data_info_assembler=DatapipeDataInfoAssembler()



class ClusterConfigDataAssembler(Assembler):
    def to_entity(self, dto: ClusterConfigDataDTO):
        return ClusterConfigData(
            data_server = datapipe_server_info_assembler.to_entity(dto.data_server),
            data = [datapipe_data_info_assembler.to_entity(m) for m in dto.data]
        )
    def to_dto(self, x:ClusterConfigData):
        return ClusterConfigDataDTO(
            data_server = datapipe_server_info_assembler.to_do(x.data_server),
            data = [datapipe_data_info_assembler.to_do(m) for m in x.data]
        )
cluster_config_data_assembler=ClusterConfigDataAssembler()



class ClusterConfigAssembler(Assembler):
    def to_entity(self, dto: ClusterConfigDTO):
        return ClusterConfig(
            cluster_name = UStr(dto.cluster_name),
            region_id = UStr(dto.region_id),
            config_data = None if dto.config_data is None else cluster_config_data_assembler.to_entity(dto.config_data),
            entry_point = None if dto.entry_point is None else [UStr(m) for m in dto.entry_point],
            timeout = UInt(dto.timeout)
        )
    def to_dto(self, x:ClusterConfig):
        return ClusterConfigDTO(
            cluster_name = x.cluster_name.get_value(),
            region_id = x.region_id.get_value(),
            config_data = None if x.config_data is None else cluster_config_data_assembler.to_do(x.config_data),
            entry_point = None if x.entry_point is None else [m.get_value() for m in x.entry_point],
            timeout = x.timeout.get_value()
        )
cluster_config_assembler=ClusterConfigAssembler()



class BootstrapAssembler(Assembler):
    def to_entity(self, dto: BootstrapDTO):
        return Bootstrap(
            cluster_config = cluster_config_assembler.to_entity(dto.cluster_config),
            template = UStr(dto.template),
            platform = UStr(dto.platform),
            patch_setting = None if dto.patch_setting is None else UDict(dto.patch_setting)
        )
    def to_dto(self, x:Bootstrap):
        return BootstrapDTO(
            cluster_config = cluster_config_assembler.to_do(x.cluster_config),
            template = x.template.get_value(),
            platform = x.platform.get_value(),
            patch_setting = None if x.patch_setting is None else x.patch_setting.get_value()
        )
bootstrap_assembler=BootstrapAssembler()
