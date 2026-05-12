import requests

from config import TMDB_API


async def search_tmdb(query):

    try:

        url = (
            "https://api.themoviedb.org/3/search/movie"
            f"?api_key={TMDB_API}"
            f"&query={query}"
        )

        response = requests.get(
            url,
            timeout=15
        )

        data = response.json()

        print(data)

        results = data.get("results")

        if not results:
            return None

        result = results[0]

        title = result.get(
            "title",
            "Unknown"
        )

        year = ""

        if result.get("release_date"):

            year = result[
                "release_date"
            ][:4]

        poster = None

        if result.get("poster_path"):

            poster = (
                "https://image.tmdb.org/t/p/w500"
                f"{result['poster_path']}"
            )

        return {
            "title": title,
            "year": year,
            "poster": poster
        }

    except Exception as e:

        print("TMDB ERROR:", e)

        return None
