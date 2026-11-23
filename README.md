# Pokémon Générations

A Pokémon collection and battle game for the desktop, written in Python with Tkinter.

The game covers the 890 Pokémon of generations 1 to 8. Build a deck of six, fight a random team, and win eggs that unlock new Pokémon in your Pokédex.

## Table of contents

- [Pokémon Générations](#pokémon-générations)
	- [Table of contents](#table-of-contents)
	- [How it works](#how-it-works)
	- [Tech stack](#tech-stack)
	- [Repository structure](#repository-structure)
	- [Prerequisites](#prerequisites)
	- [Installation](#installation)
	- [Running locally](#running-locally)
	- [License](#license)

## How it works

1. **Loading**: at startup the game loads the type icons, the Pokémon sprites, the rarity frames and the interface images, then reads the Pokémon list and the type chart from text files.
2. **Pokédex**: Pokémon are listed by generation (1 to 8) in a scrollable grid. Pokémon not yet unlocked appear as an empty frame.
3. **Deck**: the deck holds six unlocked Pokémon. Select a slot, then click a Pokémon in the Pokédex to put it there.
4. **Battle**: the opponent is a team of six random Pokémon. For each opposing Pokémon, the screen shows the types it is weak and strong against, and the player picks one of their Pokémon to duel it.
5. **Duel**: the result depends on the 18-type effectiveness chart (`fichiers/type.txt`) applied to the types of both Pokémon. The loser is removed from the battle, and a draw removes both. The battle ends when one side has no Pokémon left.
6. **Eggs**: a player who wins more duels than they lose receives an egg of a random rarity (normal, legendary, mythical or ultra beast). Opening it unlocks a random Pokémon of that rarity not yet owned.
7. **Saving**: unlocked Pokémon are stored in `fichiers/infos.txt` and the deck in `fichiers/deck.txt`. Both files are rewritten while playing.

## Tech stack

| Layer | Technologies |
| --- | --- |
| Language | Python 3 |
| Interface | Tkinter (canvas, 1280x720 window) |
| Images | PNG files, Pillow as a fallback for Tk versions without PNG support |
| Data | Plain text files (`;`-separated Pokémon list, type chart, deck) |

## Repository structure

```
.
├── main.py          Game: interface, battle logic, loading and saving
├── fichiers/
│   ├── infos.txt    Pokémon list and unlocked state (saved progress)
│   ├── deck.txt     Pokédex numbers of the six deck Pokémon
│   ├── type.txt     Type effectiveness chart (18x18)
│   └── infos_*.txt  Other copies of the Pokémon list with different unlocked states
├── images/          Interface images, frames, eggs, backgrounds
├── pokemons/        One sprite per Pokémon, named by Pokédex number (001.png to 890.png)
├── types/           Type icons
└── deck.txt         Older deck file, not read by the game
```

Each line of `fichiers/infos.txt` has seven `;`-separated fields: number, name, types, generation, rarity, evolution number and unlocked flag (`1` when owned). The game is a single script that uses global state and reacts to mouse clicks according to the current screen.

## Prerequisites

- [Python](https://www.python.org/) 3 with Tkinter
- Tk 8.6 or later, which reads PNG files natively. On macOS, the Tk 8.5 bundled with the system and with some pyenv builds shows an empty grey window; use a Python built against a recent Tk, for example from Homebrew:

```bash
brew install python-tk@3.13
```

- [Pillow](https://python-pillow.org/) (`pip install pillow`), only needed when Tk cannot read PNG files

## Installation

```bash
git clone git@github.com:maxencebonamy/Pokemon-Generations.git
cd Pokemon-Generations
```

## Running locally

Run the game from the repository root, because file paths are relative.

```bash
python3 main.py
```

With the Homebrew Python:

```bash
/opt/homebrew/bin/python3.13 main.py
```

On macOS, set `TK_SILENCE_DEPRECATION=1` to hide the Tk deprecation warning.

## License

This project is licensed under the [MIT License](LICENSE).
