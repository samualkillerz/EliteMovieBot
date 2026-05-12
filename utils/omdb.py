import requests

from config import OMDB_API


async def search_omdb(query):

    try:

        url = (
            "https://www.omdbapi.com/"
            f"?apikey={OMDB_API}"
            f"&t={query}"
        )

        response = requests.get(
            url,
            timeout=15
        )

        data = response.json()

        print(data)

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

        print("OMDB ERROR:", e)

        return None
