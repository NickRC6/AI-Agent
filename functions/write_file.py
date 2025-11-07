def write_file(working_directory, file_path, content):
    import os

    try:
        working_directory = os.path.abspath(working_directory)
        full_path = os.path.abspath(os.path.join(working_directory, file_path))

        if os.path.commonpath([working_directory, full_path]) != working_directory:
            msg = f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
            print(msg)
            return msg

        dir_name = os.path.dirname(full_path)
        os.makedirs(dir_name, exist_ok=True)

        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content)

        msg = f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        print(msg)
        return msg

    except Exception as e:
        msg = f'Error: {e}'
        print(msg)
        return msg