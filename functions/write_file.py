from google.genai import types
import os

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes text content to a file in the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "path": types.Schema(
                type=types.Type.STRING,
                description="The name or path of the file to write."
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write into the file."
            ),
        },
    ),
)

def write_file(working_directory, path, content):
    try:
        working_directory = os.path.abspath(working_directory)
        full_path = os.path.abspath(os.path.join(working_directory, path))

        # Keep it inside working directory
        if os.path.commonpath([working_directory, full_path]) != working_directory:
            msg = f'Error: Cannot write outside working directory ("{path}")'
            print(msg)
            return msg

        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content)

        print(content)
        return content

    except Exception as e:
        msg = f"Error: {e}"
        print(msg)
        return msg