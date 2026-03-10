import argparse
import os

from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from call_function import available_functions, call_function

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
            tools=[available_functions], # make the functions defined in call_function.py available for the LLM to call
            system_instruction=system_prompt,
            temperature=0) # temperature 0 for deterministic output, which is useful for testing and debugging
    )
    if not response.usage_metadata:
        raise RuntimeError("Gemini API response appears to be malformed")

    if verbose:
        print("Prompt tokens:", response.usage_metadata.prompt_token_count)
        print("Response tokens:", response.usage_metadata.candidates_token_count)

    if response.function_calls:
        function_result_list = []
        # Even if Gemini usually returns one, you should still loop. This is because the LLM could decide to call multiple functions in one response, and if you only handle the first one you would miss the others and potentially lose important information or functionality.
        for function_call in response.function_calls:
            function_call_result = call_function(function_call, verbose)
            validate_function_result(function_call_result)
            function_result_list.append(function_call_result.parts[0])

            if verbose:
                print(f"-> {function_call_result.parts[0].function_response.response}")

    else:
        print("Response:")
        print(response.text)

# helper function to validate the structure of the function call result returned from call_function before we try to access its content, to avoid runtime errors due to malformed function call results. This is especially important because if the LLM is able to call functions, it could potentially return malformed results that don't match our expected structure, and we want to catch those cases gracefully.
def validate_function_result(result):
    if (
        not result
        or not result.parts
        or not result.parts[0].function_response
        or not result.parts[0].function_response.response
    ):
        raise Exception("Function call result appears to be malformed")

if __name__ == "__main__":
    main()
