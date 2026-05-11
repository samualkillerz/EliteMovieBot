import requests

from config import TMDB_API


async def search_tmdb(query):

    url = (
        "https://api.themoviedb.org/3/search/multi"
        f"?api_key={TMDB_API}"
        f"&query={query}"
    )

    try:

        response = requests.get(url)

        data = response.json()

        results = data.get("results")

        if not results:
            return None

        result = results[0]

        title = (
            result.get("title") or
            result.get("name") or
            "Unknown"
        )

        year = ""

        if result.get("release_date"):
            year = result["release_date"][:4]

        elif result.get("first_air_date"):
            year = result["first_air_date"][:4]

        poster = None

        if result.get("poster_path"):

            poster = (
                "https://image.tmdb.org/t/p/w500"
                f"{result['poster_path']}"
            )

        rating = result.get(
            "vote_average",
            0
        )

        overview = result.get(
            "overview",
            "No description available."
        )

        return {
            "title": title,
            "year": year,
            "poster": poster,
            "rating": rating,
            "overview": overview
        }

    except Exception as e:
        print(e)
        return None
