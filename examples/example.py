from floom.FloomClient import FloomClient
import asyncio


async def main():
    floom_client = FloomClient(
        endpoint="http://localhost:4050",
        api_key="api_key_here"
    )

    floom_response = floom_client.run(
        pipelineId="simple-pipeline",
        prompt="How do I reset the oil alert in my dashboard?"
    )

    if floom_response.code is not None:
        print(f"Error: {floom_response.message}")
    else:
        print(floom_response.values[0]['value'])


if __name__ == "__main__":
    asyncio.run(main())
