import click
import string
from colorama import init
from random import choice
import tui_graphics

init()

with open("words_alpha.txt", "r") as file:
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


@tui.command()
def tui_settings():
    pass


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


@tui.command()
def play_tui():
    click.clear()
    click.echo(tui_graphics.banner)

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

        if len(guessed_correct_letters) == len(correct_letters):
            won = True
            break

        click.pause(info="Press any key to keep guessing...")

    if won:
        click.echo("Well Done! You won!")
    else:
        click.echo(f"You lose.\nThe correct word was {chosen_word}")


# GUI


@main.group()
def gui():
    """Graphical User Interface for HANGMAN"""
    pass


@gui.command()
def launch_gui():
    pass


if __name__ == "__main__":
    main()
