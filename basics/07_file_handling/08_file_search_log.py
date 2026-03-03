# Search a log file for 'python' and report the line number

with open("logfile.txt", "r") as log_file:
    log_lines = log_file.readlines()
    line_number = 1
    for line_content in log_lines:
        if "python" in line_content:
            print(f"Line No: {line_number}")
            break
        line_number += 1
    else:
        print("Python not found in the log file.")

# Alternative method (commented):
# with open("logfile.txt", "r") as f:
#     data = f.read()
#     if "python" in data.lower():
#         print("Log file contains 'python'")
#     else:
#         print("Log file does not contain 'python'")

""" Sample Log Content (logfile.txt):
[INFO] System started successfully
[WARNING] Low memory detected
[INFO] User logged in
[ERROR] python module failed to load
[INFO] System shutting down
"""
