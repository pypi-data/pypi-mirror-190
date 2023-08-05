from setuptools import setup, find_packages

long_description = """
=====================================
A simple memorable password generator
=====================================

The goal here was a simple password generator that will smash words together to
create a memorable password with a special character in between each word.  One
of the words will be uppercased.  The only options really available is the
number of words to be used.

The tool was written using the memorable library to enable offline wordlists.

.. code-block::

    ❯ mkpw --help

     Usage: mkpw [OPTIONS] [NUM_WORDS]

     Memorable Password Generator
     Generates a password that should be able to be easily remembered

    ╭─ Arguments ────────────────────────────────╮
    │   num_words      [NUM_WORDS]  [default: 5]                            │
    ╰───────────────────────────────────────╯
    ╭─ Options ─────────────────────────────────╮
    │ --help          Show this message and exit.                           │
    ╰───────────────────────────────────────╯

    ❯ mkpw
    Generated Pasword: golden-perch+intentionally-IRRELEVANTLY0lumpy7pants
    ❯ mkpw 3
    Generated Pasword: coaxingly_STUPENDOUS?worker
"""


setup(
    name='mkpw',
    version='1.0.0',
    description='Memorable Password Generator',
    long_description=long_description,
    author='Steve McGrath',
    author_email='steve@mcgrath.sh',
    url='https://github.com/stevemcgrath/mkpw',
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Topic :: System :: Systems Administration',
        'Topic :: Utilities',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
    ],
    keywords='password passwords',
    packages=find_packages(exclude=['docs', 'tests']),
    install_requires=[
        'typer>=0.3.2',
        'rich>=10.2.2',
        'requests>=2.27.1',
        'memorable>=1.0.3',
    ],
    entry_points={
        'console_scripts': [
            'mkpw=make_password:app',
        ],
    },
)
