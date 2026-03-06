import os
from config import MAX_CHARS

def get_file_content(working_directory, file_path):
    working_dir_abs_path = os.path.abspath(working_directory)

    # construct the full path to target file
    target_file = os.path.normpath(os.path.join(working_dir_abs_path, file_path))

    # check if the target file path is in the working directory
    valid_target_file = os.path.commonpath([working_dir_abs_path, target_file]) == working_dir_abs_path

    # add gaurdrails to limit the scope of directories and files that the LLM is able to view.
    if not valid_target_file:
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    
    # check if target file path is file
    if not os.path.isfile(target_file):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    
    return read_file_content(target_file, file_path)
    
def read_file_content(target_file, file_path):
    try:
        with open(target_file, 'r') as f:
            content = f.read(MAX_CHARS)

            if f.read(1):
                content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'

        return content
    except Exception as e:
        return f"Error reading {target_file}: {e}"