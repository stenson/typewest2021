from drafting.geometry import Rect
from datetime import datetime
from pathlib import Path
from random import Random
import re

wordomat_languages = [
    "catalan", "czech", "danish", "dutch", "finnish", "french", "german",
    "hungarian", "icelandic", "italian", "latin", "norwegian", "polish",
    "slovak", "spanish", "ukacd", "vietnamese"]

####################################################
# Variables to tweak
####################################################
otf_path = "~/Type/fonts/fonts/Zetkin-Light.otf"
characters = """
    DEHORV
    agnopv
"""
designer_name = "Lorem J. Ipsum"
secondary_font = "SourceSerifPro-It"
language = "ukacd" # aka english
language = "spanish"

####################################################
# Generic Functions
####################################################

font_name = installFont(str(Path(otf_path).expanduser()))
characters = "\n".join([c.strip() for c in characters.strip().splitlines()])

def capitalize(s):
    return s[0].upper() + s[1:].lower()

class Wordomatish():
    def __init__(self, characters, seed=0):
        self.seed = seed
        self.rand = Random(self.seed)
        
        path = "~/Library/Application Support/RoboFont/plugins/word-o-mat.roboFontExt"
        wordomat = Path(path).expanduser()
        wordsfile = wordomat / "resources"/ (language + ".txt")
        self.all_words = (wordsfile
            .read_text(encoding="utf-8")
            .split("*****\n")[-1]
            .splitlines())

        self.caps = []
        self.lowers = []
        
        caps, lows = characters.split("\n")
        cap_re = re.compile("^["+caps.lower()+"]{1}["+lows.lower()+"]+$")
        low_re = re.compile("^["+lows.lower()+"]+$")
                       
        for word in self.all_words:
            if len(word) > 2:
                word = word.lower()
                if cap_re.match(word):
                    self.caps.append(word)
                elif low_re.match(word):
                    self.lowers.append(word)
       
    def random_sentence(self):
        txt = capitalize(self.caps[self.rand.randint(0, len(self.caps)-1)])
        for x in range(self.rand.randint(3, 20)):
            txt += self.lowers[self.rand.randint(0, len(self.lowers)-1)] + " "
        txt = txt[:-1] + "."
        return txt

    def random_sentences(self, count):
        return " ".join([self.random_sentence() for x in range(0, count)])

page_count = 0

def add_page():
    global page_count
    page_count += 1
    newPage("LetterLandscape")
    page = Rect(width(), height()).inset(30, 30)
    labels, textarea = page.divide(20, "mny")
    
    with savedState():
        stroke(0.9)
        strokeWidth(1)
        line(*labels.en)

    with savedState():
        now = datetime.today().strftime('%Y/%m/%d %H:%M')
        fontSize(10)
        font(secondary_font)
        text(f"{designer_name} / Type West", labels.psw)
        text(font_name, labels.ps, align="center")
        text(f"{now} — Pg.{page_count}",
            labels.pse, align="right")
        
    font(font_name)
    return textarea.subtract(30, "mny")

####################################################
# The Actual Typesetting (very tweakable)
####################################################

wordomat = Wordomatish(characters, 0) # <- change the 0 here to get different random words

# Page 1
textarea = add_page()
fontSize(140)
lineHeight(120)
textBox(characters, textarea)

# Page 2
textarea = add_page()
columns = textarea.subdivide_with_leading(2, 30, "mnx")
for column in columns:
    fontSize(18)
    txt = wordomat.random_sentences(20)
    textBox(txt, column)

# Page 3
textarea = add_page()
columns = textarea.subdivide_with_leading(3, 20, "mnx")
font_size = 14
for column in columns:
    fontSize(font_size)
    txt = wordomat.random_sentences(30)
    textBox(txt, column, align="left")
    font_size -= 2

saveImage("~/specimen_test.pdf") # <- change this to whatever you want