import re
import string
import urllib2
import cPickle as pickle
from bs4 import BeautifulSoup

from films import Film, construct_films
from personas import Persona


FILM_LINK = 'http://tvtropes.org/pmwiki/pmwiki.php/Film/'
TROPE_LINK = r'.*http://tvtropes.org/pmwiki/pmwiki.php/Main/.*'

COMIC_LINK = 'http://tvtropes.org/pmwiki/pmwiki.php/ComicBook/'

path = '/home/victor/GitHub/experiment/tropes/'


def get_tropes_for_film(film):

    # hardcoded exceptions:
    if film == "Benny & Joon":
        film = "Benny And Joon"
    elif film == "Seven":
        film = "Se7en"
    elif film == "The Silver Linings Playbook":
        film = "Silver Linings Playbook"
    elif film == "Evil Dead II":
        film = "Evil Dead 2"
    elif film == "Analyze That":
        film = "Analyze This"

    # remove spaces and punctuation from title
    film = film.translate(None, string.punctuation)
    film = film.translate(None, string.whitespace)

    data = urllib2.urlopen(FILM_LINK + film).read()
    if film == "GhostWorld":
        data = urllib2.urlopen(COMIC_LINK + film).read()
    soup = BeautifulSoup(data)

    # get the div which holds the wiki article
    text = soup.find('div', {'id': "wikitext"})

    # find all links and filter out those which that aren't tropes
    tropes = filter(lambda x: re.match(TROPE_LINK, x.__str__()), text.find_all(class_='twikilink', recursive=True))

    # extract the name of each trope
    clean_tropes = map(lambda x: x.attrs['href'][len(FILM_LINK):], tropes)

    return clean_tropes


def analyze_tropes():

    from collections import defaultdict
    tropes = pickle.load(open(path + 'tropes.pickle', 'r'))

    all_tropes = defaultdict(int)
    for f in tropes:
        for t in tropes[f]:
            all_tropes[t] += 1

    s = sorted(all_tropes.items(), key=lambda x: x[1], reverse=True)


def main():

    failures = []
    tropes = {}

    films = construct_films()
    for f in films:
        title = films[f].title
        print title

        try:
            tropes[title] = get_tropes_for_film(title)

        except:
            failures.append(title)

    pickle.dump(tropes, open(path + 'tropes.pickle', 'w'))