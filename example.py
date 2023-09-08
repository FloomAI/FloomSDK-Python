from FloomClient import FloomClient, DataTransferType
import asyncio

# Since the run method isn't actually asynchronous in the Python version, you don't have to use asyncio in this example.
# I've kept it here just in case you want to use asyncio for other things in your application.

async def main():
    floom_client = FloomClient(
        endpoint="http://localhost:4050",
        api_key="Vcm6RReBMLQa0h2fUidOC7SLmh356uHH"
    )
    
    x = floom_client.run(
        pipelineId="docs-pipeline",
        input="How do I reset the oil alert in my dashboard?"
    )

    # Do something with the FloomResponse object `x`
    print(x.values[0]['value'])

    # ... and so on

if __name__ == "__main__":
    asyncio.run(main())
