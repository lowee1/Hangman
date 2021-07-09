import click
from colorama import init
from random import choice
import tui_graphics

init()

with open("words_alpha.txt", "r") as file:
    words = file.readlines()
chosen_word = choice(words)


@click.group()
def main():
    pass


@main.group()
def tui():
    """Text-Based User Interface for HANGMAN."""
    pass


@tui.command()
def tui_settings():
    pass


@tui.command()
def play_tui():
    tui_graphics.clear()
    click.echo(tui_graphics.banner)

    lives = 8
    while lives > 0:
        current_hangman_drawing = tui_graphics.get_hangman_drawing(lives)
        click.echo(current_hangman_drawing)
        lives -= 1


@main.group()
def gui():
    """Graphical User Interface for HANGMAN"""
    pass


@gui.command()
def launch_gui():
    pass


if __name__ == "__main__":
    main()
