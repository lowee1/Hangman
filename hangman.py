import string
from random import choice

import click
import yaml
from colorama import init
import PySimpleGUI as sg

import tui_graphics

init()

try:
    with open("config.yaml", "r") as file:
        config = yaml.safe_load(file)
except FileNotFoundError:
    with open("config.yaml", "w") as file:
        config = {"difficulty": 9, "drawings": "default_drawings.py",
                  "fullscreen": "no", "wordlist": "words_alpha.txt", "images": "default_hangman_images.py"}
        yaml.dump(config, file)


with open(config["wordlist"], "r") as file:
    words = file.read().splitlines()
chosen_word = choice(words).upper()

# main group so that help shows both gui and tui


@click.group()
def main():
    pass


# TUI


@main.group()
def tui():
    """Text-Based User Interface for HANGMAN."""
    pass


def get_wordlist():
    while True:
        wordlist = click.prompt("Enter path to wordlist",
                                type=click.Path(exists=True, file_okay=True,
                                                dir_okay=False, readable=True,
                                                resolve_path=True))
        with open(wordlist, "r") as file:
            words = file.readlines()
        if len(words) < 2:
            click.echo("wordlist must contain at least two lines")
            continue

        if not any(map(lambda word: bool(word.strip()), words)):
            click.echo("wordlist must not contain empty lines")
            continue

        break

    return wordlist


def get_difficulty():
    raise NotImplementedError


def get_drawings():
    raise NotImplementedError


def get_fullscreen_status():
    return click.prompt("Would you like to play in fullscreen mode",
                        show_choices=True, type=click.Choice(["yes", "no"]))


@tui.command(name="config")
def tui_settings():
    unsaved_edits = "No modifications"
    tui_graphics.centre_print(tui_graphics.settings_banner)
    while True:
        current_settings_menu = tui_graphics.settings_menu.substitute(
            new_wordlist_path=config["wordlist"], new_fullscreen=config["fullscreen"], unsaved_edits=unsaved_edits)
        tui_graphics.centre_print(current_settings_menu)
        selected = click.prompt("Select option", show_choices=True,
                                type=click.Choice(["1", "2", "3", "4", "5"]))
        unsaved_edits = "You have unsaved edits"
        match selected:
            case "1":
                new_wordlist = get_wordlist()
                config["wordlist"] = new_wordlist
            case "2":
                new_difficulty = get_difficulty()
                config["difficulty"] = new_difficulty
            case "3":
                new_drawings = get_drawings()
                config["drawings"] = new_drawings
            case "4":
                new_fullscreen_status = get_fullscreen_status()
                config["fullscreen"] = new_fullscreen_status
            case "5":
                with open("config.yaml", "w") as file:
                    yaml.dump(config, file)
                break


def generate_word_display(guessed_corrects: list, correct: list) -> str:
    return " ".join(
        [letter if letter in guessed_corrects else "_" for letter in correct]
    )


def get_letter_guess(guessed_letters: list) -> str:
    valid_guess = False
    while not valid_guess:
        guess = click.prompt("Please guess a letter",
                             prompt_suffix=" -->> ").upper()
        match guess:
            case guess if len(guess) != 1:
                click.echo("Please enter one and only one letter")
            case guess if guess not in string.ascii_uppercase:
                click.echo("You did not enter a valid letter")
            case guess if guess in guessed_letters:
                click.echo("You have already guessed " + guess)
            case _:
                return guess


@tui.command(name="play")
def play_tui():
    if config["fullscreen"]:
        tui_graphics.fullscreen()
    click.clear()
    tui_graphics.centre_print(tui_graphics.banner)

    correct_letters = list(chosen_word)
    guessed_correct_letters = []
    guessed_incorrect_letters = []

    lives = 8
    won = False
    while lives > 0 and not won:
        current_hangman_drawing = tui_graphics.get_hangman_drawing(lives)
        click.echo(current_hangman_drawing)
        click.echo(generate_word_display(
            guessed_correct_letters, correct_letters))
        click.echo(guessed_incorrect_letters)

        current_letter_guess = get_letter_guess(
            guessed_correct_letters + guessed_incorrect_letters
        )
        if current_letter_guess in correct_letters:
            guessed_correct_letters.append(current_letter_guess)
            click.echo(
                f"{current_letter_guess} is one of the letters")
        else:
            guessed_incorrect_letters.append(current_letter_guess)
            click.echo(f"{current_letter_guess} is not in the word")
            lives -= 1

        if len(guessed_correct_letters) == len(set(correct_letters)):
            won = True
            break

        click.pause(info="Press any key to keep guessing...")

    if won:
        click.echo("Well Done! You won!")
    else:
        click.echo("You lose.")

    click.echo(f"The correct word was {chosen_word}")


# GUI


@main.group()
def gui():
    """Graphical User Interface for HANGMAN"""
    pass


@gui.command(name="launch")
def launch_gui():
    sg.theme("DarkBlack")

    def make_menu():
        menu_layout = [[sg.Text("Hangman", font=("Arial", 60, "bold"), pad=(5, 40))],
                       [sg.HorizontalSeparator()],
                       [sg.Column([[sg.Button("Play", font=("Arial", 30))],
                                   [sg.Button(
                                       "Settings", font=("Arial", 30))],
                                   [sg.Button("Exit", font=("Arial", 30))]],
                                  element_justification="center",
                                  vertical_alignment="center",
                                  )
                        ],
                       ]

        if config["fullscreen"] == "yes":
            menu_window = sg.Window("Hangman", menu_layout,
                                    element_justification="center", finalize=True,
                                    no_titlebar=True, resizable=False, keep_on_top=False)
            menu_window.Maximize()
        else:
            menu_window = sg.Window("Hangman", menu_layout,
                                    element_justification="center", finalize=True)
        return menu_window

    def make_play_window():
        game_layout = [[sg.Image(filename=), sg.Text()],
                       [sg.HorizontalSeparator()],
                       [sg.Column(
                           [
                               [sg.Text("Please guess a letter")],
                               [sg.InputText()],
                               [sg.Submit("Guess")]
                           ]),
                        sg.Button("Quit Game", font=("Arial", 10))
                        ]
                       ]
        if config["fullscreen"] == "yes":
            play_window = sg.Window("play", game_layout,
                                    element_justification="center", finalize=True,
                                    no_titlebar=True, resizable=False)
            play_window.Maximize()
        else:
            play_window = sg.Window("play", game_layout,
                                    element_justification="center", finalize=True)
        return play_window

    menu_window, play_window = make_menu(), None

    while True:
        window, event, values = sg.read_all_windows()
        if window == sg.WIN_CLOSED:
            break
        if event == sg.WIN_CLOSED or event == "Exit":
            window.close()
            if window == menu_window:
                menu_window = None
        elif event == "Play":
            if not play_window:
                play_window = make_play_window()
                menu_window.close()
                menu_window = None
            while True:
                window, event, values = sg.read_all_windows()

                if event == sg.WIN_CLOSED or event == "Quit Game":
                    window.close()
                    play_window = None
                    menu_window = make_menu()
                    break


if __name__ == "__main__":
    main()
