from lolpython import lol_py
import sys
import random
import argparse
from colorama import Fore, Back, Style

import botsay.Bots
from botsay.Bots import *

def run():
    bots = [bot0, bot1]
    botsstr = ['bot0', 'bot1']


    def chooseBot(color='', printM=print, bot=None):
        if bot == None:
            random.choice(bots)(' '.join(args.text), color, printM)
        else:
            bots[bot](' '.join(args.text), color, printM)


    parser = argparse.ArgumentParser()
    parser.add_argument("text", help="text that will be displayed by the robot (if you want to display more the 1 word pls soround it in "")", type=str, nargs='+')
    parser.add_argument("-r", "--rainbow", help="makes the text rainbow", action='store_true')
    parser.add_argument("-c", "--color", help="makes the text a certain color", action='store', type=str, choices=["red", "green", "blue", "yellow", "magenta", "cyan"])
    parser.add_argument("-e", "--eyes", help="change the eyes of the robot to a char", action='store', default='n')
    parser.add_argument("-b", "--bot", help="set the bot", action='store', choices=botsstr, default=None)
    args = parser.parse_args()

    botsay.Bots.ey = args.eyes[0]

    try:
        bot = int(args.bot[3:])
    except:
        bot = None

    if args.color and args.rainbow:
        print("you must only use --color/-c or --rainbow/-r not both")
        sys.exit(2)

    colors = {"red": Fore.RED, "green": Fore.GREEN, "blue": Fore.BLUE, "yellow": Fore.YELLOW, "magenta": Fore.MAGENTA, "cyan": Fore.CYAN}


    if args.color:
        color = colors[args.color]
        chooseBot(color=color, bot=bot)

    elif not args.rainbow:
        chooseBot(bot=bot)

    else:
        chooseBot(printM=lol_py, bot=bot)