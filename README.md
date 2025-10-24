# Iron-Dome-Game
A simulation game with missile attacker, spy satellite and missile interceptor in python and pygame  

This is a Python-based simulation game that models the interception of 
incoming missiles using a virtual Iron Dome system. The game is designed 
to demonstrate basic principles of 
1. trajectory prediction, 
2. interception timing and 
3. visual feedback.

## Features

- Incoming rockets with random numbers and randomized trajectories
- Interceptor missiles launched to intercept rockets
- Visual feedback using Pygame
- Real-time simulation with adjustable parameters
- Scoring system based on successful interceptions

## Requirements

- Python 3.8+
- Pygame

Install dependencies with:

    pip install pygame

## How to Run

Launch the game with:

    python irondome.py

## Game Logic

- Rockets spawn at random intervals and descend toward the ground
- Interceptors launch from a fixed position and attempt to collide with rockets
- Collision detection is based on proximity
- Score increases with each successful interception

## Customization

You can adjust parameters in the code to change:

- Rocket speed and spawn rate
- Interceptor speed
- Collision radius
- Visual styles

## License

MIT License
