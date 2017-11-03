

def write_to_file(path, flags, content):
    with open(path, flags) as f:
        f.write(content)


def read_from_file(path, flags):
    with open(path, flags) as f:
        return f.read()
