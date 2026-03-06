import os

def write_file(working_directory, file_path, content):
    working_dir_abs_path = os.path.abspath(working_directory)

    # construct the full path to target file
    target_file = os.path.normpath(os.path.join(working_dir_abs_path, file_path))

    # check if the target file path is in the working directory
    valid_target_file = os.path.commonpath([working_dir_abs_path, target_file]) == working_dir_abs_path

    # add gaurdrails to limit the scope of directories and files that the LLM is able to view.
    if not valid_target_file:
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    
    # check if the file path points to an existing dir
    if os.path.isdir(target_file):
        return f'Error: Cannot write to "{file_path}" as it is a directory'
    
    # ensure all parent directories of the file path exist
    directory = os.path.dirname(target_file)

    #  Create the directory and any missing parent directories...If the necessary directory structure already exists, this will do nothing
    if directory:
        os.makedirs(directory, exist_ok=True)
    
    return write_contents(target_file, file_path, content)

def write_contents(target_file, file_path, content):
    try:
        with open(target_file, "w") as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error writing to {file_path}: {e}"