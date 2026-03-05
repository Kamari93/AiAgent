from functions.get_file_content import get_file_content
from test_get_files_info import print_result

def run_tests():
    print_result('Result for "lorem.txt" file:', get_file_content("calculator", "lorem.txt"))
    print_result('Result for "main.py" file:', get_file_content("calculator", "main.py"))
    print_result('Result for "pkg/calculator.py" file:', get_file_content("calculator", "pkg/calculator.py"))
    print_result('Result for "/bin/cat" file:', get_file_content("calculator", "/bin/cat"))
    print_result('Result for "pkg/does_not_exist.py" file:', get_file_content("calculator", "pkg/does_not_exist.py"))


# only run when executed directly
if __name__ == "__main__":
    run_tests()