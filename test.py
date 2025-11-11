from functions.utils import get_files_info


def test_file_info():
    result = get_files_info("app/../../")
    assert result == "Requested directory is out of scope for this tool"
    result = get_files_info("app")
    assert "test.py" in result
    assert "main.py" in result
    result = get_files_info("app/../../")
    assert result == "Requested directory is out of scope for this tool"
    result = get_files_info("app/db")
    assert "__init__.py" in result
