import argparse
import os

from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt


def main():
    parser = argparse.ArgumentParser(description="AI Code Assistant")
    parser.add_argument("user_prompt", type=str, help="Prompt to send to Gemini")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY environment variable not set")

    client = genai.Client(api_key=api_key)
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    if args.verbose:
        print(f"User prompt: {args.user_prompt}\n")

    generate_content(client, messages, args.verbose)


def generate_content(client, messages, verbose):
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=messages,
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            temperature=0) # temperature 0 for deterministic output, which is useful for testing and debugging
    )
    if not response.usage_metadata:
        raise RuntimeError("Gemini API response appears to be malformed")

    if verbose:
        print("Prompt tokens:", response.usage_metadata.prompt_token_count)
        print("Response tokens:", response.usage_metadata.candidates_token_count)

    print("Response:")
    print(response.text)


if __name__ == "__main__":
    main()

# import os
# import argparse
# from dotenv import load_dotenv
# from google import genai
# from google.genai import types


# load_dotenv()
# api_key = os.environ.get("GEMINI_API_KEY")

# if api_key is None:
#         ## raise RuntimeError
#         raise RuntimeError("GEMINI_API_KEY is not set in the environment variables.")

# client = genai.Client(api_key=api_key)

# def main():
#     print("Hello from aiagent!")
#     # user_prompt = "Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum."
#     parser = argparse.ArgumentParser(description="Aiagent")
#     parser.add_argument("user_prompt", type=str, help="The prompt to send to the Gemini API")
#     parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
#     args = parser.parse_args()
#     ## the generate_content method takes a list of Content objects, where each Content object has a role (either "user" or "assistant") and a list of Part objects, where each Part object has a text attribute that contains the text of the part. In this case, we are creating a single Content object with the role "user" and a single Part object with the text of the user prompt.
#     messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
#     response = client.models.generate_content(
#             model="gemini-2.5-flash", contents=messages
#         )
    
#     if response.usage_metadata is None:
#          raise RuntimeError("Usage metadata is not available in the response.")
#     if args.verbose:
#         print(f"User prompt: {args.user_prompt}")
#         print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
#         print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

#     ## the generate_content method returns a response object that contains the generated content in the text attribute
#     print(f'Response:\n{response.text}')


# if __name__ == "__main__":
#     main()