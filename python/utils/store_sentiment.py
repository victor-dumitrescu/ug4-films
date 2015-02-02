from collections import namedtuple

SentimentEvent = namedtuple('SentimentEvent', ['speaker', 'receiver', 'sentiment'])

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


def load(title):

    path = '/home/victor/GitHub/experiment/sentiment/'
    with open(path + title + '.csv', 'r') as f:
        pass
        #TODO Load the CSV file as a list of SentimentEvents