# Welcome to DoodsAi
---

#### What?
DoodsAi is a micro life simulation. Not so much a game, but for me, just as fun to watch. The little fish things are known as 'Doods' as that was what I was calling them when I first started on this project in Godot 3 some years ago. 
The Doods are little digital creatures that are spawned into their virtual environment and left to fend for themselves. 

They are given very few things to start with. Generation 1 is given a small neural network with a set amount of starting connections randomly assigned from input node to output node. They interpret the data within their environment and then decided what to do based on this decision process. As the creator I have no means of knowing what exactly they will do and for me that is the fun of it.

Doods are also assigned base 'physical' attributes: Size, Speed, and Sight. These are there to help them navigate their environment, and as viewers to see how different species start emerging and behaving.

Keep in mind that even with similar species, no two Doods will necessarily think the same. Their neural net brain comes equipped with weighted perceptions of data as well as bias on the outcome of that interpretation.

#### Why?
I started this project because I was inspired by this dev's project https://www.youtube.com/@TheBibitesDigitalLife. I wanted to get into game dev but didnt have an idea, I also like simulation and the study of micro biology and behaviors. So with no idea how to go about it I started researching and writing my own neural network from scratch in GDScript for godot.

I am now learning Python and thought that porting the now broken Godot project over using Pygame would give me that fuel to really dive into some more difficult things while I learn. Considering I needed to worry about handling a lot of my own stuff, So far I have been correct, but that is also what makes it fun.

### COMMUNITY
I write a lot of this code @ twitch.tv/CodeNameTribbs, and welcome people who want to get involved with it. My project is not so special as to hoard to myself. Enjoy playing with it or pushing pull requests to help make the project better!


Special Thanks To:
- __BrianlessSociety__ for being a regular viewer and pointing out my pythonic shortcomings!
- __AkaruiYami__ for being a regular viewer and contributing to the project, fixing collision and giving the Doods the gift of SIGHT

#### Project Notes & TODOS
- [X] sperate movement from fps
- [ ] controlable environement class
- [ ] generation tracking
- [ ] gene tracking
- [ ] system for watching genes
- [ ] observable avoidance behavior
- [ ] observable food detection behavior

Dood Specific:
- [ ] neural network brain for doods
- [ ] Handle collision detection between doods & doods
- [x] Handle collision detection between doods & food
- [X] Collision detection for food
- [ ] Collision detection for other doods
- [ ] Breeding capabilities based on variables and collision
- [ ] Fitness score
- [ ] Scaling attributes, size, speed, perception
- [ ] Color modulation based on attributes
- [X] Collison Mask
- [ ] Get their brain working and processing environment within 'sight'
 
Food specific:
- [X] Class needs to be coded
- [X] Needs stages with energy variants based on growth stage
- [X] Growth based over delta time
- [X] Collision mask

Environment Specifics:
- [ ] Manage Start Variables, number of doods, number of food, max food, max doods, food spawn rate
- [ ] Spawn Food - currently on initial environment creation, need interval spawning
- [X] Contain Doods
- [ ] Wider Range environment outside of window
- [ ] Camera
- [ ] Contain entities in future builds, ie rocks and stuff.
