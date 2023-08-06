def split_text(text: str, sep: str) -> list[str]:
    i = text.find(sep)
    if i == -1:
        return [text.strip()]

    return [text[0:i].strip(), text[i + len(sep):].strip()]


def filter_irrelevant(lines: list[str]) -> filter:
    return filter(lambda line: line != '' and line[0] != '#', map(lambda line: line.strip(), lines))
