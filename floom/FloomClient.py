# FloomClient.py

import json
import requests

from floom.FloomResponse import FloomResponse
from floom.FloomRequest import DataTransferType, FloomRequest


class FloomClient:
    def __init__(self, endpoint: str, api_key: str):
        self._url = endpoint
        self._api_key = api_key

    def run(self, pipelineId: str, chatId: str = "", prompt: str = "", variables: dict = None,
            data_transfer: DataTransferType = DataTransferType.Base64):  # Changed BASE64 to Base64

        headers = {
            'Api-Key': f'{self._api_key}',
            'Content-Type': 'application/json'  # Explicitly set the Content-Type header to 'application/json'
        }

        url = f"{self._url}/v1/Pipelines/Run"

        floom_request = FloomRequest(
            pipelineId=pipelineId,
            chatId=chatId,
            prompt=prompt,
            variables=variables,
            data_transfer=data_transfer
        )

        # Convert enum to integer
        request_dict = floom_request.__dict__
        request_dict["data_transfer"] = request_dict["data_transfer"].value

        payload = json.dumps(request_dict)

        try:
            response = requests.post(url, headers=headers, data=payload)
        except Exception as e:
            error_response = FloomResponse(code=500, message=str(e))
            return error_response

        if response.status_code != 200:
            error_response = FloomResponse(code=response.status_code, message=response.text)
            return error_response

        floom_response = FloomResponse(**response.json())

        return floom_response
