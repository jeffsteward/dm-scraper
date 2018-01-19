"""Script to gather Depeche Mode lyrics from AZ Lyrics."""
# References
# https://jeffknupp.com/blog/2014/02/04/starting-a-python-project-the-right-way/

import sys
import requests
import random
from time import sleep
from bs4 import BeautifulSoup

HEADERS = [{'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11'}]

def main():
	"""Main entry point for the script."""
	URL = 'https://www.azlyrics.com/d/depeche.html' 

	songs = get_song_list(URL)

	with open('lyrics.txt', 'a+') as output:
		for title, url in songs:
			print(title, url)
			lyrics = get_lyrics_for_song(url)

			output.write("\n".join(lyrics))

def get_song_list(url):
	songs = []
	response = requests.get(url,  headers = HEADERS[0])
	soup = BeautifulSoup(response.text, 'html.parser')
	song_list = soup.find(id='listAlbum')
	for song in song_list.find_all('a', target='_blank'):
		songs.append((song.text, song['href'].replace('../', 'https://www.azlyrics.com/')))

	return songs

def get_lyrics_for_song(url):
    sleep(random.randint(0,20))

    response = requests.get(url, headers = HEADERS[0],)
        
    soup = BeautifulSoup(response.content, 'html.parser')
    
    lyrics_tags = soup.find_all("div", attrs={"class": None, "id": None})
    lyrics = [tag.getText() for tag in lyrics_tags]
    return lyrics

if __name__ == '__main__':
    sys.exit(main())