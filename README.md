# MacGyver - Escape the labyrinth

## Presentation

This application is a 2D labyrinth game.

MacGyver is locked in a labyrinth and have to escape. A guard is watching over the exit. To succeed, MacGyver must collect some items scattered around the maze and craft a syringe to put the guard to sleep.


## Prerequisite

* A PC with any OS installed in it. This game is standalone. It can be runned on any computer.

* Python 3, which can be downloaded from https://www.python.org/downloads/


## Installation

* Open your terminal and type the following commands:

On Windows, open `PowerShell` and type the commands.

1. Clone the repository:

        git clone https://github.com/Joaquim10/macgyver

An alternative is to `download zip` from https://github.com/Joaquim10/macgyver by clicking on `Code` and then unzip the file.

2. Move to the root of the application:

        cd macgyver

3. Install virtualenv:

        pip install virtualenv

4. Create a virtual environment:

        virtualenv -p python3 env

* On Windows, type the following command:

        virtualenv -p $env: python3 env

5. Activate the virtual environment:

        source env/bin/activate

* On Windows, type the following command:

        ./env/scripts/activate.ps1
    
6. Install the requirements:

        pip install -r requirements.txt

* This will install Pygame.

## Setup

### The tile set grid

The maze structure loaded in the game is stored in a text file in the `mazes` directory. By default, this file is `maze.txt`.
It's a grid of 15 characters width and 15 characters height.

Structures notation in the text file:

* `#` for walls. The wall tiles blocks MacGyver.
* ` ` blank spaces for paths. MacGyver can move on the paths tiles.
* `?` for the player's starting position.
* `!` for the exit of the labyrinth and the location of the guard.

### settings
The settings are stored in the `settings.py` file in the `config` directory.

## Game launch

* Run the game by typing:

            python3 main.py

## controls

* Use the keyboard arrow keys to move.

* Walk on items to get them.

## 


