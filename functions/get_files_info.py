import os

def get_files_info(working_directory, directory="."):
    working_dir_abs_path = os.path.abspath(working_directory)
    # construct the full path to target directory 
    target_dir = os.path.normpath(os.path.join(working_dir_abs_path, directory))
    # check if the target dir is in the abs working dir path..common path should = working_dir_abs path
    valid_target_dir = os.path.commonpath([working_dir_abs_path, target_dir]) == working_dir_abs_path

    # add gaurdrails to limit the scope of directories and files that the LLM is able to view.
    if not valid_target_dir:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

    # check if dir arg is a directory
    if not os.path.isdir(target_dir):
        return f'Error: "{directory}" is not a directory'

    return list_dir_contents(target_dir)

def list_dir_contents(target_dir):
    # iterate over target directory's items and return str representing its content
    dir_items = os.listdir(target_dir)

    dir_items_list = []

    for item_name in dir_items:
        item_path = os.path.normpath(os.path.join(target_dir, item_name))
        try:
            size = os.path.getsize(item_path)
            is_dir = os.path.isdir(item_path)
            dir_items_list.append((item_name, size, is_dir))
        except (FileNotFoundError, PermissionError) as e:
            return f"Error accessing {item_path}: {e}"

    result_string = ""

    for name, size, is_dir in dir_items_list:
        result_string += f"- {name}: file_size={size} bytes, is_dir={is_dir}\n"
    
    return result_string
    
    # dir_items = os.listdir(target_dir)

    # dir_items_list = []

    # for item_name in dir_items:
    #     item_path = os.path.normpath(os.path.join(target_dir, item_name))
    #     try:
    #         size = os.path.getsize(item_path)
    #         is_dir = os.path.isdir(item_path)
    #         dir_items_list.append((item_name, size, is_dir))
    #     except (FileNotFoundError, PermissionError) as e:
    #         print(f"Error accessing {item_path}: {e}")
    #         continue

    # result_string = ""

    # for name, size, is_dir in dir_items_list:
    #     result_string += f"- {name}: file_size={size} bytes, is_dir={is_dir}/n"
    
    # return result_string
