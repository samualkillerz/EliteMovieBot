import requests

from config import OMDB_API


async def search_omdb(query):

    url = (
        "https://www.omdbapi.com/"
        f"?apikey={OMDB_API}"
        f"&t={query}"
    )

    try:

        response = requests.get(url)

        data = response.json()

        if data.get("Response") == "False":
            return None

        return {
            "rating": data.get(
                "imdbRating",
                "N/A"
            ),

            "genre": data.get(
                "Genre",
                "Unknown"
            ),

            "plot": data.get(
                "Plot",
                "No plot available."
            ),

            "imdb": data.get(
                "imdbID",
                ""
            )
        }

    except Exception as e:

        print(e)

        return None
