from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python_file import run_python_file

def run_tests():

    run_python_file("calculator", "main.py") 
    run_python_file("calculator", "main.py", ["3 + 5"]) 
    run_python_file("calculator", "tests.py")
    run_python_file("calculator", "../main.py") 
    run_python_file("calculator", "nonexistent.py")
    run_python_file("calculator", "lorem.txt")

if __name__ == "__main__":
    run_tests()