import urllib3.request
import json
import pandas as pd
import pickle
import random as rand
from colorama import Fore, Style
import vlc
import sys

def make_url(bird_sp):
    '''Given the scientific name of a bird species this function
       returns the url to retrieve the xeno-canto recordings '''

    query="https://www.xeno-canto.org/api/2/recordings?query="
    genus, name = bird_sp.split(" ")
    completeQuery=query+genus+"+"+name+"+q:A"
    return completeQuery

def get_recordings(url):
    '''Makes a request to retrieve a list of all the recordings
       for the parameters specified in url'''

    with urllib.request.urlopen(url) as response:
        data = json.loads(response.read().decode())
        dataRecordings=data["recordings"]
        if len(dataRecordings)<=100:
            return [recording["file"] for recording in dataRecordings]
        dataRecordingsSampled=dataRecordings[:100]
        return [recording["file"] for recording in dataRecordingsSampled]

def catalanNames():
    '''Returns a bidirectional dictionary catalan-scientific'''
    catalanBirds=pd.read_csv("Data/table.csv", sep=",")
    scientificToCatalan={}
    for row in catalanBirds.iterrows():
        scientificToCatalan[row[1]["Genus"].lower()+" "+row[1]["Species (Scientific)"].lower()]=row[1]["Nom català"]
        scientificToCatalan[row[1]["Nom català"]]=row[1]["Genus"].lower()+" "+row[1]["Species (Scientific)"].lower()
    return scientificToCatalan

def toCatalan(x):
    '''Given a bird's scientific name it returns the catalan name of the bird
       or "noName" if we don't have the catalan name for tha species'''
    scientificToCatalan=catalanNames()
    if x not in scientificToCatalan.keys():
        return "noName"
    else:
        return scientificToCatalan[x]

def birdData():
    '''Returns a df with the data for all birds in AvesEspaña.csv'''
    allbirds=pd.read_csv("Data/AvesEspaña.csv", header=None, sep=";")

    # Get column names
    column_names=["sp_latin", "ssp", "sp_ingles", "sp_espanol", "PB", "NA", "CA", "rareza"]
    allbirds.columns=column_names

    # Take family name and put it as new column
    family=[]
    lastfamily=None
    for row in allbirds.iterrows():
        if not isinstance(row[1][3], str):
            lastfamily=row[1][0].lower()
        else:
            family.append(lastfamily)

    # Remove family rows and set them as new column
    allbirds=allbirds[allbirds["sp_ingles"].apply(lambda x : isinstance(x, str))]
    allbirds["family"]=family

    # lowercase all scientific names
    allbirds["sp_latin"]=allbirds["sp_latin"].apply(lambda x : x.lower())

    # Set catalan name as new column
    allbirds["sp_cat"]=allbirds["sp_latin"].apply(toCatalan)

    # Filter all birds for which we don't know the catalan name
    catBirds=allbirds[allbirds["sp_cat"]!="noName"]
    return catBirds

def loadRecordings():
    '''returns the recordings for all birds in AvesEspaña'''
    with open('Data/birdRecBySpCatDict.pickle', 'rb') as handle:
        birdRecBySpCat = pickle.load(handle)
    return birdRecBySpCat


def test(numQuestions, targetList=None, recordings=None, numOptions=4):
    '''This function makes the number of questions specified in
       parameter numQuestions'''
    if numQuestions <=0:
        return
    total=0
    for i in range(numQuestions):
        #First we get the correct bird and all possibilites
        if numOptions < len(targetList):
            possibilities=rand.sample(targetList, numOptions)
        else:
            possibilities=targetList
        spLatin=rand.choice(possibilities)

        #If we have recordings for that species we make a question
        if len(recordings[spLatin])!=0:
            url="https:"+rand.choice(recordings[spLatin])
            total+=question(url, bird=spLatin, possible=possibilities)
            print("")
        else:
            continue
    print("Resultat: ",total,"/",numQuestions, sep="")
    return total/numQuestions

def question(url, bird=None, possible=None):
    p = vlc.MediaPlayer(url)
    scientificToCatalan=catalanNames()
    if possible is not None:
        print("Les teves opcions són:")
        for species in possible:
            print(" -",scientificToCatalan[species])
    p.play()

    res=scientificToCatalan[bird].lower()
    ans=input("Introdueix el nom de l'espècie: ")
    if ans.lower() == res:
        print(f"    {Fore.GREEN}Correcte!{Style.RESET_ALL}", scientificToCatalan[bird])
        p.set_pause(1)
        return 1
    else:
        print(f"    {Fore.RED}Incorrecte :({Style.RESET_ALL}")
        print( "    L'au correcta és:",  scientificToCatalan[bird])
        p.set_pause(1)
        return 0
