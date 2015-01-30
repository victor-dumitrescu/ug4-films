from utils.process_scripts import process_script
from collections import namedtuple
from vaderSentiment.vaderSentiment import sentiment as vader

import numpy as np
import matplotlib.pyplot as plt

SentimentEvent = namedtuple('SentimentEvent', ['speaker', 'receiver', 'sentiment'])


def plot_trajectory(char1, char2, mode='compound'):
                                  # can also be 'pos', 'neg', 'neu'

    def filter_events(c1, c2):
        x = []
        y = []
        for (i, event) in enumerate(timeline):
            if event.speaker == c1 and event.receiver == c2:
                x.append(i)
                if len(y):
                    y.append(y[len(y)-1] + event.sentiment[mode])
                else:
                    y.append(event.sentiment[mode])

        x = np.array(x)
        y = np.array(y)
        return x, y

    x, y = filter_events(char1, char2)
    char1_points = plt.scatter(x, y, c='blue')
    x, y = filter_events(char2, char1)
    char2_points = plt.scatter(x, y, c='red')

    plt.legend([char1_points, char2_points], [char1, char2])
    plt.show()


script_file = '../../base2/The Silence of the Lambs (film)/processed/script.xml'
# script_file = '../../base2/A Nightmare on Elm Street 3: Dream Warriors/processed/script.xml'

scenes = process_script(script_file)

timeline = []
for scene in scenes:
    characters = scene[0]
    speech_acts = scene[1]
    for (i, turn) in enumerate(speech_acts):
        speaker = turn[0]
        sentiment = vader(' '.join(turn[1]))

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