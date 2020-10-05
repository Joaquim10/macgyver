# MacGyver - Escape the labyrinth

## Presentation

This application is a 2D labyrinth game.

MacGyver is locked in a labyrinth and have to escape. A guard is watching over the exit. To succeed, MacGyver must collect some items scattered around the maze and craft a syringe to put the guard to sleep.


## Prerequisite

* A PC with any OS installed in it. This game is standalone. It can be runned on any computer.

* Python 3.7, which can be downloaded from https://www.python.org/downloads/


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

The tile set grid is stored in the maze.txt file in the config directory.
The tile set grid must be 15 tiles wide and 15 tiles height.

Tile set notation:
* '#' for walls.
* ' ' blank spaces for paths.
* '?' for the player's starting position.
* '!' for the exit of the labyrinth.

## Game launch and controls

* Run the game by typing:

            python3 escape.py

* Use the keyboard arrow keys to move.

* Walk on items to get them.

