#!/usr/bin/env python3
"""
Sample application for the Brownian motion robot simulation.
"""

import sys
import os

# Add project root to Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

import matplotlib.pyplot as plt

# Import from brownian_robot module
from brownian_robot import BrownianRobot, run_simulation
from brownian_robot import create_matplotlib_animation, run_pygame_simulation
from brownian_robot import load_config


def main():
    """Run the sample application."""
    # Load configuration
    config = load_config("config.yaml")
    
    print(f"Running Brownian motion simulation:")
    print(f"  Mode: {config['mode']}")
    print(f"  Arena size: {config['arena_size']}")
    print(f"  Robot radius: {config['robot_radius']}")
    print(f"  Speed: {config['speed']}")
    print(f"  Time step: {config['time_step']}")
    
    # Create output directory if needed
    if config['save_output']:
        os.makedirs(config['output_path'], exist_ok=True)
    
    # Run simulation based on selected mode
    if config['mode'] == 'matplotlib':
        print(f"Running matplotlib simulation for {config['steps']} steps...")
        
        # Run simulation
        position_history = run_simulation(
            arena_size=config['arena_size'],
            robot_radius=config['robot_radius'],
            speed=config['speed'],
            steps=config['steps'],
            time_step=config['time_step']
        )
        
        # Create animation
        output_path = os.path.join(config['output_path'], 'brownian_simulation.gif') if config['save_output'] else None
        anim = create_matplotlib_animation(
            position_history=position_history,
            arena_size=config['arena_size'],
            robot_radius=config['robot_radius'],
            save_path=output_path
        )
        
        # Show animation
        plt.tight_layout()
        plt.show()
        
    elif config['mode'] == 'pygame':
        print(f"Running pygame simulation for up to {config['duration']} seconds...")
        
        output_dir = os.path.join(config['output_path'], 'frames') if config['save_output'] else None
        run_pygame_simulation(
            arena_size=config['arena_size'],
            robot_radius=config['robot_radius'],
            speed=config['speed'],
            time_step=config['time_step'],
            max_duration=config['duration'],
            save_frames=config['save_output'],
            save_dir=output_dir
        )


def example_direct_usage():
    """
    Alternative usage example - directly using the BrownianRobot class.
    """
    # Create a robot instance
    robot = BrownianRobot(arena_size=100.0, robot_radius=2.0, speed=3.0)
    
    # Run a 500-step simulation
    positions = robot.run_simulation(steps=500, time_step=0.1)
    
    # Visualize results
    anim = create_matplotlib_animation(
        position_history=positions,
        arena_size=100.0,
        robot_radius=2.0
    )
    
    plt.show()


if __name__ == "__main__":
    main()
    # Uncomment to try the alternative example:
    # example_direct_usage()