# Import modules
import os
from glob import glob
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
    print('stopping all instances of video');
    try:
        os.system('pkill -9 -f "/usr/bin/omxplayer.bin"');
    except:
        print('Something went wrong. There was likely no player running in the killall process');



def isVideo(file):
    if file.endswith('.mp4') or file.endswith('.mov') or file.endswith('.avi') or file.endswith('.mkv') and isfile(file):
        return True
    else:
        return False

def buildTVShowList():
    print('building show directory');
    showsPath = "/media/pi/Untitled/TV Shows";
    series = glob(showsPath + '/*');
    showsDictionary = {};

    for series in series:
        seriesName = os.path.basename(os.path.normpath(series));
        episodes = glob(series + '/**/*.mp4', recursive=True) + glob(series + '/**/*.mkv', recursive=True) + glob(series + '/**/*.avi', recursive=True) + glob(series + '/**/*.mov', recursive=True);
        showsDictionary[seriesName] = episodes;

def getShowFromList(showList):
    series = list(showList); # convert dictionary to list for iterating
    series = random.choice(series);
    episode = random.choice(showList[series]);
    pprint(episode);
    return episode;

def playVideo(videoPath):
    print('initializing video');
    try:
        print('attempting to start the video');
        instance = OMXPlayer(videoPath);
        showLength = str(instance.duration());
        pprint(videoPath);
        pprint('show time: ' + showLength + 's');
    except Exception as e:
        print('something went wrong playing' + videoPath + ': ');
        print(e);
        instance = False;
    return instance;


def playRandomShowsMk2():
    stopAllOMXInstances();
    player = False;
    shows = buildTVShowList();
    episode = getShowFromList(shows);
    tvPlaying = True;

    while tvPlaying:
        print('show loop start');
        player = playVideo(episode);
        if player is not False:
            try:
                showLength = int(player.duration());
                sleep(showLength);
                player.quit();
                player = False;
                episode = getShowFromList(shows);
            except Exception as e:
                pprint('something went wrong in the show loop: ');
                print(e);
                tvPlaying = False;
        else:
            tvPlaying = False;



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


