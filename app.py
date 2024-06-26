#!/usr/bin/env python

import flask
from flask import request, redirect, url_for, send_from_directory, session

import random as rand
import os

from modes import modes
from utils import loadRecordings, catalanNames


# Create the application.
APP = flask.Flask(__name__)
APP.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

@APP.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(APP.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')
@APP.route('/question')
def question():
    num, max_num, game_mode = session["num"], session["max_num"], session["game_mode"]
    targetList=modes[game_mode]
    recordings=loadRecordings()
    scientificToCatalan=catalanNames()
    possibilities=rand.sample(targetList, 5 if 5<len(targetList) else len(targetList))
    spLatin=rand.choice(possibilities)
    if len(recordings[spLatin])!=0:
        url="https:"+rand.choice(recordings[spLatin])
    if int(num)<=int(max_num):
        possibilities=[scientificToCatalan[sp] for sp in possibilities]
        spLatin=scientificToCatalan[spLatin]
        return flask.render_template('question.html', 
                                    num=num, max_num = max_num, 
                                    game_mode=game_mode, possibilites=possibilities, 
                                    correct=spLatin,  url=url)
    else:
        return redirect(url_for("menu"))

@APP.route('/results')
def results():
    correct, max_num, game_mode = session["correct"], session["max_num"], session["game_mode"]
    return flask.render_template('results.html', 
                                correct=correct, max_num = max_num, 
                                game_mode=game_mode)

@APP.route('/response/<response>/<correct>')
def response(response, correct):
    num, max_num, game_mode = session["num"], session["max_num"], session["game_mode"]
    session["num"]+=1
    if response==correct: session["correct"]+=1
    return flask.render_template('response.html', 
                                num=num, max_num = max_num, 
                                game_mode=game_mode, response=response,
                                correct=correct)


@APP.route('/form')
def form():
    scientificToCatalan=catalanNames()
    print(scientificToCatalan.values(), flush=True)
    return flask.render_template('form.html', game_modes=modes.keys(), species=scientificToCatalan.values())

@APP.route('/listen_menu', methods = ['POST', 'GET'])
def listen_menu():
    if request.method == 'GET':
        scientificToCatalan=catalanNames()
        print("hello", flush=True)
        return flask.render_template('listen_menu.html', game_modes=modes.keys(), species=scientificToCatalan.values())
    if request.method == 'POST':
        print
        form_data = request.form
        game_mode=form_data["game_mode"]
        print(game_mode, flush=True)
        return redirect(url_for("listen", game_mode=game_mode))

@APP.route('/listen_species_menu', methods = ['POST', 'GET'])
def listen_species_menu():
    if request.method == 'GET':
        scientificToCatalan=catalanNames()
        print("hello", flush=True)
        return flask.render_template('listen_species_menu.html', dict=scientificToCatalan, species=[sp for sp in scientificToCatalan.keys() if sp[0].isupper()])
    if request.method == 'POST':
        form_data = request.form
        species=form_data["species"]
        print(species, flush=True)
        return redirect(url_for("listen_species", species=species))

@APP.route('/listen/<game_mode>')
def listen(game_mode):
    targetList=modes[game_mode]
    recordings=loadRecordings()
    scientificToCatalan=catalanNames()
    species=rand.choice(targetList)
    if len(recordings[species])!=0:
        url="https:"+rand.choice(recordings[species])
    return flask.render_template('listen.html', url=url, species=scientificToCatalan[species], game_mode=game_mode)

@APP.route('/listen_species/<species>')
def listen_species(species):
    recordings=loadRecordings()
    scientificToCatalan=catalanNames()
    if len(recordings[species])!=0:
        url="https:"+rand.choice(recordings[species])
    return flask.render_template('listen_species.html', url=url, species=species)


@APP.route('/start_game', methods = ['POST', 'GET'])
def start_game():
    if request.method == 'GET':
        return f"The URL /data is accessed directly. Try going to '/form' to submit form"
    if request.method == 'POST':
        form_data = request.form
        max_num=form_data["num_questions"]
        session["game_mode"]=form_data["game_mode"]
        session["num"]=1
        session["correct"]=0
        session["max_num"]=form_data["num_questions"]

        return redirect(url_for("question"))


@APP.route('/')
def menu():
    return flask.render_template('menu.html')


@APP.route('/new_mode', methods = ['POST', 'GET'])
def new_mode():
    if request.method == 'GET':
        scientificToCatalan=catalanNames()
        return flask.render_template('new_mode.html', 
                                    names=scientificToCatalan)
    if request.method == 'POST':
        modeName = request.form["modeName"]
        multiselect = request.form.getlist('mymultiselect')
        modes[modeName]=multiselect
        return "Created new game mode (stored until the end of your session)"

if __name__ == '__main__':
    APP.debug=True
    APP.run()