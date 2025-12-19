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
- **NEW: 3D model generation from photos and videos** 🎨

## 3D Model Generation

This repository now includes tools to convert photos and videos into 3D models using Python!

### Quick Start

Convert an image to a 3D model:

    python photo_to_3d.py assets/battlefield.png

Convert a video frame to 3D:

    python photo_to_3d.py video/iron_dome.mp4

For detailed documentation, see [3D_CONVERSION_GUIDE.md](3D_CONVERSION_GUIDE.md)

### Supported Features
- Single image to 3D model conversion
- Video frame extraction and 3D conversion
- Multiple export formats (OBJ, PLY, STL)
- Python API for programmatic use
- Extensible architecture for advanced techniques

## Requirements

- Python 3.8+
- Pygame
- Additional libraries for 3D conversion (optional)

Install dependencies with:

    pip install -r requirements.txt

Or for just the game:

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
