

def write_to_file(path, flags, content):
    with open(path, flags) as file:
        file.write(content)


def read_from_file(path, flags):
    with open(path, flags) as file:
        return file.read()