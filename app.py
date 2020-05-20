#!/usr/bin/env python3
import socket
import termios
import tty
import os
import sys
import configparser
from glob import glob
from termcolor import cprint
from random import choice
from subprocess import call
from os import stat, listdir, chdir, getcwd, get_terminal_size
from sys import getsizeof, stdin



# Config
config = configparser.ConfigParser()
config.read('config.ini')
download_location = config["General"]["download_location"]


class ClientCLI:
    def __init__(self):
        self.ui = UI()

    # File
    def File(self):
        list_of_files = glob('*.txt')
        latest_file = max(list_of_files, key=os.path.getctime)
        file = latest_file.replace('\\', '')
        return file

    def flush(self):
        try:
            os.remove(client.File())
            cprint("> Successfully flushed the cache file!", "green")
        except FileNotFoundError as FlushErorr:
            cprint(f"[WARNING] Couldn't Flush. Error:{FlushErorr}")


    def DownloadThemAll(self):
        if config["General"]["custom_location"] == "Enabled":
            call(f'spotdl --list={client.File()} -f "{download_location}" --overwrite skip', shell=True)
        else:
            call(f'spotdl --list={client.File()} --overwrite skip', shell=True)
            client.flush()

    # notes
    def note(self):
        cprint("Type 'c' to change category and '0' to exit program", "blue")


    def track(self):
        os.system('clear')
        client.note()


        while True:
            spot_link = input("Enter Song Link/URL [SPOTIFY]: ")

            if spot_link == "c":
                os.system('clear')
                #sys.exit()
                main_run()
            elif spot_link == "0":
                os.system('clear')
                cprint("See you next time!","yellow")
                sys.exit()
            elif spot_link == "":
                cprint("Enter a valid option and Try again...", "red")
            else:
                if config["General"]["custom_location"] == "Enabled":
                    call(f'spotdl --song {spot_link} -f "{download_location}"', shell=True)
                else:
                    call(f'spotdl --song {spot_link}', shell=True)



    def album(self):
        os.system('clear')
        client.note()



        spot_album = input("Enter Album Link [SPOTIFY]: ")
        if spot_album == "0":
            os.system('clear')
            cprint("See you next time!","yellow")
            sys.exit()
        elif spot_album == "c":
            os.system('clear')
            #sys.exit()
            main_run()

        call(f"spotdl --album {spot_album}", shell=True)
        client.DownloadThemAll()


    def your_playlist(self):
        os.system('clear')
        client.note()


        while True:
            spot_playlist = input("Enter Playlist Link [SPOTIFY]: ")
            if spot_playlist == "0":
                os.system('clear')
                cprint("See you next time!","yellow")
                sys.exit()
            elif spot_playlist == "c":
                os.system('clear')
                #sys.exit()
                main_run()

            call(f"spotdl --playlist {spot_playlist}", shell=True)
            client.DownloadThemAll()

    def artist(self):
        os.system('clear')
        client.note()

        while True:
            spot_artist = input("Enter Artist Link [SPOTIFY]: ")
            if spot_artist == "0":
                os.system('clear')
                cprint("See you next time!","yellow")
                sys.exit()
            elif spot_artist == "c":
                os.system('clear')
                #sys.exit()
                main_run()

            call(f"spotdl --all-albums {spot_artist}", shell=True)
            client.DownloadThemAll()



    def exits(self):
        os.system('clear')
        cprint("See you next time!","yellow")
        sys.exit()

    def close(self):
        os.system('clear')
        cprint("See you next time!","yellow")
        sys.exit()

class UI:
    def __init__(self):
        self.Buffer = []
        self.point = 0
        self.ask = 'select item: '
        self.search_buffer = ''
        self.search = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
                       'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
                       'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
                       'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
                       '1', '2', '3', '4', '5', '6', '7', '8', '9', '0',
                       '.', ',', ' ', '+', '_', '-'
                       ]
        self.theme = {'selection_color': self.Color.green,
                      'unselected_color': self.Color.white,
                      'selection_cursor': ' >> ',
                      'ask_color': self.Color.cyan,
                      'ask_item_color': self.Color.red,
                      'search_color': self.Color.yellow
                      }

    class Color:
        black = '\u001b[30m'
        red = '\u001b[31m'
        green = '\u001b[32m'
        yellow = '\u001b[33m'
        blue = '\u001b[34m'
        magenta = '\u001b[35m'
        cyan = '\u001b[36m'
        white = '\u001b[37m'
        reset = '\u001b[0m'

    def start(self):
        self.reload()
        while True:
            char = self.read()
            if char == '\x03':  # ctrl + c
                client.close()
            elif char == '\x0d':  # enter
                self.clear()
                return self.Buffer[self.point]
            elif char in self.search:  # append to buffer
                if len(self.search_buffer) > 15:
                    pass
                else:
                    self.search_buffer += char
                self.clear()
                count = 0
                for item in self.Buffer:
                    if self.search_buffer == item[0:len(self.search_buffer)]:
                        self.point = count
                        break
                    count += 1
                self.reload()
            elif char == '\x7f':  # backspace
                self.search_buffer = self.search_buffer[0:-1]
                self.clear()
                self.reload()
            elif char == '\x1b':
                self.read()
                char = self.read()
                if char == 'A':  # up
                    if self.point > 0:
                        self.point -= 1
                    self.clear()
                    self.reload()
                elif char == 'B':  # down
                    if self.point < len(self.Buffer) - 1:
                        self.point += 1
                    self.clear()
                    self.reload()

    def reload(self):
        print(self.theme['ask_color'] +
              self.ask + self.Color.reset +
              self.theme['ask_item_color'] + '  ' +
              self.Buffer[self.point] +
              self.Color.reset + '    ' +
              self.theme['search_color'] +
              self.search_buffer +
              self.Color.reset + ' ' * 16)
        for item in self.Buffer:
            if item == self.Buffer[self.point]:
                print(self.theme['selection_color'] + self.theme['selection_cursor'] + item + self.Color.reset)
            else:
                print(self.theme['unselected_color'] + self.theme['selection_cursor'] + item + self.Color.reset)

    @staticmethod
    def read():
        fd = stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(stdin.fileno())
            ch = stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

    def clear(self):
        print('\033[F' * (len(self.Buffer) + 1), end='')
        for item in range(0, len(self.Buffer) + 1):
            print(' ' * get_terminal_size().columns)
        print('\033[F' * (len(self.Buffer) + 1), end='')

    def reset(self):
        self.Buffer = []
        self.point = 0
        self.ask = 'select item: '
        self.search_buffer = ''

client = ClientCLI()

def main_run():

    print('\x1bc')
    try:
        client.ui.reset()
        client.ui.ask = '\rDownload list :'
        client.ui.Buffer = ['track', 'album' , 'your playlist' , 'artist' , 'exit' ]
        st = client.ui.start()
        if st == 'track':
            client.track()
        elif st == 'album':
            client.album()
        elif st == 'your playlist':
            client.your_playlist()
        elif st == 'artist':
            client.artist()
        elif st == 'exit':
            client.exits()
    except (KeyboardInterrupt, TypeError):
        exit()

main_run()