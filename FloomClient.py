# FloomClient.py

import json
import requests

from FloomRequest import FloomRequest, DataTransferType
from FloomResponse import FloomResponse

class FloomClient:
    def __init__(self, endpoint: str, api_key: str):
        self._url = endpoint
        self._api_key = api_key

    def run(self, pipelineId: str, chatId: str = "", input: str = "", variables: dict = None, data_transfer: DataTransferType = DataTransferType.Base64):  # Changed BASE64 to Base64

        headers = {
            'Api-Key': f'{self._api_key}',
            'Content-Type': 'application/json'  # Explicitly set the Content-Type header to 'application/json'
        }
        

        url = f"{self._url}/v1/Pipelines/Run"

        floom_request = FloomRequest(
            pipelineId=pipelineId,
            chatId=chatId,
            input=input,
            variables=variables,
            data_transfer=data_transfer
        )

        # Convert enum to integer
        request_dict = floom_request.__dict__
        request_dict["data_transfer"] = request_dict["data_transfer"].value

        payload = json.dumps(request_dict)
        
        #print(f"Payload: {payload}")

        response = requests.post(url, headers=headers, data=payload)
        response.raise_for_status()
        
        #print(f"Response: {response}")
        
        floom_response = FloomResponse(**response.json())
        
        return floom_response
