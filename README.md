# The Endless Battle

*"Everything that lives is designed to end. We are perpetually trapped in a never-ending spiral of life and death. Is this a curse? Or some kind of punishment? I often think about the god who blessed us with this cryptic puzzle... and wonder if we'll ever get the chance to kill him."* - **2B, NieR:Automata**

## Author
Varun Peesapati

## What works at the moment
* Player can rotate based on the mouse's position.
* Player can move while pointing towards the mouse pointer.
* Player can aim in any direction and fire bullets based on where they are pointing towards.
* Player can be controlled using a controller (**Note**: Tested using only a **PS4 controller**).
* Bullets' collision with makeshift blocks can be detected, resulting in both being removed.
* Improvised health system for both player and enemy, which also includes damage values for their respective bullets.
* Newer enemies do not spawn immediately, but rather after a second.

## Alert: There are things that are yet to be implemented
* ~~Implement one type of enemy - one that's about the same size as the player but shoots and relentlessly follows the player (Still need to implement logic for when the player gets hit by an enemy bullet).~~
* Clean up code by separating logic for both types of enemies into two different classes that inherits from the base class `Enemy`.
* Increase difficulty by introducing a different type of bullet which cannot be destroyed by the player's bullets and requires the player to dodge carefully and indicated by a different color (**Only shot by the second type of enemies**).
* Consider logic when either the player collides with the enemy or two enemies collide with each other while following the player (Possibly through the **A&ast; algorithm**).
* ~~Implement a second type of enemy - one that's circular in shape and radially shoots its bullets, while also rotating on its axis.~~
* ~~Introducing a health system for the player that is indicated by shifting the colors (for eg. green &#8594; yellow &#8594; red).~~
* Have a UI (eg. a start menu, pause menu, etc.).
* Change button mappings for XBox controllers.
* Update README with details of the completed project.