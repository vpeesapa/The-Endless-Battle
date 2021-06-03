# The Endless Battle

*"Everything that lives is designed to end. We are perpetually trapped in a never-ending spiral of life and death. Is this a curse? Or some kind of punishment? I often think about the god who blessed us with this cryptic puzzle... and wonder if we'll ever get the chance to kill him."* - **2B, NieR:Automata**

## Author
Varun Peesapati

## About the game
***The Endless Battle*** is a top-down bullet hell shooter developed using `PyGame`. Inspired by the hacking minigame found within **NieR:Automata**, ***The Endless Battle*** allows the player to control a ship that is continuously attacked by a variety of enemies, each with their own distinct shooting patterns, giving freedom to the player to move about and dodge the relentless spray of bullets while they return fire at the same time.

## Controls
***The Endless Battle*** supports keyboard/mouse as well as controllers.
* Keyboard/Mouse:
    - W,A,S,D/&#8592;,&#8593;,&#8594;,&#8595;: Moves the player within the bounds of the screen.
    - Mouse(left click): Fire bullets (**Hold to fire continuously**).
    - Mouse(movement): Aim.
    - X: Exit game.
* Controllers (**Currently tested with only PS4 controllers**):
    - Left analog stick/D-Pad: Moves the player within the bounds of the screen.
    - R1: Fire bullets (**Hold to fire continuously**)
    - Right analog stick: Aim.
    - X: Exit game

## Organization of project
``` bash
$ tree .
.
├── .git
├── .gitignore
├── colors.py
├── controllers.py
├── game.py
└── README.md
```

## Usage
Installing `PyGame`:
``` bash
$ pip3 install pygame
```

Running the game:
``` bash
$ python3 game.py
```

## What works at the moment
* Player can rotate based on the mouse's position.
* Player can move while pointing towards the mouse pointer.
* Player can aim in any direction and fire bullets based on where they are pointing towards.
* Player can be controlled using a controller (**Note**: Tested using only a **PS4 controller**).
* Bullets' collision with makeshift blocks can be detected, resulting in both being removed.
* Improvised health system for both player and enemy, which also includes damage values for their respective bullets.
* Newer enemies do not spawn immediately, but rather after a second.
* There is now a recovery time frame in which the player is invincible whenever they are damaged.
* Player now collides with the enemies.
* Multiple enemies will appear on screen at once.
* Enemies can bump into each other without one of them gobbling up the other.
* There is now a game over screen that lets the player to either restart or exit the game after dying once.
* There is now a start menu that allows the player to voluntarily enter the game.

## Alert: There are things that are yet to be implemented
* ~~Implement one type of enemy - one that's about the same size as the player but shoots and relentlessly follows the player (Still need to implement logic for when the player gets hit by an enemy bullet).~~
* ~~Implement a second type of enemy - one that's circular in shape and radially shoots its bullets, while also rotating on its axis.~~
* ~~Introducing a health system for the player that is indicated by shifting the colors (for eg. green &#8594; yellow &#8594; red).~~
* ~~Clean up code by separating logic for both types of enemies into two different classes that inherits from the base class `Enemy`.~~
* ~~Increase difficulty by introducing a different type of bullet which cannot be destroyed by the player's bullets and requires them to dodge carefully and indicated by a different color (**Only shot by the second type of enemies**).~~
* ~~Implement a third type of enemy that stays in its position (**but does not rotate**), and shoots more bullets radially.~~
* ~~Give some time for the player to recover before it can take more damage.~~
* ~~Display score and player's health at the top of the screen.~~
* ~~Consider logic when either the player collides with the enemy or two enemies collide with each other while following the player.~~
* Have a UI (eg. a start menu, pause menu, etc.).
* Change button mappings for XBox controllers.
* ~~Update README with details of the completed project.~~

## References
1. PyGame Installation: https://pypi.org/project/pygame/
2. PyGame Documentation: https://www.pygame.org/docs/