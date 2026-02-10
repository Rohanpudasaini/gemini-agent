from typing import Sequence, Any

def read_response(response: Sequence[Any]) -> str:
    result = []
    for number in range(len(response)):
        if response[number].content.parts[0].text:  # type: ignore
            result.append(response[number].content.parts[0].text)  # type: ignore
    return "".join(result)

class FileAgent:
    def __init__(self, filepath: str):
        self.filepath = filepath
        self.buffer = []
        self.history = []  # for undo
        
        self._load()

    def _load(self):
        try:
            with open(self.filepath, "r") as f:
                self.buffer = f.readlines()
        except FileNotFoundError:
            self.buffer = []  # treat as an empty file

    def save(self):
        with open(self.filepath, "w") as f:
            f.writelines(self.buffer)
        print("File saved.")

    def show(self):
        for idx, line in enumerate(self.buffer, start=1):
            print(f"{idx}: {line}", end="")

    # ---- Editing Commands ---- #

    def write(self, text: str):
        self._snapshot()
        self.buffer = [text + "\n"]

    def append(self, text: str):
        self._snapshot()
        self.buffer.append(text + "\n")

    def insert(self, line: int, text: str):
        self._snapshot()
        if line < 1: line = 1
        if line > len(self.buffer): line = len(self.buffer) + 1
        self.buffer.insert(line - 1, text + "\n")

    def replace(self, line: int, text: str):
        if not (1 <= line <= len(self.buffer)):
            print("Invalid line number.")
            return
        self._snapshot()
        self.buffer[line - 1] = text + "\n"

    def delete(self, line: int):
        if not (1 <= line <= len(self.buffer)):
            print("Invalid line number.")
            return
        self._snapshot()
        del self.buffer[line - 1]

    # ---- Undo Support ---- #
    def _snapshot(self):
        self.history.append(self.buffer.copy())

    def undo(self):
        if not self.history:
            print("Nothing to undo.")
            return
        self.buffer = self.history.pop()

    # ---- Command Parser ---- #
    def run(self):
        print("File Agent Ready. Type HELP for commands.\n")

        while True:
            command = input(">> ").strip()

            if command.upper() == "HELP":
                self._help()

            elif command.upper() == "READ":
                self.show()

            elif command.upper().startswith("WRITE "):
                self.write(command[6:].strip())

            elif command.upper().startswith("APPEND "):
                self.append(command[7:].strip())

            elif command.upper().startswith("INSERT "):
                _, line, *text = command.split()
                self.insert(int(line), " ".join(text))

            elif command.upper().startswith("REPLACE "):
                _, line, *text = command.split()
                self.replace(int(line), " ".join(text))

            elif command.upper().startswith("DELETE "):
                _, line = command.split()
                self.delete(int(line))

            elif command.upper() == "UNDO":
                self.undo()

            elif command.upper() == "SAVE":
                self.save()

            elif command.upper() == "EXIT":
                print("Bye!")
                break

            else:
                print("Invalid command. Type HELP")

    def _help(self):
        print("""
Available Commands:
    READ                       - Show file with line numbers
    WRITE <text>               - Replace file content with text
    APPEND <text>              - Add text to end of file
    INSERT <line> <text>       - Insert at a line
    REPLACE <line> <text>      - Replace a line
    DELETE <line>              - Delete a line
    UNDO                       - Undo previous edit
    SAVE                       - Save changes
    EXIT                       - Quit agent
""")

