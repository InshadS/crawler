import requests
from bs4 import BeautifulSoup
import os

def get_artists(url):
    ret =[]
    r = requests.get(url) #get the url
    body = r.content
    soup = BeautifulSoup(body, features="html.parser") #create soup
    tracklist = soup.find("table", {"class": "tracklist"}) #find the tracklist table
    links = tracklist.find_all("a") #find all the links in the tracklist table
    for i in links:
        ret.append((i.text, i['href'])) #get all the text and URLs in the list of links and add them to ret
    return ret #ret will be the list of artists 

def get_songs(artist_url):
    songs=[]
    r = requests.get(artist_url)
    body = r.content
    soup = BeautifulSoup(body, features="html.parser")
    tracklists = soup.find("table", {"class" : "tracklist"})
    links=tracklists.find_all("a")
    for i in links:
        songs.append((i.text,i['href']))
    return songs

def get_lyrics(song_url):
    r = requests.get(song_url)
    body = r.content
    soup = BeautifulSoup(body, features="html.parser")
    lyrics_div = soup.find("p", {"id": "songLyricsDiv"})
    lyrics = lyrics_div.text
    return lyrics

def crawl():
    base_dir = "lyrics"
    try:
        os.mkdir(base_dir)
    except Exception:
        pass
    artists= get_artists("https://www.songlyrics.com/a/")
    for name, link in artists:
        print(name, "   :   ",link)
        name_dir = os.path.join(base_dir, name.replace(" ", "_").lower())
        try:
            os.mkdir(name_dir)
        except Exception:
            pass
        songs = get_songs(link)
        for song, song_link in songs:
            lyrics = get_lyrics(song_link)
            song_file = os.path.join(name_dir, song.replace(" ", "_").lower()+".txt")
            with open(song_file, "w") as f:
                f.write(lyrics)
            print (".", end="", flush=True)
        print("DONE")
    
if __name__=="__main__":
    crawl()
