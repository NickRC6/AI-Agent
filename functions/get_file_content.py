def get_file_content(working_directory, file_path):
    import os

    try:
        working_directory = os.path.abspath(working_directory)
        full_path = os.path.abspath(os.path.join(working_directory, directory))

        if os.path.commonpath([working_directory, full_path]) != working_directory:
            msg = f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
            print(msg)
            return msg

        if not os.path.isdir(full_path):
            msg = f'Error: "{directory}" is not a directory'
            print(msg)
            return msg
        
    except Exception as e:
        msg = f"Error: {e}"
        print(msg)
        return msg