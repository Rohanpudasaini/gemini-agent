from functions.get_files_info import get_files_info


def test_file_info():
    result = get_files_info(
        working_directory="app",
        directory="../..",
    )
    assert result == "Directory traversal detected"
    result = get_files_info(working_directory="app")
    assert "test.py" in result
    assert "main.py" in result
    result = get_files_info(working_directory="app", directory="..")
    assert result == "Directory traversal detected"
    result = get_files_info(working_directory="app", directory="db")
    assert "__init__.py" in result
