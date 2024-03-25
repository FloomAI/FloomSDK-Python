import json
from typing import Optional, List, Dict, Any
from enum import Enum

import requests


class DataType(Enum):
    String = 1
    Image = 2
    Audio = 3
    JsonObject = 4


class ResponseValue:
    def __init__(self, type_: DataType, format_: str, value: Any):  # Adjusted value type hint to Any
        self.type = type_
        self.format = format_
        self.value = value

    @classmethod
    def from_dict(cls, data: Dict) -> 'ResponseValue':
        type_enum = DataType(data['type'])
        parsed_value = data['value']
        if type_enum == DataType.JsonObject:
            parsed_value = json.loads(data['value']) if isinstance(data['value'], str) else data['value']
        return cls(type_=type_enum, format_=data['format'], value=parsed_value)


class FloomError:
    def __init__(self, status: Optional[int] = None, title: Optional[str] = None, detail: Optional[str] = None):
        self.status = status
        self.title = title
        self.detail = detail

    @classmethod
    def from_http_error(cls, error: requests.HTTPError):
        try:
            error_info = error.response.json()
            return cls(
                status=error.response.status_code,
                title=error_info.get('title', 'HTTP Error'),
                detail=error_info.get('detail', str(error))
            )
        except ValueError:
            # Fallback in case the response is not in JSON format
            return cls(status=error.response.status_code, title="HTTP Error", detail=str(error))

    @classmethod
    def from_exception(cls, exception: Exception):
        return cls(
            status=500,
            title="Internal Server Error",
            detail=str(exception)
        )

    @classmethod
    def from_dict(cls, data: Dict):
        return cls(
            status=data.get('status'),
            title=data.get('title'),
            detail=data.get('detail')
        )


class FloomResponse:
    def __init__(self, values: Optional[List[ResponseValue]] = None, code: Optional[int] = None,
                 message: Optional[str] = None, error: Optional[FloomError] = None, success = False):
        self.values = values
        self.code = code
        self.message = message
        self.error = error
        self.success = success

    @classmethod
    def from_dict(cls, data: Dict):
        error = None
        if 'status' in data and 'title' in data and 'detail' in data:
            error = FloomError.from_dict(data)
        return cls(
            success=data.get('success', False),
            values=[ResponseValue.from_dict(val) for val in data.get('value', [])] if 'value' in data else None,
            code=data.get('code'),
            message=data.get('message'),
            error=error  # Pass the error object if any
        )
