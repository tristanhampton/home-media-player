# Import the os module
import os
import glob
from os.path import isfile
from os.path import isdir
import random
from omxplayer.player import OMXPlayer
# from pathlib import Path
from time import sleep

# Path to media hard drive
path = "/media/pi/Untitled"
movies = path + "/Movies/*"



def isVideo(file):
    if file.endswith('.mp4') or file.endswith('.mov') or file.endswith('.avi') or file.endswith('.mkv') and isfile(file):
        return True
    else:
        return False



def buildMovieList():
    # Get list of files in movie directory
    tempMovieList = glob.glob(movies)
    trueMovieList = []

    # go through files, if it's a file add to array. if not, go into folder and check for files and add
    for movie in tempMovieList:
        if isfile(movie):
            trueMovieList.append(movie)
        else:
            cPath = movie
            os.chdir(movie)
            for file in os.listdir():
                if file.endswith('.mp4') or file.endswith('.mkv') or file.endswith('.avi'):
                    filePath = cPath + '/' +  file
                    trueMovieList.append(filePath)

    return trueMovieList;


def playRandomMovies():
    movies = buildMovieList()
    # play random movie
    player = OMXPlayer(random.choice(movies))

    while True:
        movieLength = player.duration()
        sleep(movieLength)
        player = OMXPlayer(random.choice(movies))


def buildTVShowList():
    showsPath = "/media/pi/Untitled/TV Shows/*"
    showsGlob = glob.glob(showsPath)
    shows = []

    # print(showsGlob)

    for show in showsGlob:
        # Each show should be a directory, so move into it to check for episodes or seasons
        showPath = show
        os.chdir(showPath)
        currentFolder = os.listdir()

        for item in currentFolder:
            # there might be episodes here, but usually seasons. Add episodes to list and continue
            if isVideo(item):
                shows.append(showPath + '/' + item)
            elif isdir(item):
                showPath = showPath + '/' + item
                os.chdir(item)
                currentFolder = os.listdir()
                for item in currentFolder:
                    if isVideo(item):
                        shows.append(showPath + '/' + item)
                    elif isdir(item):
                        showpath = showPath + '/' + item
                        os.chdir(item)
                        currentFolder = os.listdir();
                        for item in currentFolder:
                            if isVideo(item):
                                shows.append(showPath + '/' + item)

    return shows


def playRandomShows():
    shows = buildTVShowList();
    player = OMXPlayer(random.choice(shows))

    while True:
        showLength = player.duration();
        sleep(showLength)
        player = OMXPlayer(random.choice(shows))


