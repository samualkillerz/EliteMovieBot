import re


def normalize_query(text):

    text = text.lower()

    text = text.replace(
        "_",
        " "
    )

    text = re.sub(
        r'[^a-z0-9 ]',
        '',
        text
    )

    text = re.sub(
        r'\s+',
        ' ',
        text
    ).strip()

    return text
