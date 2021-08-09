import importlib
import shutil
from string import Template
from sys import platform

import click
import keyboard
import yaml

try:
    with open("config.yaml", "r") as file:
        config = yaml.safe_load(file)
except FileNotFoundError:
    with open("config.yaml", "w") as file:
        config = {'difficulty': 9, 'drawings': 'default_drawings.py',
                  'fullscreen': 'no', 'wordlist': 'words_alpha.txt', "images": "default_hangman_images.py"}
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

settings_menu = Template(rf"""
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
1. Select wordlist
old: <{config["wordlist"]}>
new: $new_wordlist_path

2. Change difficulty (Not implemented yet)

3. Use custom drawings (Not implemented yet)

4. Play in fullscreen?{'(requires root)' if platform.startswith('linux') else ''}
old: <{config["fullscreen"]}>
new: $new_fullscreen

5. Save and exit ($unsaved_edits)
|\\                                                                            //|
####  ####  ####  ####  ####\                        /####  ####  ####  ####  ####
 \  ==    ==    ==    ==    ====--\\          //--====    ==    ==    ==    ==   /
  \                                 \________/                                  / 
   |                                                                           |
   #############################################################################  
""")


def get_hangman_drawing(lives: int) -> str:
    drawings_spec = importlib.util.spec_from_file_location(
        "drawings", config["drawings"])
    drawings = importlib.util.module_from_spec(drawings_spec)
    drawings_spec.loader.exec_module(drawings)
    return drawings.drawings[lives - 1]


def get_hangman_image(lives: int) -> str:
    images_spec = importlib.util.spec_from_file_location(
        "images", config["images"])
    images = importlib.util.module_from_spec(images_spec)
    images_spec.loader.exec_module(images)
    return images.get_image(lives)


def centre_print(text: str):
    width = shutil.get_terminal_size().columns
    if width % 2 == 1:
        width -= 1
    lines = text.splitlines()
    for line in lines:
        click.echo(line.center(width))


def fullscreen():
    keyboard.send("f11")
