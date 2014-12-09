import re
import glob
from collections import namedtuple


def standardize_title(film):
    film = film[:-5]
    if re.match(r'.*\(film\)', film):
        film = film[:-7]
    elif re.match(r'.*\(\d{4}_film\)', film):
        film = film[:-12]

    film = film.replace('__', ': ')
    film = film.replace('_', ' ')

    # temporary hack
    # also changed the name of the .gexf for Silver_Linings_Playbook to The_[...]
    if film == "One Flew Over the Cuckoos Nest":
        film = "One Flew Over the Cuckoo's Nest"
    if film == "EDtv":
        film = "EdTV"
    if film == "Millers Crossing":
        film = "Miller's Crossing"
    if film == "The Hitchhikers Guide to the Galaxy":
        film = "The Hitchhiker's Guide to the Galaxy"
    if film == "Youve Got Mail":
        film = "You've Got Mail"

    return film


def script_titles():

    IDs = namedtuple('IDs', 'title, fb')
    remaining = []
    films = {}

    path = '../../experiment/output/'
    for film in glob.glob(path + '*.gexf'):
        remaining.append(standardize_title(film[len(path):]))

    with open('../movie.metadata.tsv', 'r') as meta:
        for row in meta:
            for f in remaining:
                inf = re.search(r'(?P<wiki>\d+)\t(?P<fb>/m/\w*)\t%s' % f, row)
                if inf:
                    films[inf.group('wiki')] = IDs(f, inf.group('fb'))
                    remaining.remove(f)
                    break

    return films


def main():

    path = '../../experiment'
    titles = script_titles()
    ids = titles.keys()
    print "Got %d film IDs." % len(ids)

    with open(path + 'movies.data', 'r') as data:
        with open(path + 'filtered.movies.data', 'w') as f_data:
            for row in data:
                data_id = re.search(r'^\d+', row).group(0)
                if data_id in ids:
                    f_data.write(row)
                    ids.remove(data_id)
                    f_data.flush()
    print "Filtered data file. "

    with open(path + 'filtered.meta.data', 'w') as f:
        for id in titles.keys():
            if id not in ids:
                f.write('%s %s %s\n' % (id, titles[id].fb, titles[id].title))
    print "Done"


main()
