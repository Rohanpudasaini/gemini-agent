def read_response(response) -> str:
    result = ""
    for number in range(len(response)):
        if response[number].content.parts[0].text:  # type: ignore
            result += response[number].content.parts[0].text  # type: ignore
    return result
