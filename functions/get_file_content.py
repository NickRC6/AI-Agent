from google.genai import types
import os

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Retrieves the content of a specified file within the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to read, relative to the working directory.",
            ),
        },
        required=["file_path"],
    ),
)

def get_file_content(working_directory, file_path):
    import os
    from config import MAX_FILE_LENGTH

    try:
        working_directory = os.path.abspath(working_directory)
        full_path = os.path.abspath(os.path.join(working_directory, file_path))

        if os.path.commonpath([working_directory, full_path]) != working_directory:
            msg = f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
            print(msg)
            return msg

        if not os.path.isfile(full_path):
            msg = f'Error: File not found or is not a regular file: "{file_path}"'
            print(msg)
            return msg

        with open(full_path, "r", encoding="utf-8") as f:
            contents = f.read()

        if len(contents) > MAX_FILE_LENGTH:
            contents = (
                contents[:MAX_FILE_LENGTH]
                + f'\n[...File "{file_path}" truncated at {MAX_FILE_LENGTH} characters]'
            )

        print(contents)
        return contents

    except Exception as e:
        msg = f'Error: {e}'
        print(msg)
        return msg
