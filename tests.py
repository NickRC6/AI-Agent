from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content

def run_tests():

    get_file_content("calculator", "lorem.txt")

if __name__ == "__main__":
    run_tests()