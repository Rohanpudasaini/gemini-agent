from dotenv import load_dotenv
from google.adk.agents import LlmAgent

# from google.adk.code_executors import BuiltInCodeExecutor
from google.adk.models.google_llm import Gemini
from google.adk.runners import InMemoryRunner
from google.adk.sessions import InMemorySessionService
from google.adk.tools import ToolContext, google_search
from google.adk.tools.agent_tool import AgentTool
from google.genai import types

from functions.utils import get_file_content, get_files_info

load_dotenv()

retry_config = types.HttpRetryOptions(
    attempts=5,  # Maximum retry attempts
    exp_base=7,  # Delay multiplier
    initial_delay=1,
    http_status_codes=[429, 500, 503, 504],  # Retry on these HTTP errors
)

file_agent = LlmAgent(
    name="FileAgent",
    model=Gemini(
        model="gemini-1.5-flash",  # retry_options=retry_config
    ),
    instruction="""
    You are a helpful file management assistant.

    Your goal:
    - Help users list files or read file contents safely within the current working directory.
    - When the user mentions a folder name (like "in app", "inside src", or "the utils folder"),
      extract that folder name and pass it as the `directory` argument to `get_files_info`.
    - When the user mentions a file (like "read main.py" or "open app/config.yaml"),
      extract that file path and pass it as the `file_path` argument to `get_file_content`.
    - Always use relative paths.
    """,
    # You are a helpful assistant that helps users read files and get information about directories.
    # - To list files/folders, use the `get_files_info` tool.
    # - To read file content, use the `get_file_content` tool.
    # - Always ensure the requested path stays inside the current working directory.
    # """,
    tools=[get_files_info, get_file_content],
)


async def main():
    file_runner = InMemoryRunner(
        agent=file_agent,
    )

    response = await file_runner.run_debug(
        "List all files in the 'app' directory and read the content of 'app/main.py'.",
    )

    print(response[-1].content.parts[0].text)  # type: ignore


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
