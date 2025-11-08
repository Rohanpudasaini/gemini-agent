import argparse
import os
import sys

from dotenv import load_dotenv

# from google import genai
from google.genai import Client, types


def parse_arguments():
    parser = argparse.ArgumentParser(description="Simple Gemini AI Agent")
    parser.add_argument(
        "positional_message", nargs="?", help="Message to send to the AI"
    )

    parser.add_argument(
        "--message", "-m", type=str, help="The message to send to the Gemini AI model"
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Enable verbose output"
    )

    args = parser.parse_args()
    message = args.message or args.positional_message
    return args, message


def main():
    args, message = parse_arguments()
    is_verbose = args.verbose
    prompt = message

    if not prompt:
        sys.exit(
            "Please provide a message via a positional argument (as the first argument, without any prefix), or using `--message <your_message>` or `-m <your_message>`."
        )
    load_dotenv()

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        sys.exit(
            "Error: GEMINI_API_KEY environment variable is not set. Please set it to your Gemini API key."
        )

    client = Client(api_key=api_key)

    messages = [types.Content(role="user", parts=[types.Part(text=prompt)])]

    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
    )
    if is_verbose:
        print("User Prompt:", prompt)

    print("Response:", response.text)
    if not response.usage_metadata:
        print("Warning: Response is missing usage metadata.")
    elif is_verbose:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")


if __name__ == "__main__":
    main()
