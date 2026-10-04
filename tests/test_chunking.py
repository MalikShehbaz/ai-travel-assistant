from app.ai.chunking import chunk_text


def test_chunk_text():
    text = "First section.\n\nSecond section."

    chunks = chunk_text(text)

    assert chunks == [
        "First section.",
        "Second section.",
    ]