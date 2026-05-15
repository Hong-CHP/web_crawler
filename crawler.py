import os
import requests
from lxml import html
from urllib.parse import urlparse
from save_csv import save_csv_content


TMDB_DOMAINE = "https://www.themoviedb.org"
TMDB_TOP_URL = "https://www.themoviedb.org/movie/top-rated"

def get_movie_info(movie_url) -> list:
    pass

def save_all_movies(all_movies):
    pass

def has_number(str) -> bool:
    return any(c.isdigit() for c in str)
 
def main():
    # 1.send requests to get top rated data
    domaine = urlparse(TMDB_DOMAINE).netloc
    domaine_name = domaine.split(".")[1]
    target_page = urlparse(TMDB_TOP_URL).path

    res = None
    try:
        res = requests.get(TMDB_TOP_URL, timeout=60)
        res.raise_for_status()
    except requests.RequestException as e:
        print(f"Request failed: {e}")

    # 2.extract movies list
    doc = html.fromstring(res.text)
    url_list = doc.xpath("//a[contains(@href, '/movie/')]/@href")
    all_movies_url = []
    all_movies = []
    for url in url_list:
        if not has_number(url):
            continue 
        movie_url = TMDB_DOMAINE + url
        if movie_url not in all_movies_url:
            all_movies_url.append(movie_url)

    # 3.get each movie info in list by url
    for movie_url in all_movies_url:
        movie_info = get_movie_info(movie_url)
        all_movies.append(movie_info)

    # 4.stock data in csv file
    save_all_movies(all_movies)

if __name__ == '__main__':
    main()

# if site_content:
#     if not os.path.exists(f"sources/{domaine_name}"):
#         os.makedirs(f"sources/{domaine_name}")
#     with open(f"sources/{domaine_name}/{page}.html", "w", encoding="utf-8") as f:
#         f.write(site_content)

# print("Web content saved successfully")

# extract_html()

# save_csv_content()