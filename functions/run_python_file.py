def run_python_file(working_directory, file_path, args=[]):
    import os
    import subprocess
    import sys

    try:
        working_directory = os.path.abspath(working_directory)
        full_path = os.path.abspath(os.path.join(working_directory, file_path))

        if os.path.commonpath([working_directory, full_path]) != working_directory:
            msg = f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
            print(msg)
            return msg

        if not os.path.isfile(full_path):
            msg = f'Error: File "{file_path}" not found.'
            print(msg)
            return msg
        if not full_path.endswith('.py'):
            msg = f'Error: "{file_path}" is not a Python file.'
            print(msg)
            return

        command = [sys.executable, full_path] + args
        result = subprocess.run(command, capture_output=True, text=True, cwd=working_directory)

        if result.returncode == 0:
            msg = f'STDOUT: Successfully ran "{file_path}". Output:\n{result.stdout}'
        else:
            msg = f"Error: executing Python file: {e}"

        print(msg)
        return msg

    except Exception as e:
        msg = f'Error: {e}'
        print(msg)
        return msg