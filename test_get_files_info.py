from functions.get_files_info import get_files_info


def run_tests():
    print_result("Result for current directory:", get_files_info("calculator", "."))
    print_result('Result for "pkg" directory:', get_files_info("calculator", "pkg"))
    print_result('Result for "/bin" directory:', get_files_info("calculator", "/bin"))
    print_result('Result for "../" directory:', get_files_info("calculator", "../"))


def print_result(label, result):
    print(label)
    if result.startswith("Error:"):
        print(f"    {result}")
    else:
        for line in result.splitlines():
            print(f"  {line}")

# only run when executed directly
if __name__ == "__main__":
    run_tests()