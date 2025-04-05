"""
Brownian Motion Robot Simulation

A Python module that simulates a robot exhibiting Brownian-like motion in a square arena.
The robot moves in straight lines and changes direction randomly upon colliding with boundaries.
"""

from .core import BrownianRobot, run_simulation
from .visualization import create_matplotlib_animation, run_pygame_simulation
from .config import load_config

__version__ = "0.1.0"
__all__ = [
    "BrownianRobot",
    "run_simulation",
    "create_matplotlib_animation", 
    "run_pygame_simulation",
    "load_config"
]