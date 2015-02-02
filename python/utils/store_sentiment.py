from collections import namedtuple

SentimentEvent = namedtuple('SentimentEvent', ['speaker', 'receiver', 'sentiment'])
# 'sentiment' is a dictionary with files 'neg', 'neu', 'pos', 'compound'

def dump(title, timeline):

    path = '/home/victor/GitHub/experiment/sentiment/'
    with open(path + title + '.csv', 'w+') as f:
        f.write('speaker,receiver,neg,neu,pos,compound\n')
        for event in timeline:
            f.write(','.join([event.speaker,
                              event.receiver,
                              str(event.sentiment['neg']),
                              str(event.sentiment['neu']),
                              str(event.sentiment['pos']),
                              str(event.sentiment['compound'])
                             ]).encode('utf8') + '\n')


def load(f_name):

    path = '/home/victor/GitHub/experiment/sentiment/'
    timeline = []
    with open(path + f_name + '.csv', 'r') as f:
        f.readline()
        for line in f:
            vals = line.split(',')
            sentiment = dict(zip(['neg', 'neu', 'pos', 'compound'], map(float, vals[-4:])))
            event = SentimentEvent(vals[0], vals[1], sentiment)
            timeline.append(event)

    return timeline