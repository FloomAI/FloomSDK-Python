
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

```bash
python3 -m pip install floom
```

### Basic Usage

Below is a quick example to get you started with the SDK in your Python project:

```python
from floom.FloomClient import FloomClient

async def main():
    floom_client = FloomClient(
        url="http://localhost:4050",
        api_key="api_key_here"
    )

    floom_response = floom_client.run(
        pipelineId="simple-pipeline",
        prompt="Who was the first president of the US?"
    )

    if floom_response.code is not None:
        print(f"Error: {floom_response.message}")
    else:
        print(floom_response.values[0]['value'])

if __name__ == "__main__":
    main()
```

## Documentation

For comprehensive documentation and API references, please visit [Floom Documentation](https://floom.ai/docs).

## Support and Contributions

Should you encounter any issues or if you need further assistance, feel free to open an issue on our [GitHub issues page](https://github.com/FloomAI/FloomSDK-Python/issues).

We warmly welcome contributions! If you're interested in contributing, please fork the repository, make your changes, and submit a pull request.

## License

FloomSDK for Python is distributed under the [MIT license](./LICENSE).
