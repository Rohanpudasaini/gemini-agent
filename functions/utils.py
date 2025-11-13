from typing import Sequence, Any

def read_response(response: Sequence[Any]) -> str:
    result = []
    for number in range(len(response)):
        if response[number].content.parts[0].text:  # type: ignore
            result.append(response[number].content.parts[0].text)  # type: ignore
    return "".join(result)
