
  
# FloomSDK for Python  
  
FloomSDK is a comprehensive Python client designed to facilitate the integration of Floom's Generative AI capabilities into your Python applications. This SDK offers a straightforward interface for making requests to Floom's API, allowing developers to seamlessly incorporate advanced AI features into their projects while abstracting away the complexity of direct API calls.  
  
## Features  
  
- **Simplified Integration**: Effortlessly integrate Floom's Generative AI functionalities into your Python applications.  
- **Python 3 Support**: Fully supports Python 3, ensuring compatibility with modern Python environments.  
- **Versatile**: Suitable for use in a wide range of Python projects, from simple scripts to complex applications.  
  
## Getting Started  
  
### Prerequisites  
  
- Python 3.6 or newer  
- An API key from Floom  
  
### Installation  
  
Install Floom SDK using pip:  
  
```bash  python3 -m pip install floom```  
  
### Basic Usage  
  
The Floom SDK for Python provides various functionalities to integrate Generative AI capabilities into your applications effortlessly. Here is an overview of the options available in the examples/example.py file, illustrating the SDK's versatility in handling different types of AI tasks:  
  
#### Running a Simple Pipeline
Send a textual prompt to a predefined pipeline and receive a textual response. Ideal for straightforward AI interactions:  
```python  
from floom import FloomClient  
  
def run_simple_pipeline():  
	floom_client = FloomClient(
		url="http://localhost:4050",
		api_key="Vcm6RReBMLQa0h2fUidOC7SLmh356uHH")
			
	floom_response = floom_client.run(
		pipelineId="floom-simple-pipeline",
		prompt="List top 10 countries in the world.")

	 if floom_response.success is False:
		 print(f"Error: {floom_response.error.detail}")
	 else:
		 for content in floom_response.values:
			 print(f"Response: ", content.value)
			 
```  
  


#### Running a Pipeline with Object Response
Interpret the response as a list of objects, each representing structured information. Useful for applications requiring object-oriented responses. Note the `@dataclass` annotation for the response object class:

```python  
from floom import FloomClient
from dataclasses import dataclass
from typing import List

@dataclass
class Country:
    name: str = ""
    population: str = ""
    continent: str = ""

def run_object_response_pipeline():
    floom_client = FloomClient(
        url="http://localhost:4050",
        api_key="Vcm6RReBMLQa0h2fUidOC7SLmh356uHH")
    
    floom_response = floom_client.run(
        pipelineId="floom-object-response-pipeline",
        prompt="List top 10 countries in the world, sorted by population.",
        response_type=List[Country])

    if floom_response.success is False:
        print(f"Error: {floom_response.error.detail}")
    else:
        content = floom_response.values[0].value
        for country in content:
            print(f"Country: {country.name}, Population: {country.population}, Continent: {country.continent}")

```

#### Running a RAG Pipeline
Generate detailed, context-aware responses based on a corpus of documents:
```python  
`from floom import FloomClient

def run_rag_pipeline():
    floom_client = FloomClient(
        url="http://localhost:4050",
        api_key="Vcm6RReBMLQa0h2fUidOC7SLmh356uHH")
    
    floom_response = floom_client.run(
        pipelineId="floom-docs-pipeline",
        prompt="Question about your document.")

    if floom_response.success is False:
        print(f"Error: {floom_response.error.detail}")
    else:
        for content in floom_response.values:
            print(f"Response: ", content.value)`
```



#### Running a Text to image Pipeline
Convert textual descriptions into images. Demonstrates decoding the base64 encoded image and displaying it:

```python  
from floom import FloomClient
import base64
import webbrowser
import os

def run_text_to_image_pipeline():
    floom_client = FloomClient(
        url="http://localhost:4050",
        api_key="Vcm6RReBMLQa0h2fUidOC7SLmh356uHH")
            
    floom_response = floom_client.run(
        pipelineId="floom-image-generator-pipeline",
        prompt="Group of people drinking coffee while camping in the ice cold forest, surrounded by snow.")

    if floom_response.success is False:
        print(f"Error: {floom_response.error.detail}")
    else:
        image_base_64 = floom_response.values[0].value
        print('Image preview:', image_base_64[:100], '...')

        image_path = "image.png"
        with open(image_path, "wb") as fh:
            fh.write(base64.b64decode(image_base_64))

        webbrowser.open(f"file://{os.path.abspath(image_path)}")
```

#### Running a Text to Speech Pipeline
This functionality converts text into speech, showcasing how to handle and play the generated audio content:

```python  
from floom import FloomClient
import base64
import webbrowser
import os

def run_text_to_speech_pipeline():
    floom_client = FloomClient(
        url="http://localhost:4050",
        api_key="Vcm6RReBMLQa0h2fUidOC7SLmh356uHH")
    
    floom_response = floom_client.run(
        pipelineId="floom-tts-pipeline",
        prompt="Why do birds suddenly appear every time you are near? Just like me, they long to be close to you.")

    if floom_response.success is False:
        print(f"Error: {floom_response.error.detail}")
    else:
        audio_base_64 = floom_response.values[0].value
        print('Audio preview:', audio_base_64[:100], '...')

        audio_path = "audio.mp3"
        with open(audio_path, "wb") as fh:
            fh.write(base64.b64decode(audio_base_64))

        webbrowser.open(f"file://{os.path.abspath(audio_path)}")

```


## Documentation  
  
For comprehensive documentation and API references, please visit [Floom Documentation](https://floom.ai/docs).  
  
## Support and Contributions  
  
Should you encounter any issues or if you need further assistance, feel free to open an issue on our [GitHub issues page](https://github.com/FloomAI/FloomSDK-Python/issues).  
  
We warmly welcome contributions! If you're interested in contributing, please fork the repository, make your changes, and submit a pull request.  
  
## License  
  
FloomSDK for Python is distributed under the [MIT license](./LICENSE).