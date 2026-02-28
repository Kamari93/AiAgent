import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

if api_key is None:
        ## raise RuntimeError
        raise RuntimeError("GEMINI_API_KEY is not set in the environment variables.")

client = genai.Client(api_key=api_key)


def main():
    print("Hello from aiagent!")
    user_prompt = "Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum."
    response = client.models.generate_content(
            model="gemini-2.5-flash", contents=user_prompt
        )
    
    if response.usage_metadata is None:
         raise RuntimeError("Usage metadata is not available in the response.")
    print(f"User Prompt: {user_prompt}")
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

    ## the generate_content method returns a response object that contains the generated content in the text attribute
    print(f'Response:\n{response.text}')


if __name__ == "__main__":
    main()
