from bs4 import BeautifulSoup
import requests

wiki_band_urls = [
    "https://en.wikipedia.org/wiki/List_of_death_metal_bands,_!%E2%80%93K",
    "https://en.wikipedia.org/wiki/List_of_death_metal_bands,_L–Z",
    "https://en.wikipedia.org/wiki/List_of_black_metal_bands,_0–K",
    "https://en.wikipedia.org/wiki/List_of_black_metal_bands,_L–Z",
    "https://en.wikipedia.org/wiki/List_of_doom_metal_bands",            
]

def get_wiki_page_bands(url):
    r = requests.get(url)
    text = r.text
    soup = BeautifulSoup(text)
    sups = soup.select("ul li sup")
    band_names = []
    for sup in sups:
        band_names.append(sup.parent.a.text)
    return band_names

def get_all_wiki_pages():
    bands = []
    for url in wiki_band_urls:
        bands += get_wiki_page_bands(url)
    bands = list(set(bands))
    bands.sort()
    return bands

if __name__ == "__main__":
    bands = get_all_wiki_pages()
    for band in bands:
        print(band)


