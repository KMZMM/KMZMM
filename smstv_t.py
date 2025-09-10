#!/data/data/com.termux/files/usr/bin/python
import requests
import json
import time

OUTPUT_FILE = "movies.json"

# Replace this with your real token
AUTH_TOKEN = "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiI5ZWJjNDUzZS00ZTU5LTRiOGEtYjk0Ny0xMWUwNjUyN2NhZDUiLCJqdGkiOiI0NzdhMzUyYWMwOGVhYWNiMDNiNTNmYzhkY2FmMTQ4YmQ2MWMwNTZhMDcwY2Y2MzJmMWFhYzI5OTQ5MWNjMDE5YzIyZDk3YTQwNGFiOTE2YiIsImlhdCI6MTc1NzQ5OTIxNy40NjQwOTYsIm5iZiI6MTc1NzQ5OTIxNy40NjQxMDQsImV4cCI6MTc4OTAzNTIxNy40NTEyMjEsInN1YiI6IjE3MDkiLCJzY29wZXMiOltdfQ.fHLgsxcD-zvdxWF0tvlW2zZzrQvXTGrcrKkBf1_HkyWYEoKE_Vu13_nVt9BUJQhgeJyN5vj-9rPnWIJmOfjFDaxJODxHuQ3xxHvKi80GBDz7MypXRfMaH0QYcVYGYCnoesL0oOMOuya55NNWF2R5wqlxS7n5CjHHwqbgiV0HQ3qqZn1ifZasLDiS8dufflDDrQoCHj_gHOSg8IHgWQEprrBh-jgH83KdtZkhM7JdXudKF4K_JZycD9u7sCtMRbWqRYCqMiwWD91n2A8dpPgzChsMVB3nLBtCnsI-hRVptq9phunfDK13GtvPiKPTVwnLTWH5TpXgqqTPeYXGdbodbETsIo9AC6f02lWuczXOW2kjKHKXcOxAQnEN4J7unvnuI5Gm_zmbebTzmbOwH2HuanYsEJlmw7cUh52mek2DWBQFXSqg_iKt5DaiCSL8eM20fVDH3PNpgHhadolGgL0msSvdUscSUbLnpU2ekVJZcQwviLM0IkKXih7cPIXgQV2EuUUN09bR4mQvb7H2S3TFXwzs6QUpDv8F10vn0VBsFx9rRqkdT_y7b45XB8XcCYvCCEVkDa6rrx_W343xNQ4HLboVVQkn-wEKMXaNzpoKcdmOrU3sbT169ybt_U-nqAs_YY1MC-o1GknSBeU6nrWUjIb2cIyee8oGu_fkLdTB-gk"

HEADERS = {
    "user-agent": "Dart/3.7 (dart:io)",
    "accept-encoding": "gzip",
    "authorization": AUTH_TOKEN
}

def fetch_movie_ids(page):
    url = f"http://shwemateset.com/api/sub/movie/get?page={page}"
    try:
        r = requests.get(url, headers=HEADERS, timeout=15)
        r.raise_for_status()
        data = r.json()
        movies_node = data.get("data")
        if isinstance(movies_node, dict):
            return movies_node.get("data", []) or []
        if isinstance(movies_node, list):
            return movies_node
        return data.get("data", []) or []
    except Exception as e:
        print(f"Error fetching page {page}: {e}")
        return []

def fetch_movie_sources(movie_id):
    url = f"https://or.smstv.live/api/sub/movie/source/get/{movie_id}"
    try:
        r = requests.get(url, headers=HEADERS, timeout=15)
        r.raise_for_status()
        data = r.json()
        sources_node = data.get("data", [])
        if isinstance(sources_node, dict):
            sources_list = sources_node.get("data", []) or []
        else:
            sources_list = sources_node or []

        formatted = []
        for src in sources_list:
            formatted.append({
                "source_name": src.get("source_name"),
                "quality": src.get("quality"),
                "type": src.get("type"),
                "url": src.get("url"),
                "isPremium": src.get("isPremium")
            })
        return formatted
    except Exception as e:
        print(f"Error fetching sources for {movie_id}: {e}")
        return []

def save_movies(all_movies):
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(all_movies, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    all_movies = []
    counter = 0

    for page in range(1, 561):
        movies = fetch_movie_ids(page)
        print(f"Page {page}: found {len(movies)} movies")

        for movie in movies:
            movie_id = movie.get("id")
            if not movie_id:
                continue

            sources = fetch_movie_sources(movie_id)
            if not sources:
                print(f"No sources for movie id {movie_id} ({movie.get('name')})")

            movie_data = {
                "id": movie_id,
                "name": movie.get("name"),
                "year": movie.get("year"),
                "poster": movie.get("poster"),
                "cover": movie.get("cover"),
                "genre": movie.get("genre"),
                "description": movie.get("description"),
                "release_date": movie.get("release_date"),
                "sources": sources
            }

            all_movies.append(movie_data)
            counter += 1

            if counter % 20 == 0:
                save_movies(all_movies)
                print(f"Saved {counter} movies so far...")
                time.sleep(1)

            time.sleep(0.2)

    save_movies(all_movies)
    print(f"Final save complete: {counter} movies total")