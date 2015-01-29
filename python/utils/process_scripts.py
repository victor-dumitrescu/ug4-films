import re
import xml.etree.ElementTree as ET

def adjust(s):

    # hacky corrections for some merging issues
        s = re.sub(r' [nN][\'`][tT]', 'n\'t', s)
        s = re.sub(r'[Ii] [\'`][mM]', 'I\'m', s)
        s = re.sub(r' [\'`](ll|LL)', '\'ll', s)
        s = re.sub(r' [\'`](re|RE)', '\'re', s)
        s = re.sub(r' [\'`][sS]', '\'s', s)

        return s


def process_script(script_file):
    with open(script_file) as g:
        root = ET.parse(g).getroot()
        scenes = []
        for scene in root.findall('scene'):
            chars = set()
            speech_acts = []
            for speech_node in scene.findall('speech'):
                speaker = speech_node.attrib['speaker']
                chars.add(speaker)
                sentences = []
                for sent in speech_node[0].findall('sentence'):
                    if sent.attrib['type'] == 'normal':
                        word_list = sent.find('wordList').getchildren()
                        words = map((lambda x: x.text), word_list)
                        sent = adjust(' '.join(words))
                        sentences.append(sent)

                speech_acts.append((speaker, sentences))
            scenes.append((chars, speech_acts))

    # filter out scenes with no characters/dialogue
    scenes = filter((lambda x: x[0] != set()), scenes)
    return scenes
