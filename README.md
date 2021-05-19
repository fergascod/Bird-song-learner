# Bird Song Learner
This project consists in designing an application that allows its users to practice their bird identification skills using the [xeno-canto API](https://www.xeno-canto.org/explore/api).

List of used Spanish birds from SEO birdlife can be found [here](https://seo.org/listaavesdeespana/) and Catalan bird names [here](http://www.rarebirds.cat/catalan-bird-list-ocells-de-catalunya-2020/).

## REQUIRED MODULES

To install the required modules use:

> ```
> pip install -r requirements.txt
> ```

The scripts use the `vlc` library (to reproduce the audio files) which is a VLC binding for Python, meaning **having VLC installed is also a prerequisite**. Follow the following [link](https://www.videolan.org/vlc/download-ubuntu.html) to install it 

Important: in order to execute the game you need Internet connectivity to be enabled.

## INSTALLATION

Clone the repository using:

> ```
> git clone https://github.com/fergascod/Bird-song-learner.git
> ```

This will create a directory called `Bird-song-learner` with everything you need to play the Bird Song Learner game.

## USE

Move into the directory we just created using:

> ```
> cd Bird-song-learner
> ```

Then just execute:
> ```
> python3 play.py
> ```

The program will guide you from that point on.


TODO:
- Some trouble with VLC if going through questions fast:
  - [00007f361010a6e0] prefetch stream error: reading while paused (buggy demux?)
