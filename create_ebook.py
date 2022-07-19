from pathlib import Path
import sys, os
import subprocess

outFile = "out.md"

def replaceTitle(line):
    if "TITLE" in line:
        title = line.replace("#+TITLE: ", "").replace(" tab", "")
        return f"<h1>{title}</h1>"
    return line

def readlines(filename):
    with open(filename, "r") as f:
        return f.readlines()

def getTitle(content):
    for line in content:
        if "TITLE" in line:
            title = line.replace("#+TITLE: ", "").replace(" tab", "")
            return title

def createEbook(inputFiles):
    contents = [readlines(f) for f in inputFiles]
    contents.sort(key=lambda content: getTitle(content))
    lines = [line for content in contents for line in content]
    lines = [replaceTitle(line) for line in lines]
    lines = [l for l in lines if not "[[" in l]
    with open(outFile, "w") as f:
        result = "".join(lines)
        f.write(result)
    os.system(f"ebook-convert {outFile} out.epub --markdown-extensions=nl2br ")
    os.unlink(outFile)

def findTabNotes():
    folder = Path("/home/toni/notes")
    note = folder / "20201025191841-tab.org"
    result = subprocess.getoutput(f"pundit {folder} list-backlinks --show-path {note}")
    return result.split("\n")


inputFiles = findTabNotes()
createEbook(inputFiles)
