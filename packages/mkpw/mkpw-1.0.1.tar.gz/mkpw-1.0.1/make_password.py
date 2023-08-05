#!/usr/bin/env python
"""
Memorable Password Generator

Generates a password that should be able to be easily remembered
"""
from typing import Optional
import random
from memorable import _word_bank
import typer
import rich


NON_NAMES = list(set(
    _word_bank.NOUNS
    + _word_bank.VERBS
    + _word_bank.ADJECTIVES
    + _word_bank.ADVERBS
))
app = typer.Typer(add_completion=False)


def gen_memorable_password(num_words: int = 5,
                           kind: Optional[str] = None
                           ) -> str:
    """
    Generates a memorable password using a word list

    Args:
        num_words (int): The number of words to use.  Defaults to 5

    Returns:
        str: The generated password

    Example:
        >>> password = gen_memorable_password(6)
    """

    spaces = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0',
              '-', '_', '.', '!', '$', '#', '<', '>', '+', '?', '&',
              ]
    words = [random.choice(NON_NAMES) for _ in range(num_words)]
    upper_idx = random.choice(range(len(words)))
    words[upper_idx] = words[upper_idx].upper()

    password = ''
    used_spaces = [' ']
    for word in words:
        space = ' '
        while space in used_spaces:
            space = random.choice(spaces)
        password += f'{word}{space}'
    return password[:-1]


@app.command()
def cli(num_words: int = typer.Argument(5)):
    """
    Memorable Password Generator

    Generates a password that should be able to be easily remembered
    """
    passwd = gen_memorable_password(num_words)
    rich.print(f'Generated Pasword: [bold green]{passwd}[/bold green]')


if __name__ == '__main__':
    app()
