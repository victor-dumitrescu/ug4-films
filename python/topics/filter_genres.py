import re
import glob
from utils.filter_summaries import standardize_title


def main():

    # We will get the first max_films comedies/thriller plus any of the ScriptBase films which
    # weren't in the first max_films
    max_films = 10000
    remaining = []

    path = '/home/victor/GitHub/experiment/output/'
    for film in glob.glob(path + '*.gexf'):
        remaining.append(standardize_title(film[len(path):]))

    path = '/home/victor/GitHub/experiment/'
    out = open(path + 'genres/ids.txt', 'w')

    with open(path + 'movie.metadata.tsv', 'r') as meta:
        for row in meta:

            if max_films <= 0 and not len(remaining):
                break

            found_base = False
            for f in remaining:
                # get the wiki code if title matches one of the scripts from ScriptBase
                inf = re.search(r'(?P<wiki>\d+)\t(?P<fb>/m/\w*)\t%s' % f, row)
                if inf:
                    out.write(inf.group('wiki') + '\n')
                    out.flush()
                    max_films -= 1
                    remaining.remove(f)
                    found_base = True
                    break

            if max_films > 0 and not found_base:
                inf = row.split()[0]
                try:
                    if 'English' in re.search(r'\{\"/m/\w+\": \"(\w+) Language\"\}', row).groups():
                        genres = re.search(r'{.*}\t{.*}\t{(.*)}$', row).group(1)
                        if re.search(r'[tT]hriller|[cC]omedy', genres):
                            out.write(inf + '\n')
                            out.flush()
                            max_films -= 1
                except AttributeError:
                    pass

        print remaining

main()