import os
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path, args=None):
    working_dir_abs_path = os.path.abspath(working_directory)

    # construct the full path to target file
    target_file = os.path.normpath(os.path.join(working_dir_abs_path, file_path))

    # check if the target file path is in the working directory
    valid_target_file = os.path.commonpath([working_dir_abs_path, target_file]) == working_dir_abs_path

    # add gaurdrails to limit the scope of directories and files that the LLM is able to view.
    if not valid_target_file:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
    # check if target file path is exists and is a regular file
    if not os.path.isfile(target_file):
        return f'Error: "{file_path}" does not exist or is not a regular file'
    
    # make sure we only run python files
    if not target_file.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file'

    # create command list to run command for the subprocess
    command = ["python", target_file]

    # if additional args were provided add to command list
    if args:
        command.extend(args)
    
    return run_command_output(command, working_dir_abs_path)
    
def run_command_output(command, working_dir_abs_path):
    try:
        # run the command using subprocess...this returns a completed process object
        completed_process = subprocess.run(
            command, # run the built command
            cwd=working_dir_abs_path, # set the working dir properly
            capture_output=True, # Capture standard output and standard error
            text=True, # Decode output to strings
            timeout=30 # Set a timeout of 30 seconds
        )

        # build an output str based on the completed process
        output_str = ""

        if completed_process.returncode != 0:
            output_str = f"Process exited with code {completed_process.returncode}"
        elif not completed_process.stdout and not completed_process.stderr:
            output_str = "No output produced"
        
        if completed_process.stdout:
            output_str += f"STDOUT: {completed_process.stdout.strip()}"
        if completed_process.stderr:
            if output_str:
                output_str += "\n"
            output_str += f"STDERR: {completed_process.stderr.strip()}"
        
        return output_str

    except Exception as e:
        return f"Error: executing Python file: {e}"
    
# Define the function schema for run_python_file to be used in the LLM's function calling capabilities
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a specified Python file with optional arguments, with guardrails to prevent execution of files outside the working directory and to ensure only Python files are executed",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path to the Python file to execute, relative to the working directory",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                    type=types.Type.STRING,
                ),
                description="Optional list of string arguments to pass to the Python file when executing",
            ),
        },
        required=["file_path"],
    ),
)