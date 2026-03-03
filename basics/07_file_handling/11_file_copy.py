# Write a program to make a copy of "this.txt" to "pcopy.txt"

def copy_file(source, destination):
    """Copy content from source to destination file"""
    with open(source, "r") as f:
        data = f.read()
    with open(destination, "w") as f:
        f.write(data)


copy_file("this.txt", "pcopy.txt")
    