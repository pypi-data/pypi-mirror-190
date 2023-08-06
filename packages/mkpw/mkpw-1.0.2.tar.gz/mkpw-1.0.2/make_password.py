#!/usr/bin/env python
"""
Memorable Password Generator

Generates a password that should be able to be easily remembered
"""
from typing import Optional
import random
import time
from memorable import _word_bank
import pyperclip
import typer
import rich


__VERSION__ = '1.0.2'
__AUTHOR__ = 'Steve McGrath <steve@mcgrath.sh>'


NON_NAMES = list(set(
    _word_bank.NOUNS
    + _word_bank.VERBS
    + _word_bank.ADJECTIVES
    + _word_bank.ADVERBS
))
app = typer.Typer(add_completion=False)


def gen_memorable_password(num_words: int = 5,
                           kind: Optional[str] = None,
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


def clear_clipboard():
    pyperclip.copy('')
    rich.print('[dim]Clipboard cleared.[/dim]')


@app.command()
def cli(num_words: int = typer.Argument(5),
        clip: bool = typer.Option(False, '--clip', '-c',
                                  help='Send the password to the clipboard'),
        timer: Optional[int] = typer.Option(
            None, '--timer', '-t',
            help='How many seconds to keep the password in in the clipboard?'
        )
        ):
    """
    Memorable Password Generator

    Generates a password that should be able to be easily remembered
    """
    passwd = gen_memorable_password(num_words)
    rich.print(f'Generated Pasword: [bold green]{passwd}[/bold green]')
    if clip:
        rich.print('[dim]Copied to clipboard![/dim]')
        pyperclip.copy(passwd)
        if timer:
            rich.print((f'[dim]Waiting {timer} seconds '
                        'for clipboard expiration...[/dim]'
                        ))
            try:
                start = int(time.time())
                while int(start + timer) > int(time.time()):
                    time.sleep(1)
            except KeyboardInterrupt:
                clear_clipboard()
            else:
                clear_clipboard()


if __name__ == '__main__':
    app()
