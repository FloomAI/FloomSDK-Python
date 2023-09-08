from enum import Enum
from typing import Dict, Optional

class DataTransferType(Enum):
    Base64 = 1

class FloomRequest:
    def __init__(
        self,
        pipelineId: str,
        chatId: str = "",
        input: str = "",
        variables: Optional[Dict[str, str]] = None,
        data_transfer: DataTransferType = DataTransferType.Base64,
    ):
        self.pipelineId = pipelineId
        self.chatId = chatId
        self.input = input
        self.variables = variables or {}
        self.data_transfer = data_transfer
