"""
Core functionality for Brownian motion robot simulation.
"""

import numpy as np
import math
import random
from typing import List, Tuple

class BrownianRobot:
    """
    A robot exhibiting Brownian-like motion in a square arena.
    """
    
    def __init__(self, arena_size: float = 100.0, robot_radius: float = 1.0, speed: float = 1.0):
        """Initialize robot with given parameters."""
        self.arena_size = arena_size
        self.robot_radius = robot_radius
        self.speed = speed
        
        # Start at the center of the arena
        self.position = np.array([arena_size / 2, arena_size / 2])
        
        # Random initial direction (in radians)
        self.direction = 2 * math.pi * random.random()
        
        # History of positions for visualization
        self.position_history = [self.position.copy()]
    
    def update(self, time_step: float = 1.0) -> None:
        """Update robot position for one time step."""
        # Calculate velocity vector from direction and speed
        velocity = np.array([
            self.speed * math.cos(self.direction),
            self.speed * math.sin(self.direction)
        ])
        new_position = self.position + velocity * time_step
        
        # Check for boundary collisions
        collision = False
        
        # X-axis boundaries
        if new_position[0] - self.robot_radius < 0:
            new_position[0] = self.robot_radius
            collision = True
        elif new_position[0] + self.robot_radius > self.arena_size:
            new_position[0] = self.arena_size - self.robot_radius
            collision = True
            
        # Y-axis boundaries
        if new_position[1] - self.robot_radius < 0:
            new_position[1] = self.robot_radius
            collision = True
        elif new_position[1] + self.robot_radius > self.arena_size:
            new_position[1] = self.arena_size - self.robot_radius
            collision = True
            
        # Change direction randomly upon collision
        if collision:
            reflection_angle = random.uniform(-math.pi/2, math.pi/2)
            self.direction = (self.direction + math.pi + reflection_angle) % (2 * math.pi)
        
        # Update position and history
        self.position = new_position
        self.position_history.append(self.position.copy())
    
    def run_simulation(self, steps: int, time_step: float = 1.0) -> List[np.ndarray]:
        """Run simulation for specified number of steps."""
        self.position_history = [self.position.copy()]
        
        for _ in range(steps):
            self.update(time_step)
            
        return self.position_history


def run_simulation(
    arena_size: float = 100.0,
    robot_radius: float = 1.0,
    speed: float = 1.0,
    steps: int = 1000,
    time_step: float = 1.0
) -> List[np.ndarray]:
    """Run a Brownian motion simulation with specified parameters."""
    robot = BrownianRobot(arena_size, robot_radius, speed)
    return robot.run_simulation(steps, time_step)