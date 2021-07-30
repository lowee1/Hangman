import shutil
import keyboard
import yaml
import importlib
import click

try:
    with open("config.yaml", "r") as file:
        config = yaml.safe_load(file)
except FileNotFoundError:
    with open("config.yaml", "w") as file:
        config = {'difficulty': 9, 'drawings': 'default_drawings.py',
                  'fullscreen': 'no', 'wordlist': 'words_alpha.txt'}
        yaml.dump(config, file)

banner = """
 █████   █████   █████████   ██████   █████   █████████  ██████   ██████   █████████   ██████   █████
░░███   ░░███   ███░░░░░███ ░░██████ ░░███   ███░░░░░███░░██████ ██████   ███░░░░░███ ░░██████ ░░███ 
 ░███    ░███  ░███    ░███  ░███░███ ░███  ███     ░░░  ░███░█████░███  ░███    ░███  ░███░███ ░███ 
 ░███████████  ░███████████  ░███░░███░███ ░███          ░███░░███ ░███  ░███████████  ░███░░███░███ 
 ░███░░░░░███  ░███░░░░░███  ░███ ░░██████ ░███    █████ ░███ ░░░  ░███  ░███░░░░░███  ░███ ░░██████ 
 ░███    ░███  ░███    ░███  ░███  ░░█████ ░░███  ░░███  ░███      ░███  ░███    ░███  ░███  ░░█████ 
 █████   █████ █████   █████ █████  ░░█████ ░░█████████  █████     █████ █████   █████ █████  ░░█████
░░░░░   ░░░░░ ░░░░░   ░░░░░ ░░░░░    ░░░░░   ░░░░░░░░░  ░░░░░     ░░░░░ ░░░░░   ░░░░░ ░░░░░    ░░░░░ 

"""

settings_banner = r"""
  █████████             ███       ███      ██                              
 ███░░░░░███          ░░███     ░░███     ░░                               
░███    ░░░   ██████  ███████   ███████   ████  ████████    ███████  █████ 
░░█████████  ███░░███░░░███░   ░░░███░   ░░███ ░░███░░███  ███░░███ ███░░  
 ░░░░░░░░███░███████   ░███      ░███     ░███  ░███ ░███ ░███ ░███░░█████ 
 ███    ░███░███░░░    ░███ ███  ░███ ███ ░███  ░███ ░███ ░███ ░███ ░░░░███
░░█████████ ░░██████   ░░█████   ░░█████  █████ ████ █████░░███████ ██████ 
 ░░░░░░░░░   ░░░░░░     ░░░░░     ░░░░░  ░░░░░ ░░░░ ░░░░░  ░░░░░███░░░░░░  
                                                           ███ ░███        
                                                          ░░██████         
                                                           ░░░░░░          
"""

settings_menu = rf"""
   #############################################################################  
  /                                                                             \ 
 /                                                                               \
#    ___ ___ _    ___ ___ _____     _   _  _     ___  ___ _____ ___ ___  _  _    #
#   / __| __| |  | __/ __|_   _|   /_\ | \| |   / _ \| _ \_   _|_ _/ _ \| \| |   #
#   \__ \ _|| |__| _| (__  | |    / _ \| .` |  | (_) |  _/ | |  | | (_) | .` |   #
#   |___/___|____|___\___| |_|   /_/ \_\_|\_|   \___/|_|   |_| |___\___/|_|\_|   #
#                                                                                #
#--------------------------------------------------------------------------------#
#                                                                                #
1. Select wordlist <{config["wordlist"]}>
2. Change difficulty (Not implemented yet)
3. Use custom drawings (Not implemented yet)
4. Play in fullscreen?(requires root) <{config["fullscreen"]}>
5. Save and exit
|\\                                                                            //|
####  ####  ####  ####  ####\                        /####  ####  ####  ####  ####
 \  ==    ==    ==    ==    ====--\\          //--====    ==    ==    ==    ==   /
  \                                 \________/                                  / 
   |                                                                           |
   #############################################################################  
"""


def get_hangman_drawing(lives: int) -> str:
    spec = importlib.util.spec_from_file_location(
        "drawings", config["drawings"])
    drawings = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(drawings)
    return drawings.drawings[lives - 1]


def centre_print(text: str):
    width = shutil.get_terminal_size().columns
    if width % 2 == 1:
        width -= 1
    lines = text.splitlines()
    for line in lines:
        click.echo(line.center(width))


def fullscreen():
    keyboard.send("f11")
