def version():
    with open(os.path.join(self.__root_dir, 'VERSION'), 'r') as f:
        ver = f.read()
    return ver.strip()
