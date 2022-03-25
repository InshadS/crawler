import requests
from bs4 import BeautifulSoup
import psycopg2

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
    conn = psycopg2.connect("dbname=lyrics")
    cur = conn.cursor()
    artists= get_artists("https://www.songlyrics.com/a/")
    for name, link in artists[:10]:
        cur.execute("INSERT INTO artist (artist_name) VALUES (%s);", (name,))
        print(name, "   :   ",link)
        songs = get_songs(link)
        for song, song_link in songs[:10]:
                lyrics = get_lyrics(song_link)
                cur.execute("INSERT INTO song (artist,song_name, lyrics) VALUES ((select artist_id from artist where artist_name=%s),%s,%s);", (name,song,lyrics))
    conn.commit()
    print("DONE")
    
if __name__=="__main__":
    crawl()
