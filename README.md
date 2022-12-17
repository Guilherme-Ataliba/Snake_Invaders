# Snake_Invaders
 ## Game inspired by galaga and space invaders in pygame

This is my first "big" project, developed as a final grade for a python class on my university. 

It is based on the tutorial by ClearCode on Youtube (https://www.youtube.com/watch?v=o-6pADy5Mdg&t=71s).

Even though I tried to make it as organized as I could, now with a little more experience, there are several things that I would change completely. This must be a curse on this kind of project, you'll learn more as you do it, and it's never gonna end. 

This is the version that I presented in class. 

![image](https://user-images.githubusercontent.com/120763485/208255588-3742cc0c-6df6-4dab-b00c-7aaaa08a3139.png)
![image](https://user-images.githubusercontent.com/120763485/208255631-b6c54e2b-eb3a-464c-9345-b4b004bfe389.png)

## Implementations
I kept on adding more things to this project, and i'll try to remember all of them:
* **Console**: Press the key ['] to open a console terminal in-game. There are 3 commands: godmode, nextwave, nocooldown.
  This was intended to help during the presentation, since we didn't have much time (and it really helped).
* **Power-Ups**: You get these by killing blue space ships or the insects. The power-ups are chosen randomly every time you kill one of these enemies
* **Score**: The score sceen show all scores saved in a .txt arquive, thus it is saved throught sessions. 
* **Controls**: The controls are what you'd expect: directional arrows, space to shoot/select, Enter to enter text. 

## Installation
1. Install python
2. Install pygame
```
pip install pygame
```
When this project was developed, pygame hadn't updated to the latest python version yet, if this is your case, use this instead
```
pip install pygame --pre
```
3. Run the main.py file with your prefered method
