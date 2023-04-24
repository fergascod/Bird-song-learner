from utils import *
import os
from modes import modes
#from custom import custom

def welcome():
    print("Benvingut! \
    \nAquest joc et permetrà posar a prova els teus coneixements d'identificació d'aus pel seu cant.\n")

    print("Els diferents modes de joc són:")
    for i in list(modes.keys()):
        print("-",i)
    print("- custom")
    print("\nPer parar de jugar seleccioni el mode de joc: stop")
    print("Si ets valent i vols jugar amb totes les espècies disponibles usa el mode de joc: tots")

if __name__=="__main__":
    rows, columns = os.popen('stty size', 'r').read().split()
    welcome()
    birdrecordings=loadRecordings()
    scientificToCatalan=catalanNames()


    print("*"*int(columns))
    mode=input("Seleccioni mode de joc: ")

    while mode!="stop":
        try:
            if mode.lower() in list(modes.keys())+["tots", "custom"]:

                if mode.lower()=="tots":
                    targetList=list(birdrecordings.keys())
                #elif mode.lower()=="custom":
                #    targetList=custom(list(birdrecordings.keys()), scientificToCatalan)
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
        except KeyboardInterrupt:
            print("\nA reveure!")
            sys.exit()
