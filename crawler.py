import os
import requests
from lxml import html
from urllib.parse import urlparse
from save_csv import save_csv_content


TMDB_DOMAINE = "https://www.themoviedb.org"
TMDB_TOP_URL = "https://www.themoviedb.org/movie/top-rated"

def get_movie_info(movie_url) -> list:
    # 1.send request, get details
    movie_res = requests.get(movie_url)

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