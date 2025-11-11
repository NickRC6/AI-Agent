import os
import sys
from config import system_prompt
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_file_content import get_file_content
from functions.get_files_info import schema_get_files_info
from functions.get_files_info import available_functions

load_dotenv()
api_key = os.environ.get('GEMINI_API_KEY')
client = genai.Client(api_key=api_key)


def main():
    verbose = False
    if "--verbose" in sys.argv:
        verbose = True
        sys.argv.remove("--verbose")

    if len(sys.argv) > 1:
        arg = sys.argv[1]
    else:
        arg = sys.stdin.read().strip()

    if not arg:
        print("Error: No argument provided.")
        sys.exit(1)

    messages = [
    types.Content(role="user", parts=[types.Part(text=arg)]),
]
    
    response = client.models.generate_content(
    model="gemini-2.0-flash-001",
    contents=messages,
    config=types.GenerateContentConfig(
    tools=[available_functions], system_instruction=system_prompt
)
)
    prompt_tokens = None
    response_tokens = None

    if hasattr(response, "metadata") and hasattr(response.metadata, "token_metadata"):
        tokens = response.metadata.token_metadata
        prompt_tokens = getattr(tokens, "input_token_count", None)
        response_tokens = getattr(tokens, "output_token_count", None)

    if response.function_calls:
        for part in response.function_calls:
            print(f"Calling function: {part.name}({part.args})")
    else:
        print(response.text)

    if verbose:
        print(f"User prompt: {arg}")
        if prompt_tokens is not None and response_tokens is not None:
            print(f"Prompt tokens: {prompt_tokens}")
            print(f"Response tokens: {response_tokens}")
        else:
            print("Token usage data not available for this response.")

if __name__ == "__main__":
    main()
