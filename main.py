import os
import sys
from config import system_prompt
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info, get_files_info
from functions.get_file_content import schema_get_file_content, get_file_content
from functions.write_file import schema_write_file, write_file
from functions.run_python_file import schema_run_python_file, run_python_file
from functions.call_function import call_function

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_write_file,
        schema_run_python_file,
    ]
)

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)


def main():
    verbose = "--verbose" in sys.argv
    if verbose:
        sys.argv.remove("--verbose")

    arg = sys.argv[1] if len(sys.argv) > 1 else sys.stdin.read().strip()

    if not arg:
        print("Error: No argument provided.")
        sys.exit(1)

    messages = [types.Content(role="user", parts=[types.Part(text=arg)])]

    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=system_prompt,
        ),
    )

    if response.function_calls:
        for part in response.function_calls:
            function_call_result = call_function(part, verbose=verbose)
            if not hasattr(function_call_result.parts[0], "function_response"):
                raise RuntimeError("Fatal: function call result missing function_response")
    else:
        if arg.startswith("run ") and arg.endswith(".py"):
            inferred_call = {"file_path": arg[4:].strip(), "args": []}
            print(f"Calling function: run_python_file({inferred_call})")
            run_python_file(os.getcwd(), **inferred_call)
        elif response.text:
            print(response.text)

    if verbose:
        print(f"User prompt: {arg}")
        if hasattr(response, "metadata") and hasattr(response.metadata, "token_metadata"):
            tokens = response.metadata.token_metadata
            print(
                f"Prompt tokens: {getattr(tokens, 'input_token_count', None)}\n"
                f"Response tokens: {getattr(tokens, 'output_token_count', None)}"
            )
        else:
            print("Token usage data not available for this response.")


if __name__ == "__main__":
    main()