import os


def get_files_info(working_directory, directory=None):
    working_directory = os.path.abspath(working_directory)
    absolute_path = os.path.abspath(
        os.path.join(working_directory, directory) if directory else working_directory
    )
    print(f"Working Directory: {working_directory}")
    print(f"Absolute Path: {absolute_path}")
    if not absolute_path.startswith(working_directory) or ".." in os.path.relpath(
        absolute_path, working_directory
    ):
        return "Directory traversal detected"

    contents = os.listdir(absolute_path)
    files_info = []
    for item in contents:
        item_path = os.path.join(absolute_path, item)
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
