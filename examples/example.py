import base64
import os
import webbrowser
from typing import List

from floom import FloomClient
from dataclasses import dataclass


def run_simple_pipeline():
    floom_client = FloomClient(
        url="http://localhost:4050"
    )
    floom_response = floom_client.run(
        pipelineId="floom-simple-pipeline",
        prompt="List top 10 countries in the world, sorted by population."
    )

    if floom_response.success is False:
        print(f"Error: {floom_response.error.detail}")
    else:
        for content in floom_response.values:
            print(f"Response: ", content.value)


@dataclass
class Country:
    name: str = ""
    population: str = ""
    continent: str = ""


def run_object_response_pipeline():
    floom_client = FloomClient(
        url="http://localhost:4050"
    )
    floom_response = floom_client.run(
        prompt="Get largest country in the Asia",
        response_type=Country
    )

    if floom_response.success is False:
        print(f"Error: {floom_response.error.detail}")
    else:
        content = floom_response.values[0].value
        for country in content:
            print(f"Country: {country.name}, Population: {country.population}, Continent: {country.continent}")


def run_rag_pipeline():
    floom_client = FloomClient(
        url="http://localhost:4050"
    )
    floom_response = floom_client.run(
        pipeline_id="floom-docs-pipeline",
        prompt="Question about your document"
    )
    if floom_response.success is False:
        print(f"Error: {floom_response.error.detail}")
    else:
        for content in floom_response.values:
            print(f"Response: ", content.value)


def run_text_to_image_pipeline():
    floom_client = FloomClient(
        url="http://localhost:4050"
    )
    floom_response = floom_client.run(
        pipeline_id="floom-image-generator-pipeline",
        prompt="Group of people drinking coffee while camping in the ice cold forest, surrounded by snow."
    )

    if floom_response.success is False:
        print(f"Error: {floom_response.error.detail}")
    else:
        image_base_64 = floom_response.values[0].value
        print('Image preview:', image_base_64[:100], '...')

        image_path = "image.png"
        with open(image_path, "wb") as fh:
            fh.write(base64.b64decode(image_base_64))

        webbrowser.open(f"file://{os.path.abspath(image_path)}")


def run_text_to_speech_pipeline():
    floom_client = FloomClient(
        url="http://localhost:4050"
    )
    floom_response = floom_client.run(
        pipeline_id="floom-tts-pipeline",
        prompt="Why do birds suddenly appear every time you are near? Just like me, they long to be close to you."
    )

    if floom_response.success is False:
        print(f"Error: {floom_response.error.detail}")
    else:
        audio_base_64 = floom_response.values[0].value
        print('Audio preview:', audio_base_64[:100], '...')

        audio_path = "audio.mp3"
        with open(audio_path, "wb") as fh:
            fh.write(base64.b64decode(audio_base_64))

        webbrowser.open(f"file://{os.path.abspath(audio_path)}")


def main():
    print("Welcome to the Floom SDK demo.")
    while True:
        print("1. Simple Pipeline")
        print("2. Simple Pipeline (Response as Object)")
        print("3. RAG Pipeline (Docs)")
        print("4. Text to Image Pipeline")
        print("5. Text to Speech Pipeline")
        print("6. Exit")

        choice = input("Enter your choice (1-6): ").strip()

        if choice == '1':
            run_simple_pipeline()
        elif choice == '2':
            run_object_response_pipeline()
        elif choice == '3':
            run_rag_pipeline()
        elif choice == '4':
            run_text_to_image_pipeline()
        elif choice == '5':
            run_text_to_speech_pipeline()
        elif choice == '6':
            print("Thank you for using the Floom SDK demo. Goodbye!")
            break
        else:
            print("Invalid choice, please select 1-5.")


if __name__ == '__main__':
    main()
