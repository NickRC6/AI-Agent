def get_files_info(working_directory, directory="."):
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

        result_lines = []

        for root, dirs, files in os.walk(full_path):
            rel_root = os.path.relpath(root, working_directory)
            if rel_root == ".":
                rel_root = ""
            for d in dirs:
                dir_path = os.path.join(root, d)
                result_lines.append(
                    f"- {os.path.join(rel_root, d)}: file_size=0 bytes, is_dir=True"
                )
            for f in files:
                file_path = os.path.join(root, f)
                try:
                    file_size = os.path.getsize(file_path)
                except Exception as e:
                    file_size = f"Error getting size: {e}"
                result_lines.append(
                    f"- {os.path.join(rel_root, f)}: file_size={file_size} bytes, is_dir=False"
                )

        output = "\n".join(result_lines)
        print(output)
        return output

    except Exception as e:
        msg = f"Error: {e}"
        print(msg)
        return msg