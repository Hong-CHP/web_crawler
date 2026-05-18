import os, csv
import requests
from lxml import html
from urllib.parse import urlparse
from save_csv import save_csv_content


TMDB_DOMAINE = "https://www.themoviedb.org"
TMDB_TOP_URL_1 = "https://www.themoviedb.org/movie/top-rated"
TMDB_TOP_URL_2 = "https://www.themoviedb.org/discover/movie/items"

def get_movie_info(movie_url) -> list:
    # 1.send request, get details
    movie_res = requests.get(movie_url)
    print(f"Get movie's informations from: {movie_url}...")

    # 2.parse data, get movie's info
    movie_doc = html.fromstring(movie_res.text)
    movie_name = movie_doc.xpath("/html/body/div[1]/main/section/div[2]/div/div/section/div[2]/section/div[1]/h2/a/text()")
    movie_year = movie_doc.xpath("/html/body/div[1]/main/section/div[2]/div/div/section/div[2]/section/div[1]/h2/span/text()")
    movie_date = movie_doc.xpath("/html/body/div[1]/main/section/div[2]/div/div/section/div[2]/section/div[1]/div/span[2]/text()")
    movie_genres = movie_doc.xpath("/html/body/div[1]/main/section/div[2]/div/div/section/div[2]/section/div[1]/div/span[3]/a/text()")
    movie_time = movie_doc.xpath("/html/body/div[1]/main/section/div[2]/div/div/section/div[2]/section/div[1]/div/span[4]/text()")
    movie_rate = movie_doc.xpath("/html/body/div[1]/main/section/div[2]/div/div/section/div[2]/section/div[2]/div/div/div[1]/div/div[1]/div/div/@data-percent")
    movie_lang = movie_doc.xpath("/html/body/div[1]/main/section/div[3]/div/div/div[2]/div/section/div[1]/div/section[1]/p[2]/text()")
    movie_dir = movie_doc.xpath("/html/body/div[1]/main/section/div[2]/div/div/section/div[2]/section/div[3]/ol/li[1]/p[1]/a/text()")
    movie_author = movie_doc.xpath("/html/body/div[1]/main/section/div[2]/div/div/section/div[2]/section/div[3]/ol/li[2]/p[1]/a/text()")
    movie_slogan = movie_doc.xpath("/html/body/div[1]/main/section/div[2]/div/div/section/div[2]/section/div[3]/h3[1]/text()")
    movie_desp = movie_doc.xpath("/html/body/div[1]/main/section/div[2]/div/div/section/div[2]/section/div[3]/div/p/text()")
    # 3.return infos
    movie_info = {
        "name": movie_name[0].strip() if movie_name else '',
        "year": movie_year[0].strip() if movie_year else '',
        "date": movie_date[0].strip() if movie_date else '',
        "genres": ','.join(g.strip() for g in movie_genres) if movie_genres else '',
        "time": movie_time[0].strip() if movie_time else '',
        "rate": movie_rate[0].strip() if movie_rate else '',
        "lang": movie_lang[0].strip() if movie_lang else '',
        "dir": movie_dir[0].strip() if movie_dir else '',
        "auth": movie_author[0].strip() if movie_author else '',
        "slog": movie_slogan[0].strip() if movie_slogan else '',
        "desp": movie_desp[0].strip() if movie_desp else '',
    }
    return movie_info
    

def save_all_movies(all_movies, domaine_name, target_file):
    if not os.path.exists(f"movie_data/{domaine_name}"):
        os.makedirs(f"movie_data/{domaine_name}")
    with open(f"movie_data/{domaine_name}/{target_file}.csv", "w", encoding="utf-8") as f:
        data_w = csv.DictWriter(f, fieldnames=["name", "year","date",
                                               "genres","time", "rate",
                                               "lang", "dir", "auth",
                                               "slog", "desp"])
        data_w.writeheader()
        data_w.writerows(all_movies)

def has_number(str) -> bool:
    return any(c.isdigit() for c in str)
 
def main():
    all_movies = []
    domaine_name = None
    target_page = None
    target_file = ""

    for page in range(1, 6):
        # 1.send requests to get top rated data
        domaine = urlparse(TMDB_DOMAINE).netloc
        domaine_name = domaine.split(".")[1]
        target_page = urlparse(TMDB_TOP_URL_1).path.split('/')
        target_file = "_".join(t for t in target_page if t)

        res = None
        try:
            if page == 1:
                res = requests.get(TMDB_TOP_URL_1, timeout=60)
            else:
                res = requests.post(TMDB_TOP_URL_2, 
                                    f"air_date.gte=&air_date.lte=&certification=&certification_country=US&debug=&first_air_date.gte=&first_air_date.lte=&include_adult=false&include_softcore=false&latest_ceremony.gte=&latest_ceremony.lte=&page={page}&primary_release_date.gte=&primary_release_date.lte=&region=&release_date.gte=&release_date.lte=2026-11-18&show_me=everything&sort_by=vote_average.desc&vote_average.gte=0&vote_average.lte=10&vote_count.gte=300&watch_region=US&with_genres=&with_keywords=&with_networks=&with_origin_country=&with_original_language=&with_watch_monetization_types=&with_watch_providers=&with_release_type=&with_runtime.gte=0&with_runtime.lte=400",
                                    timeout=60)
            res.raise_for_status()
        except requests.RequestException as e:
            print(f"Request failed: {e}")

        # 2.extract movies list
        doc = html.fromstring(res.text)
        url_list = doc.xpath("//a[contains(@href, '/movie/')]/@href")
        all_movies_url = []

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
    print("Movies's informations saved successfully in 'movie_data/tmdb_top_rated.csv'!")
    save_all_movies(all_movies, domaine_name, target_file)

if __name__ == '__main__':
    main()