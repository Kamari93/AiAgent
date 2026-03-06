from functions.write_file import write_file
from test_get_files_info import print_result

def run_tests():
    print_result('Result for "lorem.txt" file:', write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum"))
    print_result('Result for "pkg/morelorem.txt" file:', write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"))
    print_result('Result for "/tmp/temp.txt" file:', write_file("calculator", "/tmp/temp.txt", "this should not be allowed"))

# only run when executed directly
if __name__ == "__main__":
    run_tests()