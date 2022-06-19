# What this project is about
Solves 2d mazes given to it as a picture. This bot was initially written as part of a math lecture (our professor told us to solve a maze in two minutes and this was the solution I came up with).  
Currently the bot runs with a few limitations 
 * the contrast of the photo needs to be fairly good (best is black on white in okay lighting) as all pixels below a certain brightness threshold are considered to be 'wall'
 * the entrance and exit of the labyrinth need to be on the left and right side of the center of the maze, respectively
 * the path as it is drawn doesn't scale with the resolution of the photo, but it should be decent enough for all reasonable sizes.

If you want to test the bot, there might be an instance running on my raspberry pi (so please don't spam it with requests or I have to shut it down). You can reach it on telegram: [@maze_solver_bot](https://telegram.me/maze_solver_bot)

# Running it locally
Most of the important code is contained in ``solver.py``. To run it, you need to have the python libraries ``Pillow``, ``numpy`` and ``matplotlib`` installed.  
If you want to run an instance on telegram, you also need the ``telegram-bot-ext`` packages (at least v20) and a bot auth token, which you can request from the [@botfather](https://telegram.me/botfather) and have to put in a file called ``token`` in same directory as ``bot.py``.

# How it works
``bot.py`` simply uses the python telegram interface and all it does is downloading sent images and forwarding them to the solver itself. Note that for laziness reasons files are saved locally and won't be cleaned up automatically.  

The solver itself is a bit more interesting: first we discard all pictures with low enough brightness as walls (this might be replaced by a more sophisticated approach in the future, but for now it works surprisingly well). We then find a bounding box around the maze itself to possibly reduce the size of the image.  

Because compupter vision is tough and I wanted to keep things as simple as possible, we do not search for the entrance and exit of the maze. Instead we draw a vertical line from the top and the bottom side of the picture to the labyrinth walls and then simply look for a path from the top left to the bottom right pixel.

# Results
Here are some examples of what the bot can do:
Input | Output
------|-------
![Picture of a maze](img/input_1.jpg?raw=true "A maze") | ![Picture of a maze with solution](img/output_1.jpg?raw=true "The maze with solution")
![Picture of a maze](img/input_2.jpg?raw=true "Another maze") | ![Picture of a maze with solution](img/output_2.jpg?raw=true "The other maze with solution")
