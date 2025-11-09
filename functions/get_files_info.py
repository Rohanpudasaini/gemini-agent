import os


def get_files_info(working_directory, directory=None):
    working_directory = os.path.abspath(working_directory)
    absulate_path = os.path.abspath(
        os.path.join(working_directory, directory) if directory else working_directory
    )
    print(f"Working Directory: {working_directory}")
    print(f"Absolute Path: {absulate_path}")
    if not absulate_path.startswith(working_directory) or ".." in os.path.relpath(
        absulate_path, working_directory
    ):
        return "Directory traversal detected"

    contents = os.listdir(absulate_path)
    files_info = []
    for item in contents:
        item_path = os.path.join(absulate_path, item)
        is_file = os.path.isfile(item_path)
        size = os.path.getsize(item_path) if is_file else 0
        files_info.append({"name": item, "is_file": is_file, "size": size})
    # print(files_info)
    return "\n".join(str(file) for file in files_info)


# get_files_info("../../", "../")
print(
    get_files_info(
        # os.getcwd()
        working_directory="app",
        directory="..",
    )
)
