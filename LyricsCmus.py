#!/usr/bin/env python3
import mutagen
import os
from pycmus import remote
from lyricsgenius import Genius

def EmbedLyrics(audioFile, lyrics):
    print('')
    choice = input('Do you wish to embed the above lyrics in the file? [y/N] ')
    try:
       if choice == 'y' or choice =='Y':
           audioFile['LYRICS'] = lyrics
           audioFile.save()
           print('Tags updated sucefully')
        
    except:
        print('Failed to update tags')

def GetPosition(word, array):
    position_of_word = 0
    for position, line in enumerate(array):
        if word in line:
            return position

def GetLyrics(metadata):
    for string in lyrics_strings:
        if GetPosition(string, metadata) > 0:
            return string
    
def DisplayLyrics(musicPath):
    metadata = tuple(mutagen.File(musicPath).tags)
    try:
        lyrics = GetLyrics(metadata)
        print(''.join(metadata[GetPosition(lyrics, metadata)]).replace(
            lyrics, '')) #Prints only the lyrics part and formats it nicely
        
    except TypeError:
        try:
            print('Lyrics not found on file, looking for it online')
            print('')
            title = cmus[GetPosition('tag title', cmus)].replace('tag title','')
            artist = cmus[GetPosition('tag artist', cmus)].replace('tag artist','')
            song = genius.search_song(title, artist)
            lyrics = (song.lyrics.replace('EmbedShare URLCopyEmbedCopy', ''))
            print(lyrics)
            EmbedLyrics(mutagen.File(musicPath), lyrics)
        
        except AttributeError:
           print('Lyrics not found on the internet either :(')

#Gets token for Genius.com api
def GetToken():
    token = ''
    #Get token from file for future convenience
    try:
        token_file = open('token.txt', 'r')
        for line in token_file:
            token += line
            
    #Writes token to file if no file exists
    except FileNotFoundError:
        token_file = open("token.txt","w")
        token = input('Insert token here: ')
        print(token, file=token_file)
        
    token_file.close()
    return token

def GetPath():
    os.system('clear')
    musicPath = (cmus[1].split()) #Second line is path of the file
    musicPath.pop(0) #Removes junk the the list
    musicPath = ' '.join(musicPath)
    return musicPath

genius = Genius(GetToken())
lyrics_strings = ('LYRICS', 'UNSYNCEDLYRICS') #String for lyrics tag on files
cmus = remote.PyCmus().status().splitlines() #Connect with Cmus
DisplayLyrics(GetPath())

#Compare the path of the song being played until it changes then update it
while True:
    if cmus[1] != remote.PyCmus().status().splitlines()[1]: 
        cmus = remote.PyCmus().status().splitlines()
        DisplayLyrics(GetPath())
