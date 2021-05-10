from utils import *
import os
from modes import modes

def welcome():
    print("Benvingut! \
    \nAquest joc et permetrà posar a prova els teus coneixements d'identificació d'aus pel seu cant.\n")

    print("Els diferents modes de joc són:")
    for i in list(modes.keys()):
        print("-",i)
    print("Per parar de jugar seleccioni el mode de joc: stop")
    print("Si ets valent i vols jugar amb totes les espècies disponibles usa el mode de joc: tots")

if __name__=="__main__":
    rows, columns = os.popen('stty size', 'r').read().split()
    welcome()
    birdrecordings=loadRecordings()
    scientificToCatalan=catalanNames()

    print("*"*int(columns))
    mode=input("Seleccioni mode de joc: ")

    while mode!="stop":
        if mode.lower() in list(modes.keys()) or mode.lower()=="tots":
            if mode.lower()=="tots":
                targetList=list(birdrecordings.keys())
            else:
                targetList=modes[mode]
            rows, columns = os.popen('stty size', 'r').read().split()
            numQ=int(input("Quantes preguntes vols respondre? "))
            print("")

            result=test(numQ, targetList, birdrecordings)
            print("*"*int(columns))
        else:
            print("El mode seleccionat no existeix.")
        mode=input("Seleccioni mode de joc: ")
