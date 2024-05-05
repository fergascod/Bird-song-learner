# Bird Song Learner
This project consists in designing an application that allows its users to practice their bird identification skills using the [xeno-canto API](https://www.xeno-canto.org/explore/api). The app is deployed at [https://ferbirder.pythonanywhere.com/](https://ferbirder.pythonanywhere.com/), check it out!

List of used Spanish birds from SEO birdlife can be found [here](https://seo.org/listaavesdeespana/) and Catalan bird names [here](http://www.rarebirds.cat/catalan-bird-list-ocells-de-catalunya-2020/).

## REQUIRED MODULES

To install the required modules using a virtual environment:

> ```
> python3 -m venv env_name
> source env_name/bin/activate
> pip install -r requirements.txt
> ```

The scripts use the `vlc` library (to reproduce the audio files) which is a VLC binding for Python, meaning **having VLC installed is also a prerequisite**. Follow the following [link](https://www.videolan.org/vlc/download-ubuntu.html) to install it. 

Important: in order to execute the game you need Internet connectivity to be enabled.

## USE

Clone the repository using:

> ```
> git clone https://github.com/fergascod/Bird-song-learner.git
> ```

This will create a directory called `Bird-song-learner` with everything you need to play the Bird Song Learner game.

Move into the directory we just created using:

> ```
> cd Bird-song-learner
> ```

Then just execute the Flask app:
> ```
> flask --app app run
> ```

The program will be running in http://127.0.0.1:5000 use your browser of choice to open the app.


TODO:
- Some trouble with VLC if going through questions fast:
  - [00007f361010a6e0] prefetch stream error: reading while paused (buggy demux?)
  - [000073466000c190] http stream error: local stream 1 error: Cancellation (0x8)
- Issues when selecting modes
