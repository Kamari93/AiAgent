from functions.run_python_file import run_python_file
from test_get_files_info import print_result

def run_tests():
    print_result('Result for "main.py" file with no args:', run_python_file("calculator", "main.py"))
    print_result('Result for "main.py" file with args ["3 + 5"]:', run_python_file("calculator", "main.py", ["3 + 5"]))
    print_result('Result for "tests.py" file with no args:', run_python_file("calculator", "tests.py"))
    print_result('Result for "../main.py" file with no args:', run_python_file("calculator", "../main.py"))
    print_result('Result for "nonexistent.py" file with no args:', run_python_file("calculator", "nonexistent.py"))
    print_result('Result for "lorem.txt" file with no args:', run_python_file("calculator", "lorem.txt"))

# only run when executed directly
if __name__ == "__main__":
    run_tests()