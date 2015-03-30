# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import glob
import numpy as np
import matplotlib.pyplot as plt
from utils.process_scripts import process_script
from utils.store_sentiment import dump, SentimentEvent
from unidecode import unidecode
from vaderSentiment.vaderSentiment import sentiment as vader

DEFAULT_MODE = 'compound'
plt.rcParams['font.size'] = 13
plt.rcParams['xtick.labelsize'] = 'small'
plt.rcParams['ytick.labelsize'] = 'small'
plt.rc('font', family='Sans')


def filter_events(timeline, c1, c2, mode=DEFAULT_MODE, cumulative=True):
    # return all the SentimentEvents from c1 to c2 [in y] and their timestamp [in x]
    x = []
    y = []
    for (i, event) in enumerate(timeline):
        if event.speaker == c1 and event.receiver == c2:
            x.append(i)
            if cumulative and len(y):
                    y.append(y[len(y)-1] + event.sentiment[mode])
            else:
                y.append(event.sentiment[mode])

    x = np.array(x)
    y = np.array(y)
    return x, y


def total_sentiment(timeline, char1, char2, mode=DEFAULT_MODE):

    _, values = filter_events(timeline, char1, char2, mode)
    return values[-1]


def fix_name(name):
    return ' '.join(map(lambda x: x[0] + x[1:].lower(), name.split()))

def plot_trajectory(timeline, char1, char2, mode=DEFAULT_MODE, title=None):
                                  # can also be 'pos', 'neg', 'neu'

    x, y = filter_events(timeline, char1, char2, mode)
    char1_points = plt.scatter(x, y, linewidth='0.5', s=60, c=(0.38, 0.75, 0.16, 0.55))
    x, y = filter_events(timeline, char2, char1, mode)
    char2_points = plt.scatter(x, y, linewidth='0.5', s=60, c=(0.82, 0.02, 0.03, 0.55))

    char1 = fix_name(char1)
    char2 = fix_name(char2)
    plt.legend([char1_points, char2_points], [char1 + ' ⟶ ' + char2, char2 + ' ⟶ ' + char1],
               loc='upper left', bbox_to_anchor=(0.5, 1.12),
               ncol=1, fancybox=True)
    if title:
        plt.title(title, x=0.1, y=1.035)
    plt.xlabel('Time (speech act)')
    plt.ylabel('Cumulative compound sentiment')
    plt.grid(True)
    plt.axhline(y=0, c="black", linewidth=0.7)
    plt.show()


def construct_timeline(script_file):

    scenes = process_script(script_file)

    timeline = []
    for scene in scenes:
        characters = scene[0]
        speech_acts = scene[1]
        for (i, turn) in enumerate(speech_acts):
            speaker = turn[0]
            try:
                # Vader doesn't accept Unicode input, turn it into closest ASCII char
                sentiment = vader(unidecode(' '.join(turn[1])))
            except UnicodeEncodeError:
                print turn[1]
                raise

            receiver = None
            if len(characters) == 2:
                # if there are only 2 characters, the other one is the receiver
                receiver = (set(characters) - set([speaker])).pop()
            elif len(speech_acts) > 1:
                # if it's the first speech act, the receiver is the next speaker,
                # otherwise, it's the previous speaker
                if i == 0:
                    receiver = speech_acts[i+1][0]
                else:
                    receiver = speech_acts[i-1][0]
            if receiver:
                timeline.append(SentimentEvent(speaker, receiver, sentiment))

    return timeline


def compute_sentiment():
    # construct the sentiment timelines of all processed scripts

    # reconstruct folder names of films for which there is a character graph
    path = '/home/victor/GitHub/ug4-films/output/'
    folders = []
    for film in glob.glob(path + '*.gexf'):
        film = film[len(path):-5]
        film = film.replace('__', ': ')
        film = film.replace('_', ' ')
        folders.append(film)

    path_drive = '/media/victor/SAMSUNG/ug4-films/base/'
    file_name = '/processed/script.xml'

    for i, film in enumerate(folders):
        script_file = path_drive + film + file_name
        timeline = construct_timeline(script_file)
        title = film.replace(': ', '__').replace(' ', '_')
        dump(title, timeline)
        print 'Dumped %d %s' % (i, title)