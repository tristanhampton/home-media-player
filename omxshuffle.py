# Import modules
import os
import glob
from os.path import isfile
from os.path import isdir
import random
from omxplayer.player import OMXPlayer
from time import sleep
from pprint import pprint;

# TODO
# 1. Choose random episodes by show rather than file to prevent long series from taking over the server
# 2. Write schedule by getting current day, play movies on Sundays etc.
# 3. Find way to sort shows by type, to play episodes by type (cartoons on saturday, for example)
# 4. When video is nearly done, start a second instance of omx player behind the scenes, and reveal it when the first instance os over
# to prevent the gap between videos


def stopAllOMXInstances():
    try:
        os.system('killall omxplayer.bin && pkill python && pgrep python && kill $(pgrep omxplayer)');
    except:
        print('Something went wrong. There was likely no player running in the killall process');



def isVideo(file):
    if file.endswith('.mp4') or file.endswith('.mov') or file.endswith('.avi') or file.endswith('.mkv') and isfile(file):
        return True
    else:
        return False


def buildTVShowList():
    showsDictionary = {}
    showsPath = "/media/pi/Untitled/TV Shows"
    os.chdir(showsPath)
    for series in os.listdir():
        if not isfile(series) and not series.startswith('.'):
            firstLevelPath = showsPath + '/' + series; # /media/pi/Untitled/TV Shows/Parks and Rec
            os.chdir(firstLevelPath);
            episodes = []
            for firstItem in os.listdir():
                # might have episodes here, so handle that
                if isVideo(firstItem):
                    episodes.append(firstItem);
                elif not isfile(firstItem):
                    secondLevelPath = firstLevelPath + '/' + firstItem; # /media/pi/Untitled/TV Shows/Parks and Rec/Season 01/
                    os.chdir(secondLevelPath)
                    for secondItem in os.listdir():
                        if isVideo(secondItem):
                            episodes.append(secondLevelPath + '/' + secondItem)
                        elif not isfile(secondItem):
                            thirdLevelPath = secondLevelPath + '/' + secondItem;
                            os.chdir(thirdLevelPath);
                            for thirdLevelItem in os.listdir():
                                if isVideo(thirdLevelItem):
                                    episodes.append(thirdLevelPath + '/' + thirdLevelItem);
                showsDictionary[series] = episodes
    return showsDictionary;

def getShowFromList(showList):
    series = list(showList); # convert dictionary to list for iterating
    series = random.choice(series);
    episode = random.choice(showList[series]);
    return episode

def playVideo(videoPath):
    try:
        return OMXPlayer(videoPath);
    except:
        return False;


def playRandomShowsMk2():
    stopAllOMXInstances();
    player = False;
    shows = buildTVShowList();
    episode = getShowFromList(shows);

    # this logic can probably be moved into the playVideo function
    while player == False:
        player = playVideo(episode);

    while True:
        showLength = int(player.duration());
        sleep(showLength);
        player.quit();
        player = False;
        episode = getShowFromList(shows);

        while player  == False:
            player = playVideo(episode);


def buildMovieList():
    movies = "/media/pi/Untitled/Movies/*"
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
        player.stop()
        player = OMXPlayer(random.choice(movies))


def playRandomShows():
    stopAllOMXInstances();
    shows = buildTVShowList();
    episode = getShowFromList(shows);
    player = OMXPlayer(episode);

    while True:
        showLength = int(player.duration());
        sleep(showLength);
        player.quit();
        episode = getShowFromList(shows);
        player = OMXPlayer(episode);


