from colorama import Fore
from os import system, name

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
   _____      _   _   _
  / ____|    | | | | (_)
 | (___   ___| |_| |_ _ _ __   __ _ ___
  \___ \ / _ \ __| __| | '_ \ / _` / __|
  ____) |  __/ |_| |_| | | | | (_| \__ \
 |_____/ \___|\__|\__|_|_| |_|\__, |___/
                               __/ |
                              |___/
"""


def get_hangman_drawing(lives: int) -> str:
    m = Fore.MAGENTA
    g = Fore.GREEN
    rst = Fore.RESET
    drawings = [
        rf"""
      {m}╔════╦
      ║    ║
      ║    {g}0
      {m}║   {g}\|/
      {m}║    {g}|
      {m}║   {g}/ \
      {m}║
    ══╩══════════{rst}
    """,
        rf"""
      {m}╔════╦
      ║    ║
      ║    {g}0
      {m}║   {g}\|/
      {m}║    {g}|
      {m}║   {g}  \
      {m}║
    ══╩══════════{rst}
    """,
        rf"""
      {m}╔════╦
      ║    ║
      ║    {g}0
      {m}║   {g}\|/
      {m}║    {g}|
      {m}║   {g}
      {m}║
    ══╩══════════{rst}
    """,
        rf"""
      {m}╔════╦
      ║    ║
      ║    {g}0
      {m}║   {g}\|/
      {m}║    {g}
      {m}║   {g}
      {m}║
    ══╩══════════{rst}
    """,
        rf"""
      {m}╔════╦
      ║    ║
      ║    {g}0
      {m}║   {g} |/
      {m}║    {g}
      {m}║   {g}
      {m}║
    ══╩══════════{rst}
    """,
        rf"""
      {m}╔════╦
      ║    ║
      ║    {g}0
      {m}║   {g} |
      {m}║    {g}
      {m}║   {g}
      {m}║
    ══╩══════════{rst}
    """,
        rf"""
      {m}╔════╦
      ║    ║
      ║    {g}0
      {m}║   {g}
      {m}║    {g}
      {m}║   {g}
      {m}║
    ══╩══════════{rst}
    """,
        rf"""
      {m}╔════╦
      ║    ║
      ║    {g}
      {m}║   {g}
      {m}║    {g}
      {m}║   {g}
      {m}║
    ══╩══════════{rst}
    """,
    ]

    return drawings[lives - 1]
