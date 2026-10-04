def chunk_text(text: str) -> list[str]:
    chunks = []

    sections = text.split("\n\n")

    for section in sections:
        section = section.strip()

        if section:
            chunks.append(section)

    return chunks