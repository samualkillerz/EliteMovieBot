import re


REMOVE_WORDS = [
    "480p",
    "720p",
    "1080p",
    "2160p",
    "x264",
    "x265",
    "hevc",
    "hdrip",
    "webrip",
    "bluray",
    "web-dl",
    "aac",
    "esub",
    "hindi",
    "english",
    "tam",
    "tel",
    "mkv",
    "mp4"
]


def normalize_query(text):

    text = text.lower()

    text = text.replace("_", " ")
    text = text.replace("-", " ")
    text = text.replace(".", " ")

    # REMOVE EXTRA WORDS
    for word in REMOVE_WORDS:

        pattern = r"\b" + re.escape(word) + r"\b"

        text = re.sub(
            pattern,
            "",
            text
        )

    # REMOVE SPECIAL CHARS
    text = re.sub(
        r"[^a-z0-9 ]",
        "",
        text
    )

    # REMOVE EXTRA SPACES
    text = re.sub(
        r"\s+",
        " ",
        text
    ).strip()

    return text
