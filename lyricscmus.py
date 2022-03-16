#!/usr/bin/env python3
import mutagen
import os
from pycmus import remote
from lyrics import *


def EmbedLyrics(audioFile, lyrics):
    print("")
    choice = input("Do you wish to embed the above lyrics in the file? [y/N]")
    try:
        if choice == "y" or choice == "Y":
            audioFile["LYRICS"] = lyrics
            audioFile.save()
            print("Tags updated sucefully")

    except TypeError:
        print("Failed to update tags")


def GetPosition(word, array):
    for position, line in enumerate(array):
        if word in line:
            return position


def GetLyrics(metadata):
    for string in lyrics_strings:
        if GetPosition(string, metadata) != None:
            return string


def LookUp(artist, title):
    def Choice():
        choice = input("\nDo you wish to look up for lyrics on another source? [y/N]")
        if choice == "y" or choice == "Y":
            return "y"
        else:
            return "n"

    try:
        lyrics = Genius(artist, title)
        print(lyrics)
        if Choice() == "n":
            return lyrics
    except AttributeError:
        pass

    try:
        os.system("clear")
        lyrics = Letras(artist, title)
        print(lyrics)
        if Choice() == "n":
            return lyrics
    except AttributeError:
        pass

    try:
        os.system("clear")
        lyrics = LetrasMus(artist, title)
        print(lyrics)
        if Choice() == "n":
            return lyrics
    except AttributeError:
        pass

    # Happens when LetrasMus can't handle foreign characters.
    except requests.exceptions.TooManyRedirects:
        pass

    os.system("clear")
    lyrics = AzLyrics(artist, title)
    print(lyrics)
    return lyrics


def DisplayLyrics(musicPath):
    metadata = tuple(mutagen.File(musicPath).tags)
    try:
        lyrics = GetLyrics(metadata)
        # Prints only the lyrics part and formats it nicely
        print("".join(metadata[GetPosition(lyrics, metadata)]).replace(lyrics, ""))

    except TypeError:
        try:
            print("Lyrics not found on file, looking for it online")
            print("")
            title = (cmus[GetPosition("tag title", cmus)].replace("tag title", "").strip())
            artist = (cmus[GetPosition("tag artist", cmus)].replace("tag artist", "").strip())
            lyrics = LookUp(artist, title)
            EmbedLyrics(mutagen.File(musicPath), lyrics)

        except AttributeError:
            print("Lyrics not found on the internet either :(")

        except requests.exceptions.ConnectionError:
            print("Couldn't connect to the internet :(")


def GetPath():
    os.system("clear")
    musicPath = cmus[1].split()  # Second line is path of the file
    musicPath.pop(0)  # Removes junk from the the list
    musicPath = " ".join(musicPath)
    return musicPath


if __name__ == "__main__":
    lyrics_strings = ("LYRICS", "UNSYNCEDLYRICS")  # String for lyrics tag on files
    cmus = remote.PyCmus().status().splitlines()  # Connect with Cmus
    DisplayLyrics(GetPath())

    # Compare the path of the song being played until it changes then update it
    while True:
        if cmus[1] != remote.PyCmus().status().splitlines()[1]:
            cmus = remote.PyCmus().status().splitlines()
            DisplayLyrics(GetPath())
