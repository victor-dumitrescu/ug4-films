import re
import glob
from lxml import etree

# path to Philip's scripts
PATH = '/media/victor/SAMSUNG/ug4-films/base/'


def make_scene(lines, scene_count, scene_whitespace):

    def speech_marker(l):
        is_correct_format = l.isupper() and not re.match(r'\(.*\)', l.strip())
        return is_correct_format and len(re.match(r'^\s*', l).group(0)) > scene_whitespace

    def format_char_name(l):
        for match in re.findall(r'\(.*\)', l):
            l = l.replace(match, '')
        return l.strip()

    # while i < len(lines):
    #     line = lines[i]
    #     if scene_marker(line):
    #         if scene:
    #             script.append(scene)

    if lines[0].startswith(':SC:'):
        # for scripts processed by Philip
        sd = lines[0][5:].strip()
    else:
        sd = lines[0].strip()

    scene = etree.Element('scene', attrib={'count': str(scene_count)})  # build scene node
    stage_direction = etree.Element('stageDirection', attrib={'count': '0'})
    stage_direction.text = sd
    scene.append(stage_direction)  # add stage direction to current scene

    return scene

        # elif speech_marker(line):
        #     print format_char_name(line)
        #
        # else:
        #     text += line.strip().replace('\n', ' ')



def process_script(title, lines):

    def scene_marker(l):
        is_correct_format = re.match(r':SC:|INT[. ]|EXT[. ]|FADE (IN|OUT)|.*( DAY | NIGHT ).*', l.strip()) and l.isupper()
        if not scene_whitespace:
            return is_correct_format
        else:
            return is_correct_format and len(re.match(r'^\s*', l).group(0)) == scene_whitespace

    script = etree.Element('script', attrib={'title': title})
    scene_count = 0
    scene_whitespace = None

    scene_stops = []
    for (n, line) in enumerate(lines):
        if scene_marker(line):
            scene_stops.append(n)
            if not scene_whitespace:
                scene_whitespace = len(re.match(r'^\s*', line).group(0))

    print scene_stops, scene_whitespace
    for (n, s) in enumerate(scene_stops):
        try:
            ls = lines[s: scene_stops[n+1]]
        except IndexError:
            ls = lines[s:]
        scene_count += 1
        scene = make_scene(ls, scene_count, scene_whitespace)
        script.append(scene)

    print etree.tostring(script, pretty_print=True)


def gen_scripts(limit=None):

    if limit:
        done = 0

    for path in glob.glob(PATH + '*/processed/script_clean.txt'):
        title = path[len(PATH):-len('/processed/script_clean.txt')]

        # need to preserve whitespace in front of lines in order to identify chars speaking
        lines = []
        with open(path, 'r') as script:
            for line in script:
                lines.append(line)

        if limit:
            if done == limit:
                return
            done += 1

        yield (title, lines)

    return


def main():

    scripts = gen_scripts(limit=2)

    try:
        while True:
            script = next(scripts)
            process_script(*script)

    except StopIteration:
        pass

main()
# scene markers:
# INT.
# EXT.
# FADE IN
# FADE OUT