from dotenv import load_dotenv
from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.adk.runners import InMemoryRunner
from google.genai import types

from functions.llm_tools import (
    append_file_content,
    get_file_content,
    get_files_info,
    write_file_content,
)
from functions.utils import read_response

load_dotenv()

retry_config = types.HttpRetryOptions(
    attempts=5,  # Maximum retry attempts
    exp_base=7,  # Delay multiplier
    initial_delay=1,
    http_status_codes=[429, 500, 503, 504],  # Retry on these HTTP errors
)

file_agent = LlmAgent(
    name="FileAgent",
    model=Gemini(model="gemini-2.0-flash", retry_options=retry_config),
    instruction="""
    You are a helpful file management assistant that can list, read, write, and append files safely
    within the current working directory.

    Your responsibilities:
    1. **Listing files**
       - When the user asks to "list", "show", or "see" files or folders,
         extract the folder name and call `get_files_info(directory=...)`.

    2. **Reading files**
       - When the user asks to "read", "open", or "view" a file,
         extract the file path and call `get_file_content(file_path=...)`.

    3. **Writing or updating files**
       - When the user asks to "write", "update", "save", or "create" a file,
         extract the file path and the text they want written.
       - Generate or modify the content as needed, and call:
         `write_file_content(file_path=..., content=...)`.
       - This function automatically creates a backup (`.bak`) of the file if it already exists.

    4. **Appending to files**
       - When the user asks to "append", "add", or "extend" a file,
         extract the file path and the text to add.
       - Use `append_file_content(file_path=..., content=...)` to safely append.
       - This also creates a backup of the original file before appending.

    Rules:
    - Always use **relative paths** (like "app/config.py" or "src/utils").
    - Never attempt to write, read, or list files outside the current directory.
    - Always validate that the target file or directory exists before reading.
    - When writing or appending, assume it is safe — backups are created automatically.
    - Do not request or modify any `working_directory` argument; it is fixed internally.
""",
    tools=[get_files_info, get_file_content, write_file_content, append_file_content],
)


async def main():
    file_runner = InMemoryRunner(
        agent=file_agent,
    )

    response = await file_runner.run_debug(
        """Read the content of 'app/main.py',
          I want another file named main2.py at app/main2.py with a very simple fastapi boiler code.""",
    )
    print(read_response(response))
    response = await file_runner.run_debug(
        """Read the content of 'app/main2.py', now append two new endpoint that returns hello name where name is query parameter and path parameter respectively.""",
    )
    print(read_response(response))


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
