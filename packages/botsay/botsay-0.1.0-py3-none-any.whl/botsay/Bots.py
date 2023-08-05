from lolpython import lol_py
from colorama import Fore, Back, Style

ey = 'n'

def bot0(txt, color='', printM=print):
    txtbot = "           < " + txt + " >\n"
    txtlen = len(txtbot)
    top = "            " + "_" * (txtlen - 14) + "\n"
    bottom = "            " + "-" * (txtlen - 14)

    printM(color + top + txtbot + bottom + f'''
             /
            /
     |---|     
     |{ey} {ey}|     
     |_-_|     
    /|(\)|\    
   d |___| b   
     |_|_|     
     /_|_\ ''')


def bot1(txt, color='', printM=print):
    txtbot = "           < " + txt + " >\n"
    txtlen = len(txtbot)
    top = "            " + "_" * (txtlen - 14) + "\n"
    bottom = "            " + "-" * (txtlen - 14)

    printM(color + top + txtbot + bottom + f'''
             /
            /
      ___T_     
     | {ey} {ey} |    
     |__0__|    
     ,=|x|=.    
     'c/_\  'c  
      /7 [|     
    \/7  [|_ ''')
