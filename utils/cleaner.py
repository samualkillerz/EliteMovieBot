import re


BRANDING = "@LordVT4ProBot"


def clean_file_name(name):

    # REMOVE EXTENSION
    extension = ""

    if "." in name:

        extension = "." + name.split(".")[-1]

        name = name.rsplit(".", 1)[0]

    # REMOVE TELEGRAM TAGS
    patterns = [

        r"@\w+",

        r"\[.*?\]",

        r"\(.*?ESub.*?\)",

        r"ESub",

        r"www\.\S+",

        r"MoviesMod",

        r"mkvCinema",

        r"Vegamovies",

        r"HDHub4u",

        r"Telly",

        r"TamilBlasters",

        r"Telugu",

        r"Hindi Dubbed",

        r"Official",

        r"RymOfficial",

        r"SkymoviesHD",

        r"CineVood",
    ]

    for pattern in patterns:

        name = re.sub(
            pattern,
            "",
            name,
            flags=re.IGNORECASE
        )

    # REMOVE EXTRA SYMBOLS
    name = re.sub(
        r"[_\-\.]+",
        " ",
        name
    )

    # REMOVE EXTRA SPACES
    name = " ".join(
        name.split()
    )

    # ADD YOUR BRANDING
    cleaned = (
        f"{name} {BRANDING}"
    ).strip()

    return cleaned + extension
