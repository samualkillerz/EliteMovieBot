from utils.tmdb import search_tmdb
from utils.omdb import search_omdb


async def get_metadata(query):

    tmdb = await search_tmdb(query)

    if not tmdb:
        return None

    omdb = await search_omdb(
        tmdb["title"]
    )

    return {
        "title": tmdb["title"],
        "year": tmdb["year"],
        "poster": tmdb["poster"],

        "rating": (
            omdb["rating"]
            if omdb else "N/A"
        ),

        "genre": (
            omdb["genre"]
            if omdb else "Unknown"
        ),

        "plot": (
            omdb["plot"]
            if omdb else "No plot."
        ),

        "imdb": (
            omdb["imdb"]
            if omdb else ""
        )
    }
