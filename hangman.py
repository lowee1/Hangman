import click
from random import choice

with open("popular.txt", "r") as file:
    words = file.readlines()
chosen_word = choice(words)

click.echo(chosen_word)
