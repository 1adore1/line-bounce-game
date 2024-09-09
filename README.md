# Line Bounce Game

### Overview

The Line Bounce project is a computer vision game built using Python, OpenCV, and MediaPipe.
The game involves bouncing a ball off a line drawn between two index fingers tracked via webcam.
The ball moves in real-time, and the player uses their fingers to control the line, trying to hit the ball to keep it bouncing.
The score increments every time the ball collides with the line.

### Installation
1. Clone the repository:
```
cd <your directory>
git clone https://github.com/1adore1/line-bounce-game.git
cd line-bounce-game
```
2. Install the required dependencies:
```
pip install requirements.txt
```

### How To Run
To start the game, execute the following command:
```
python main.py
```

### Gameplay Instructions

* When launched, ball will randomly fall from the top of the screen and will bounce off the walls.
* Your score increases each time a ball touches the line between your hands.
* The game ends when you press the 'q' key to quit.
---
