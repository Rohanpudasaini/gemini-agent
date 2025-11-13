import os
import shutil


def get_files_info(directory: str) -> str:
    """
    List files and folders in a directory.

    This tool safely lists files and subdirectories within a given directory path.
    It automatically prevents directory traversal attacks by ensuring all paths
    stay within the allowed working directory scope (current directory).

    **Usage:**
    - Use this tool when you need to see which files or folders exist.
    - Always provide the target path relative to the current directory (`directory` argument).

    Args:
        directory (str, optional): The relative path from the current working directory
            whose contents should be listed. Defaults to "" (current directory).

    Returns:
        str: A newline-separated list of JSON-like objects representing each file or folder, e.g.:
            {'name': 'example.py', 'is_file': True, 'size': 1234}
    """
    working_directory = os.path.abspath(".")
    absolute_path = os.path.abspath(
        os.path.join(working_directory, directory) if directory else working_directory
    )
    print(f"Working Directory: {working_directory}")
    print(f"Absolute Path: {absolute_path}")
    if not absolute_path.startswith(working_directory) or ".." in os.path.relpath(
        absolute_path, working_directory
    ):
        return "Requested directory is out of scope for this tool"

    contents = os.listdir(absolute_path)
    files_info = []
    for item in contents:
        item_path = os.path.join(absolute_path, item)
        is_file = os.path.isfile(item_path)
        size = os.path.getsize(item_path) if is_file else 0
        files_info.append({"name": item, "is_file": is_file, "size": size})
    # print(files_info)
    return "\n".join(str(file) for file in files_info)


def get_file_content(file_path: str) -> str:
    """
    Read the content of a specific file.

    This tool safely reads text content from a file while preventing directory traversal attacks.
    It ensures the file is within the allowed working directory (current directory).

    **Usage:**
    - Use this tool when you need to see or analyze the content of a file.
    - Always provide the target file path relative to the current directory (`file_path` argument).

    Args:
        file_path (str): The relative path to the file to read, starting from the current directory.

    Returns:
        str: The file's content if found, or an error message such as "File not found" or "Requested directory is out of scope for this tool".
    """
    working_directory = os.path.abspath(".")
    absolute_file_path = os.path.abspath(os.path.join(working_directory, file_path))
    if not absolute_file_path.startswith(working_directory) or ".." in os.path.relpath(absolute_file_path, working_directory):
        return "Requested directory is out of scope for this tool"
    try:
        with open(absolute_file_path, "r", encoding="utf-8") as file:
            content = file.read()
        return content
    except FileNotFoundError:
        return "Error while reading file: File not found"
    except Exception as e:
        return f"Error while reading file: {str(e)}"


def write_file_content(file_path: str, content: str) -> str:
    """
    Write text content to a file safely.

    This tool creates or overwrites a file within the current working directory.
    It prevents directory traversal by ensuring that all write operations stay inside
    the allowed working directory.

    Args:
        file_path (str): The relative path (from the current working directory) of the file to write.
            Example: "app/config.json", "data/output.txt".
        content (str): The exact text content to write into the file.

    Returns:
        str: A message indicating whether the file was written successfully or if an error occurred.

    Usage:
        - Use this tool to create new files or update existing ones.
        - Only use paths relative to the current working directory.
        - Never attempt to write outside the current directory.
        - Example call:
            write_file_content(file_path="logs/info.txt", content="Log entry added.")
    """
    working_directory = os.path.abspath(".")
    absolute_file_path = os.path.abspath(os.path.join(working_directory, file_path))
    parent_directory = os.path.dirname(absolute_file_path)

    if not absolute_file_path.startswith(working_directory) or ".." in os.path.relpath(absolute_file_path, working_directory):
        return "Requested directory is out of scope for this tool"

    os.makedirs(parent_directory, exist_ok=True)
    try:
        if os.path.exists(absolute_file_path):
            backup_path = absolute_file_path + ".bak"
            shutil.copy2(absolute_file_path, backup_path)

        with open(absolute_file_path, "w", encoding="utf-8") as file:
            file.write(content)
        return "File written successfully"
    except Exception as e:
        return f"Error while writing file: {str(e)}"


def append_file_content(file_path: str, content: str) -> str:
    """
    Append content to a specific file safely, creating a backup of the original first.

    This tool safely appends text content to a file while preventing directory traversal attacks.
    It ensures the file is within the allowed working directory (current directory), and before
    appending, it automatically creates a backup (`<filename>.bak`) if the file already exists.

    **Usage:**
    - Use this tool when you need to add new lines or extend a file without overwriting existing data.
    - Always provide the target file path relative to the current directory (`file_path` argument).

    Args:
        file_path (str): The relative path to the file to append.
        content (str): The content to append to the file.

    Returns:
        str: A message indicating whether the content was appended successfully (and a backup was created)
            or if an error occurred.
    """
    working_directory = os.path.abspath(".")
    absolute_file_path = os.path.abspath(os.path.join(working_directory, file_path))
    parent_directory = os.path.dirname(absolute_file_path)

    if not absolute_file_path.startswith(working_directory) or ".." in os.path.relpath(absolute_file_path, working_directory):
        return "Requested directory is out of scope for this tool"

    os.makedirs(parent_directory, exist_ok=True)
    try:
        # Create a backup before appending
        file_existed = os.path.exists(absolute_file_path)
        if file_existed:
            backup_path = absolute_file_path + ".bak"
            shutil.copy2(absolute_file_path, backup_path)

        with open(absolute_file_path, "a", encoding="utf-8") as file:
            file.write(content)

        if file_existed:
            return "Content appended successfully (backup created)."
        else:
            return "Content appended successfully."
    except Exception as e:
        return f"Error while appending to file: {str(e)}"
