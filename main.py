import os
import sys
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

    for i in range(20):  
        try:
            response = client.models.generate_content(
                model="gemini-2.0-flash-001",
                contents=messages,
                config=types.GenerateContentConfig(
                    tools=[available_functions],
                    system_instruction=system_prompt,
                    temperature=0, 
                ),
            )

            did_call_function = False

            for candidate in response.candidates:
                messages.append(candidate.content)
                for part in candidate.content.parts:
                    if hasattr(part, "function_call") and part.function_call:
                        did_call_function = True
                        fn = part.function_call
                        fn_name = fn.name
                        print(f" - Calling function: {fn_name}")
                        sys.stdout.flush()

                        result = call_function(fn, verbose=verbose)
                        
                        messages.append(
                            types.Content(
                                role="user",
                                parts=[types.Part(function_response=result.parts[0].function_response)],
                            )
                        )

            if did_call_function:
                continue

            if response.text:
                print("Final response:\n")
                print(response.text)
                sys.stdout.flush()
                break

        except Exception as e:
            print(f"Error during iteration {i+1}: {e}")
            sys.stdout.flush()
            break

    else:
        print("Reached max iterations (20) without final response.")
        sys.stdout.flush()


if __name__ == "__main__":
    main()