# Home Media Player
This script is meant to be run on a Raspberry Pi. I wrote it to randomly play my favourite shows and movies on a continuous loop, rather than scrolling through netflix to play something in the background while I'm at home.

## Remote Functions
To start playing random shows use the following function on the Raspberry Pi
`python3 -c 'from omxshuffle import playRandomShows; playRandomShows()'`