#!/usr/bin/env python

import flask
from flask import request, redirect, url_for

import random as rand

from modes import modes
from utils import loadRecordings, catalanNames



# Create the application.
APP = flask.Flask(__name__)
question=0
max_num=0

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
    return flask.render_template('form.html', game_modes=modes.keys())

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