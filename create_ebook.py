from pathlib import Path
import itertools
import sys, os
import subprocess

outFile = "out.md"

def isWhitespace(line):
    return line.strip() == ""

def replaceTitle(line):
    if "TITLE" in line:
        title = line.replace("#+TITLE: ", "").replace(" tab", "")
        return f"<h3 class=\"chapter\">{title}</h3>"
    return line

def readlines(filename):
    with open(filename, "r") as f:
        lines = f.readlines()
        endIndex = [i for (i, line) in enumerate(lines) if "[END BOOK]" in line]
        if len(endIndex) > 0:
            return lines[:endIndex[0]]
        else:
            return lines
            

def getTitle(content):
    for line in content:
        if "TITLE" in line:
            title = line.replace("#+TITLE: ", "").replace(" tab", "")
            return title

def replaceWeirdCharacters(line):
    return line.replace("’", "'").replace("“", "\"").replace("”", "\"")

def filterLines(lines):
    # Filter note links
    lines = [line for line in lines if "file:" not in line]
    # Filter section annotations, takes up too much space
    lines = [line for line in lines if not ("[" in line and "]" in line)]
    # Filter out multiple empty lines
    grouped = itertools.groupby(lines, isWhitespace)
    lines = [item for group in grouped for item in (group[1] if not group[0] else ["\n"])]
    return lines


def createEbook(inputFiles):
    contents = [readlines(f) for f in inputFiles]
    contents.sort(key=lambda content: getTitle(content))
    lines = [line for content in contents for line in content]
    lines = [replaceWeirdCharacters(line) for line in lines]
    lines = [replaceTitle(line) for line in lines]
    lines = filterLines(lines)
    with open(outFile, "w") as f:
        result = "".join(lines)
        f.write(result)
    os.system(f"ebook-convert {outFile} out.epub --markdown-extensions=nl2br --no-default-epub-cover --title chords --authors tehforsch")
    os.unlink(outFile)

def findTabNotes():
    folder = Path("/home/toni/notes")
    note = folder / "20220930114446-chords.org"
    result = subprocess.getoutput(f"pundit {folder} list-backlinks --show-path {note}")
    return result.split("\n")


inputFiles = findTabNotes()
createEbook(inputFiles)
