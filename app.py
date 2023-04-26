#!/usr/bin/env python

import flask
from flask import request, redirect, url_for, send_from_directory

import random as rand
import os

from modes import modes
from utils import loadRecordings, catalanNames


# Create the application.
APP = flask.Flask(__name__)
question=0
max_num=0

@APP.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(APP.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')
@APP.route('/question/<num>/<max_num>/<game_mode>')
def question(num, max_num, game_mode):
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

@APP.route('/response/<num>/<max_num>/<game_mode>/<response>/<correct>')
def response(num, max_num, game_mode, response, correct):
    return flask.render_template('response.html', 
                                num=num, max_num = max_num, 
                                game_mode=game_mode, response=response,
                                correct=correct)


@APP.route('/form')
def form():
    scientificToCatalan=catalanNames()
    print(scientificToCatalan.values(), flush=True)
    return flask.render_template('form.html', game_modes=modes.keys(), species=scientificToCatalan.values())

@APP.route('/listen/<game_mode>')
def listen(game_mode):
    targetList=modes[game_mode]
    recordings=loadRecordings()
    scientificToCatalan=catalanNames()
    species=rand.choice(targetList)
    if len(recordings[species])!=0:
        url="https:"+rand.choice(recordings[species])
    return flask.render_template('listen.html', url=url, species=scientificToCatalan[species], game_mode=game_mode)


@APP.route('/start_game', methods = ['POST', 'GET'])
def start_game():
    if request.method == 'GET':
        return f"The URL /data is accessed directly. Try going to '/form' to submit form"
    if request.method == 'POST':
        form_data = request.form
        max_num=form_data["num_questions"]
        return redirect(url_for("question",num=1, max_num = max_num, game_mode=form_data["game_mode"]))


@APP.route('/')
def menu():
    return flask.render_template('menu.html')

if __name__ == '__main__':
    APP.debug=True
    APP.run()