# Import modules
import os
from glob import glob
from os.path import isfile
from os.path import isdir
import random
from omxplayer.player import OMXPlayer
from time import sleep
from pprint import pprint;
import datetime;

# TODO
# 2. Write schedule by getting current day, play movies on Sundays etc.
# 3. Find way to sort shows by type, to play episodes by type (cartoons on saturday, for example)
# 4. When video is nearly done, start a second instance of omx player behind the scenes, and reveal it when the first instance os over
# to prevent the gap between videos


def stopAllOMXInstances():
    print('stopping all instances of video');
    try:
        os.system('pkill -9 -f "/usr/bin/omxplayer.bin"');
    except:
        print('Something went wrong. There was likely no player running in the killall process');

def printPlayTime(time):
    print('playtime: ' + str(datetime.timedelta(seconds=time)));

def buildTVShowList():
    print('building show directory');
    showsPath = "/media/pi/Untitled/TV Shows";
    series = glob(showsPath + '/*');
    showsDictionary = {};

    for series in series:
        seriesName = os.path.basename(os.path.normpath(series));
        episodes = glob(series + '/**/*.mp4', recursive=True) + glob(series + '/**/*.mkv', recursive=True) + glob(series + '/**/*.avi', recursive=True) + glob(series + '/**/*.mov', recursive=True);
        showsDictionary[seriesName] = episodes;
    return showsDictionary;

def getShowFromList(showList):
    series = list(showList); # convert dictionary to list for iterating
    series = random.choice(series);
    episode = random.choice(showList[series]);
    pprint(episode);
    return episode;

def playRandomShows():
    stopAllOMXInstances();
    shows = buildTVShowList();
    tvPlaying = True;

    while tvPlaying:
        stableEpisode = False;
        while stableEpisode is False:
            try:
                print('attempting to find a playable episode.');
                episode = getShowFromList(shows);
                player = OMXPlayer(episode);
                printPlayTime(player.duration())
                stableEpisode = True;
            except Exception as e:
                stopAllOMXInstances();
                print('episode wasnt playable.');
                print(e);
                stableEpisode = False;

        showLength = int(player.duration());
        sleep(showLength);
        player.quit();
        #repeat



# MOVIES
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
    pprint(trueMovieList);
    return trueMovieList;


def playRandomMovies():
    movies = buildMovieList()
    player = OMXPlayer(random.choice(movies))

    while True:
        movieLength = player.duration()
        sleep(movieLength)
        player.stop()
        player = OMXPlayer(random.choice(movies))


