# File Handling - Readline Methods

# 1. Use of readline()
file_handle = open("newfile.txt")
current_line = file_handle.readline()
while current_line:
    print(current_line)
    current_line = file_handle.readline()
file_handle.close()

# or

file_handle = open("newfile.txt")
line_data = file_handle.readline()
while line_data != "":
    print(line_data)
    line_data = file_handle.readline()
file_handle.close()

# 2. Use of readlines()
file_handle = open("newfile.txt")
all_lines = file_handle.readlines()
print(all_lines)
file_handle.close()
