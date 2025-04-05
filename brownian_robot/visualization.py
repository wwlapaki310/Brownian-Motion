"""
Visualization functionality for Brownian motion robot simulation.
"""

import os
import time
import numpy as np
from typing import List, Optional

# Matplotlib imports
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.patches as patches

# Pygame imports (if available)
try:
    import pygame
    PYGAME_AVAILABLE = True
except ImportError:
    PYGAME_AVAILABLE = False

# Local imports
from .core import BrownianRobot

def create_matplotlib_animation(
    position_history: List[np.ndarray],
    arena_size: float,
    robot_radius: float,
    interval: int = 50,
    trail_length: int = 100,
    save_path: Optional[str] = None
) -> animation.FuncAnimation:
    """Create a matplotlib animation of the robot's movement."""
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_xlim(0, arena_size)
    ax.set_ylim(0, arena_size)
    ax.set_aspect('equal')
    ax.set_title("Brownian Motion Robot Simulation")
    
    # Draw arena boundary
    arena = patches.Rectangle((0, 0), arena_size, arena_size, 
                             fill=False, edgecolor='black', linewidth=2)
    ax.add_patch(arena)
    
    # Initialize robot visualization
    robot = plt.Circle(position_history[0], robot_radius, color='blue', fill=True)
    ax.add_patch(robot)
    
    # Initialize trail line
    trail, = ax.plot([], [], 'r-', alpha=0.6, linewidth=1)
    
    # Animation update function
    def update(frame):
        robot.center = position_history[frame]
        
        # Update trail
        start_idx = max(0, frame - trail_length)
        trail_x = [p[0] for p in position_history[start_idx:frame+1]]
        trail_y = [p[1] for p in position_history[start_idx:frame+1]]
        trail.set_data(trail_x, trail_y)
        
        return robot, trail
    
    # Create animation
    anim = animation.FuncAnimation(
        fig, update, frames=len(position_history),
        interval=interval, blit=True
    )
    
    # Save animation if path provided
    if save_path:
        writer = animation.PillowWriter(fps=30) if save_path.endswith('.gif') else animation.FFMpegWriter(fps=30)
        anim.save(save_path, writer=writer)
        print(f"Animation saved to {save_path}")
    
    return anim


def run_pygame_simulation(
    arena_size: float = 100.0,
    robot_radius: float = 1.0,
    speed: float = 1.0,
    time_step: float = 0.1,
    window_size: int = 800,
    max_duration: float = 60.0,
    save_frames: bool = False,
    save_dir: str = "frames"
) -> None:
    """Run a real-time Brownian motion simulation using Pygame."""
    if not PYGAME_AVAILABLE:
        print("Pygame is not available. Please install pygame to use this feature.")
        return
    
    # Initialize Pygame
    pygame.init()
    window = pygame.display.set_mode((window_size, window_size))
    pygame.display.set_caption("Brownian Motion Robot Simulation")
    clock = pygame.time.Clock()
    
    # Scale factor for converting between simulation and screen coordinates
    scale = window_size / arena_size
    
    # Create robot
    robot = BrownianRobot(arena_size, robot_radius, speed)
    
    # Trail points
    trail_points = [robot.position.copy()]
    max_trail_points = 500
    
    # For saving frames
    if save_frames:
        os.makedirs(save_dir, exist_ok=True)
        frame_count = 0
    
    # Simulation loop
    running = True
    start_time = time.time()
    
    while running and (time.time() - start_time < max_duration):
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        
        # Update simulation
        robot.update(time_step)
        
        # Update trail
        trail_points.append(robot.position.copy())
        if len(trail_points) > max_trail_points:
            trail_points.pop(0)
        
        # Clear screen
        window.fill((255, 255, 255))
        
        # Draw arena boundary
        pygame.draw.rect(window, (0, 0, 0), (0, 0, window_size, window_size), 2)
        
        # Draw trail
        if len(trail_points) > 1:
            scaled_points = [(int(p[0] * scale), int(p[1] * scale)) for p in trail_points]
            pygame.draw.lines(window, (255, 0, 0), False, scaled_points, 2)
        
        # Draw robot
        robot_pos = (int(robot.position[0] * scale), int(robot.position[1] * scale))
        pygame.draw.circle(window, (0, 0, 255), robot_pos, int(robot.robot_radius * scale))
        
        # Update display
        pygame.display.flip()
        
        # Save frame if requested
        if save_frames:
            pygame.image.save(window, f"{save_dir}/frame_{frame_count:05d}.png")
            frame_count += 1
        
        # Cap framerate
        clock.tick(60)
    
    pygame.quit()
    
    # Suggest ffmpeg command if frames were saved
    if save_frames and frame_count > 0:
        print(f"Saved {frame_count} frames to {save_dir}/")
        print("To create a video, you can use ffmpeg:")
        print(f"ffmpeg -framerate 30 -i {save_dir}/frame_%05d.png -c:v libx264 -pix_fmt yuv420p output.mp4")