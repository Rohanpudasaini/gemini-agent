# AI Fixer Agent

A small, command-line AI agent that reads project files, accepts user queries/updates, calls tools to edit and run code, and verifies fixes. Built to follow the boot.dev tutorial pattern: use tool-calling (file read/write, run processes) so the agent can iteratively fix issues (example: `calculator/main.py`).

## Goals
- Let a user describe a bug or change from the CLI.
- Let the agent inspect project files, propose edits, apply them, run the app/tests, and confirm the result.
- Keep the workflow simple and transparent.

## Features
- Interactive CLI prompts for tasks (fix, add feature, refactor).
- Tool calls for:
    - Reading and listing files
    - Editing files
    - Running scripts or tests
    - Reporting output and errors
- Example target: `calculator/main.py` — user can ask for fixes or improvements and the agent will try to apply them and run the file.

## Quickstart
1. Clone the repo and enter the project folder:
     - git clone <repo-url>
     - cd <repo>
2. Create a Python venv and install deps:
     - python -m venv .venv
     - source .venv/bin/activate  (or `.venv\Scripts\activate` on Windows)
     - pip install -r requirements.txt
3. Configure your AI API key (example):
     - export OPENAI_API_KEY="your_key_here"  (or set in environment on Windows)

## Usage
- Interactive mode:
    - python agent.py --project ./calculator --interactive
- Single command:
    - python agent.py --project ./calculator --task "Fix divide-by-zero error in calculator/main.py"
- The agent will:
    1. Read the project files.
    2. apply edit (via tool calls).
    3. Run the target script or tests.
    4. Return results and any remaining errors.

## Example workflow
1. User: "Calculator crashes when dividing by zero."
2. Agent reads `calculator/main.py`.
3. Agent applies the change, runs `python calculator/main.py` or tests, and reports success or next steps.


## Project layout (suggested)
- agent.py          — CLI entrypoint
- tools/            — file-reader, editor, process-runner
- calculator/       — example app (e.g., main.py)
- requirements.txt
- README.md

## Notes
- This README is intentionally concise. Implementation follows the boot.dev tutorial approach: small, testable tools + an orchestrating agent that uses them.
- Ensure your API keys and permissions are set before running the agent.

## Contributing
- Open issues and PRs are welcome. Keep changes small and focused.

## License
- Choose a permissive license (e.g., MIT) and add LICENSE file.

Enjoy building the agent!