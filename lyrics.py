import requests
from bs4 import BeautifulSoup


def Formatter(string):
    new_string = "-".join(string.split()).replace("'", "").lower()
    return new_string


def Letras(artist_input, song_input):
    artist = Formatter(artist_input)
    song = Formatter(song_input)
    response = requests.get(f"https://www.letras.com.br/{artist}/{song}")
    html = response.content
    soup = BeautifulSoup(html, "html.parser")
    lyrics = str(soup.find("print-component").attrs[":lyrics"]).strip("`")
    return lyrics


def Genius(artist_input, song_input):
    artist = Formatter(artist_input)
    song = Formatter(song_input)
    response = requests.get(f"https://genius.com/{artist}-{song}-lyrics")
    html = response.content
    soup = BeautifulSoup(html, "html.parser")
    lyrics = "".join(
        [
            div.get_text(strip=True, separator="\n")
            for div in soup.select('div[class^="Lyrics__Container"]')
        ]
    )

    if lyrics == '':
        raise AttributeError()
    return lyrics


def LetrasMus(artist_input, song_input):
    artist = Formatter(artist_input)
    song = Formatter(song_input)
    response = requests.get(f"https://www.letras.mus.br/{artist}/{song}.html/")
    html = response.content
    soup = BeautifulSoup(html, "html.parser")
    lyrics = soup.find("div", {"class": "cnt-letra p402_premium"}).get_text(
        separator="\n"
    )
    return lyrics


def AzLyrics(artist_input, song_input):
    artist = Formatter(artist_input).replace("-", "")
    song = Formatter(song_input).replace("-", "")
    response = requests.get(f"https://www.azlyrics.com/lyrics/{artist}/{song}.html")
    html = response.content
    soup = BeautifulSoup(html, "html.parser")
    lyrics = (
        soup.find("div", class_="col-xs-12 col-lg-8 text-center")
        .find("div", class_=None)
        .text
    )
    return lyrics
