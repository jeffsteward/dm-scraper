"""Script to gather Depeche Mode lyrics from AZ Lyrics."""
# References
# https://jeffknupp.com/blog/2014/02/04/starting-a-python-project-the-right-way/

import sys
import os
import requests
import random
from dotenv import load_dotenv
from time import sleep
from bs4 import BeautifulSoup

load_dotenv()

HEADERS = [{'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11'}]

CONCERTS = ['4bd7f392', '23d7bc13', '33c660f5', '7be282c8', '7beab678', '53b8b3c9']

def main():
	"""Main entry point for the script."""
	get_set_list(CONCERTS[0])

	URL = 'https://www.azlyrics.com/d/depeche.html' 
	songs = get_song_list(URL)

	with open('lyrics.txt', 'a+') as output:
		for title, url in songs:
			print(title, url)
			lyrics = get_lyrics_for_song(url)

			output.write("\n".join(lyrics))

def get_dm_info():
	mbid = '8538e728-ca0b-4321-b7e5-cff6565dd4c0'

	url = f'https://api.setlist.fm/rest/1.0/artist/{mbid}/setlists'

	header = {
		'x-api-key': os.getenv('SETLISTFM_API_KEY'),
		'Accept': 'application/json'
	}
	response = requests.get(url, headers = header)
	return response

def get_set_list(setlistid):
	setlist = []

	url = f'https://api.setlist.fm/rest/1.0/setlist/{setlistid}'

	header = {
		'x-api-key': os.getenv('SETLISTFM_API_KEY'),
		'Accept': 'application/json'
	}
	response = requests.get(url, headers = header)
	setlist = response.json()['sets']['set'][0]

	return setlist

def get_song_list(url):
	songs = []
	response = requests.get(url,  headers = HEADERS[0])
	soup = BeautifulSoup(response.text, 'html.parser')
	song_list = soup.find(id='listAlbum')
	for song in song_list.find_all('a', target='_blank'):
		songs.append((song.text, f'https://www.azlyrics.com{song["href"]}'))

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