from utils import *
import os

def setMode(mode):
    # I should make a mode.py where I store all the lists and load it here
    return None

if __name__=="__main__":
    rows, columns = os.popen('stty size', 'r').read().split()
    #modeList=modeList()
    print("Benvingut! \
    \nAquest joc et permetrà posar a prova els teus coneixements d'identificació d'aus pel seu cant.\n")
    print("Per parar de jugar seleccioni el mode de joc: stop")
    birdrecordings=loadRecordings()
    print("*"*int(columns))
    mode=input("Seleccioni mode de joc: ")

    while mode!="stop":
        #targetList=setMode(mode)
        targetList=birdrecordings.keys()
        rows, columns = os.popen('stty size', 'r').read().split()
        numQ=int(input("Quantes preguntes vols respondre? "))
        print("")

        result=test(numQ, targetList, birdrecordings)
        print("*"*int(columns))
        mode=input("Seleccioni mode de joc: ")
