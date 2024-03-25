from enum import Enum
from typing import Dict, Optional, Union, List, Any


class FloomRequest:
    def __init__(
            self,
            pipelineId: str,
            prompt: str = "",
            variables: Optional[Dict[str, str]] = None,
            responseType: Union[dict, List[dict], str, None] = None
    ):
        self.pipelineId = pipelineId
        self.prompt = prompt
        self.variables = variables or {}
        self.responseType = responseType


class FloomJSONKeys:
    VALUE = "value"
    TYPE = "type"
    FORMAT = "format"
    PIPELINE_ID = "pipelineId"
    PROMPT = "prompt"
    VARIABLES = "variables"
    RESPONSE_TYPE = "responseType"
    SUCCESS = "success"


class FloomRequestData:
    @staticmethod
    def build(pipelineId: str, prompt: str, variables: Dict[str, Any],
              response_type_example: Union[Dict[str, Any], List[Dict[str, Any]], None]) -> Dict[str, Any]:
        """Constructs the request payload for the Floom API call."""
        request_data = {
            FloomJSONKeys.PIPELINE_ID: pipelineId,
            FloomJSONKeys.PROMPT: prompt,
            FloomJSONKeys.VARIABLES: variables or {}
        }
        if response_type_example is not None:
            request_data[FloomJSONKeys.RESPONSE_TYPE] = response_type_example
        return request_data
