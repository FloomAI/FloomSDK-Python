# client.py

import json
import requests

from floom.models import FloomResponse, FloomError, DataType, ResponseValue

from typing import Type, Union, List, get_args, get_origin, Any, Dict
from typing import get_type_hints

from floom.request import FloomRequestData, FloomJSONKeys


class FloomClient:
    API_VERSION = "v1"
    RUN_PIPELINE_ENDPOINT = "/Pipelines/Run"
    HEADERS = {'Content-Type': 'application/json'}

    """
    A client for interacting with the Floom API.
    """

    def __init__(self, url: str, api_key: str = "", verbose_debugging: bool = False):
        """
        Initializes the FloomClient with API URL and key.

        :param url: Base URL for the Floom API.
        :param api_key: API key for authenticating requests.
        """
        self._url = url.rstrip('/')  # Remove trailing slash if it exists
        self._api_key = api_key
        self.verbose_debugging = verbose_debugging

    def _log(self, message: str):
        if self.verbose_debugging:
            print(message)

    @property
    def _headers(self) -> Dict[str, str]:
        return {'Api-Key': self._api_key, **self.HEADERS}

    def _get_endpoint_url(self, endpoint: str) -> str:
        return f"{self._url}/{self.API_VERSION}{endpoint}"

    def run(self, response_type: Union[Type, List[Type]] = None, pipeline_id: str = "", prompt: str = "",
            variables: dict = None) -> FloomResponse:
        """
        Executes a pipeline and returns a FloomResponse.

        :param response_type: The expected type of the response, used for dynamic instance creation.
        :param pipeline_id: The ID of the pipeline to be run.
        :param prompt: The input prompt for the pipeline.
        :param variables: Additional variables for the pipeline run.
        :return: The processed response, either as a FloomResponse or the instantiated response_type.
        """
        self._log(f"Running pipeline with ID '{pipeline_id}' and prompt '{prompt}'")

        # If self._url contains "pipeline.floom.ai" and api_key is not set, raise an error
        if "pipeline.floom.ai" in self._url and not self._api_key:
            self._log("API key is required for the Floom instance at 'pipeline.floom.ai'")
            return FloomResponse(error=FloomError(status=401, title="Unauthorized", detail="API key is required for "
                                                                                           "the "
                                                                                           "Floom instance at " + self._url))
        # Preparing request payload
        response_type_json_example = self.generate_response_type_example(response_type) if response_type else None
        floom_request_data = FloomRequestData.build(pipeline_id, prompt, variables, response_type_json_example)

        payload = json.dumps(floom_request_data)
        # Sending request
        try:
            response = requests.post(self._get_endpoint_url(self.RUN_PIPELINE_ENDPOINT), headers=self._headers,
                                     data=payload)
            response.raise_for_status()
            response_json = response.json()
            self._log("Successfully received response from Floom API")
            return self._process_response(response_json, response_type)
        except requests.ConnectionError:
            self._log("Failed to establish a new connection. Make sure the Floom instance is running.")
            return FloomResponse(error=FloomError(status=503, title="Service Unavailable", detail="Failed to "
                                                                                                  "establish a new "
                                                                                                  "connection. Make "
                                                                                                  "sure the Floom "
                                                                                                  "instance is "
                                                                                                  "running."))
        except requests.HTTPError as e:
            self._log(f"HTTP error occurred: {e}")
            return FloomResponse(error=FloomError.from_http_error(e))
        except Exception as e:
            self._log(f"Unexpected error occurred: {e}")
            return FloomResponse(error=FloomError.from_exception(e))

    def _process_response(self, response_json: Dict[str, Any], response_type: Union[Type, List[Type]]) -> FloomResponse:
        if response_json.get(FloomJSONKeys.SUCCESS) and FloomJSONKeys.VALUE in response_json:
            response_value = response_json[FloomJSONKeys.VALUE]
            if response_value[FloomJSONKeys.TYPE] == DataType.JsonObject.value:
                instantiated_objects = self._process_json_object_response(response_value[FloomJSONKeys.VALUE],
                                                                          response_type)
                value = ResponseValue(type_=DataType(response_value[FloomJSONKeys.TYPE]),
                                      format_=response_value[FloomJSONKeys.FORMAT],
                                      value=instantiated_objects)
                return FloomResponse(values=[value], success=response_json[FloomJSONKeys.SUCCESS])
            elif response_value[FloomJSONKeys.TYPE] in {DataType.String.value, DataType.Image.value,
                                                        DataType.Audio.value}:
                value = ResponseValue(
                    type_=DataType(response_value[FloomJSONKeys.TYPE]),
                    format_=response_value[FloomJSONKeys.FORMAT],
                    value=response_value[FloomJSONKeys.VALUE]
                )
                return FloomResponse(values=[value], success=response_json[FloomJSONKeys.SUCCESS])

        return FloomResponse.from_dict(response_json)

    def _process_json_object_response(self, data: Any, response_type: Union[Type, List[Type]]) -> Union[
        object, List[object]]:
        """
        Processes the JSON object response based on the provided response_type.

        :param data: The JSON object or array of JSON objects from the response.
        :param response_type: The expected type of the response for instantiation.
        :return: An instance or list of instances of response_type based on the provided data.
        """
        origin = get_origin(response_type)
        if origin is list:
            element_type = get_args(response_type)[0]
            return [self.create_instance_of_type(element_type, item) for item in data]
        else:
            return [self.create_instance_of_type(response_type, item) for item in data]

    @staticmethod
    def load_response_from_file(file_path: str) -> dict:
        """
        Load the response from a given file path and return it as a dictionary.

        :param file_path: The path to the file containing the JSON response.
        :return: The JSON response as a dictionary.
        """
        with open(file_path, 'r') as file:
            data = json.load(file)
        return data

    def create_instance_of_type(self, response_type: Union[Type, List[Type]], data: dict) -> object:
        """
        Dynamically create an instance of a given type or a list of instances if the type is a list type.
        """
        origin = get_origin(response_type)
        if origin is list:
            # It's a list type, so get the element type and create a list of instances
            element_type = get_args(response_type)[0]
            return [self.create_instance_of_type(element_type, item) for item in data]
        else:
            # It's a single object, instantiate it directly
            if isinstance(data, dict):
                return response_type(**data)  # Assuming `response_type` is a class that can be instantiated like this
            return data  # Return the data directly if it's not a dict

    def generate_response_type_example(self, response_type: Union[Type, List[Type]]) -> Union[dict, List[dict]]:
        """
        Generates a JSON example string for the given response_type.
        Handles both direct class types and lists of a class.
        """
        if hasattr(response_type, '__origin__') and response_type.__origin__ == list:
            # If it's a list type, generate example for the element type and wrap it in a list
            element_type = response_type.__args__[0]
            example = [self.generate_response_type_example_for_class(element_type)]
        else:
            # Otherwise, directly generate the example for the class
            example = self.generate_response_type_example_for_class(response_type)

        return example

    @staticmethod
    def generate_response_type_example_for_class(cls: Type) -> dict:
        """
        Generates a dictionary with example values based on type annotations.
        This function handles basic types and defaults to a generic placeholder for unsupported types.
        """
        example = {}
        for field, field_type in get_type_hints(cls).items():
            if field_type == int:
                example[field] = 0
            elif field_type == str:
                example[field] = f"{field}.example"
            else:
                example[field] = f"Unsupported type ({field_type})"
        return example
