# Brownian Motion Robot Simulation

A Python module simulating a robot exhibiting Brownian-like motion in a square arena. The robot moves in straight lines and changes direction randomly upon colliding with boundaries.

https://www.youtube.com/watch?v=9QLnZeQwQe0

## Features

- Robot movement simulation in a square arena
- Boundary collision detection and random direction changes
- Matplotlib animation generation with GIF export
- Real-time simulation with Pygame
- Configuration file for parameter management

## Installation

```bash
# Basic installation
pip install .

# With Pygame support
pip install ".[pygame]"
```

## Usage

### As a Module

```python
import matplotlib.pyplot as plt
from brownian_robot import BrownianRobot, create_matplotlib_animation

# Create robot instance
robot = BrownianRobot(arena_size=100.0, robot_radius=2.0, speed=2.0)

# Run simulation
positions = robot.run_simulation(steps=1000, time_step=0.5)

# Visualize results
anim = create_matplotlib_animation(
    position_history=positions,
    arena_size=100.0,
    robot_radius=2.0
)
plt.show()
```

### Running the Sample Application

```bash
python examples/run_simulation.py
```

Edit `config.yaml` to change simulation parameters.

## Configuration

Simulation parameters can be set in the `config.yaml` file:

```yaml
# Visualization mode: 'matplotlib' or 'pygame'
mode: matplotlib

# Arena size
arena_size: 100.0

# Robot radius
robot_radius: 2.0

# Movement speed
speed: 2.0

# Simulation time step
time_step: 0.5

# Number of simulation steps (for matplotlib mode)
steps: 1000

# Maximum simulation duration in seconds (for pygame mode)
duration: 60.0

# Whether to save visualization output
save_output: false

# Path to save output files
output_path: output
```

## Generating Videos and GIFs

### Matplotlib Animation

Set `save_output: true` to automatically save Matplotlib animations as GIFs.

### Video Frames from Pygame

When using Pygame mode with `save_output: true`, sequential frames will be generated. Create a video from these frames using ffmpeg:

```bash
ffmpeg -framerate 30 -i output/frames/frame_%05d.png -c:v libx264 -pix_fmt yuv420p output.mp4
```

## Requirements

- Python 3.6+
- NumPy
- Matplotlib (for visualization)
- Pygame (optional, for real-time simulation)

## Mathematical Background

This simulation implements a simplified Brownian motion model, combining straight-line movement with random direction changes upon collision.

The position update equation is:

```
new_position = current_position + velocity * time_step
```

Direction changes upon collision follow:

```
new_direction = (current_direction + π + random(-π/2, π/2)) % 2π
```

Over long periods, this model shows characteristics of a constrained random walk in a bounded arena.

## Module Structure

```
brownian_robot/
├── brownian_robot/
│   ├── __init__.py       # Module interface
│   ├── core.py           # Core simulation functionality
│   ├── visualization.py  # Visualization capabilities
│   └── config.py         # Configuration management
├── examples/
│   └── run_simulation.py # Sample application
├── setup.py              # Installation configuration
└── README.md             # This file
```
