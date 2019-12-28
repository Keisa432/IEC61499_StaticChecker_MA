#!/usr/bin/python3
from file_index import FileIndex

if __name__ == "__main__":
    index = FileIndex(r"C:\Users\Dominik\Documents\LStudioProjects\ma_test", ['.sys', '.fbt', '.res'])
    print(index.get_file_by_name('System'))
