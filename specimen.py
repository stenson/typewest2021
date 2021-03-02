# Requires the `drafting` package (instructions on how to install in DrawBot in the README.md in this repository)

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
otf_path = "~/Type/fonts/fonts/Zetkin-Light.otf" # <- change to the path to the otf version of your font that you want to proof
caps = "DEHORV"
lowers = "agnopv"
designer_name = "Lorem J. Ipsum"
secondary_font = "SourceSerifPro-It"
language = "ukacd" # aka english
#language = "spanish"

####################################################
# Generic Functions
####################################################

font_name = installFont(str(Path(otf_path).expanduser()))

def capitalize(s):
    return s[0].upper() + s[1:].lower()

class Wordomatish():
    def __init__(self, caps, lows, seed=0):
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
        self.all_caps = []
        self.lowers = []
        
        cap_re = re.compile("^["+caps.lower()+"]{1}["+lows.lower()+"]+$")
        low_re = re.compile("^["+lows.lower()+"]+$")
        all_cap_re = re.compile("^["+caps.lower()+"]+$")
                   
        for word in self.all_words:
            if len(word) >= 2:
                word = word.lower()
                if cap_re.match(word):
                    self.caps.append(word)
                elif low_re.match(word):
                    self.lowers.append(word)
                elif all_cap_re.match(word):
                    self.all_caps.append(word)
       
    def random_sentence(self, all_caps = False):
        if all_caps and len(self.all_caps) > 0:
            txt = ""
            for x in range(self.rand.randint(3, 20)):
                txt += self.rand.choice(self.all_caps).upper() + " "
            return txt
        
        txt = capitalize(self.rand.choice(self.caps))
        for x in range(self.rand.randint(3, 20)): # random sentence length
            txt += self.rand.choice(self.lowers) + " "
        if False: # could check for existence of period
            txt = txt[:-1] + "."
        return txt

    def random_sentences(self, count, all_caps=False):
        return " ".join([self.random_sentence(all_caps) for x in range(0, count)])

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

wordomat = Wordomatish(caps, lowers, 0) # <- change the 0 here to get different random words

# Page 1
textarea = add_page()
fontSize(140)
lineHeight(120)
textBox(f"{caps}\n{lowers}", textarea)

# Page 2
textarea = add_page()
columns = textarea.subdivide_with_leading(2, 30, "mnx")
for idx, column in enumerate(columns):
    data, column = column.divide(20, "mxy")
    with savedState():
        fontSize(10)
        font(secondary_font)
        textBox(f"18pt", data, align="center")
    fontSize(18)
    txt = wordomat.random_sentences(20, all_caps=idx==0)
    textBox(txt, column)

# Page 3
textarea = add_page()
columns = textarea.subdivide_with_leading(3, 20, "mnx")
font_size = 14
for column in columns:
    data, column = column.divide(20, "mxy")
    with savedState():
        fontSize(10)
        font(secondary_font)
        textBox(f"{font_size}pt", data, align="center")
    fontSize(font_size)
    txt = wordomat.random_sentences(30)
    textBox(txt, column, align="left")
    font_size -= 2

now = datetime.today().strftime('%Y-%m-%d_%H%M')
filename = f"specimen_{font_name}_{now}.pdf"
if True: # flip this to False is you actually want versioned PDFs with the date in the filename
    filename = "speciment_test.pdf"
saveImage(f"~/Desktop/{filename}") # <- change ~/Desktop to whatever you want