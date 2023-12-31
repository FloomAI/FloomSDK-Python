from typing import Optional, List, Dict
from enum import Enum

class DataType(Enum):
    String = 1
    Image = 2
    Video = 3
    Audio = 4

class ResponseValue:
    def __init__(self, type_: DataType, format_: str, value: str, b64: str, url: str):
        self.type = type_
        self.format = format_
        self.value = value
        self.b64 = b64
        self.url = url

    @classmethod
    def from_dict(cls, data: Dict):
        return cls(
            type_=DataType(data['type']),
            format_=data['format'],
            value=data['value'],
            b64=data['b64'],
            url=data['url']
        )

class FireResponseTokenUsage:
    def __init__(self, processing_tokens: int, prompt_tokens: int, total_tokens: int):
        self.processing_tokens = processing_tokens
        self.prompt_tokens = prompt_tokens
        self.total_tokens = total_tokens

    @classmethod
    def from_dict(cls, data: Dict):
        return cls(
            processing_tokens=data['processingTokens'],
            prompt_tokens=data['promptTokens'],
            total_tokens=data['totalTokens']
        )

class FloomResponse:
    def __init__(self, messageId: str, chatId: str, values: List[ResponseValue], processingTime: int, tokenUsage: FireResponseTokenUsage):
        self.messageId = messageId
        self.chatId = chatId
        self.values = values
        self.processingTime = processingTime
        self.tokenUsage = tokenUsage

    @classmethod
    def from_dict(cls, data: Dict):
        return cls(
            messageId=data['messageId'],
            chatId=data['chatId'],
            values=[ResponseValue.from_dict(val) for val in data['values']],
            processingTime=data['processingTime'],
            tokenUsage=FireResponseTokenUsage.from_dict(data['tokenUsage'])
        )
