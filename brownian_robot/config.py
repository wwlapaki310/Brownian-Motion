"""
Configuration management for Brownian motion robot simulation.
"""

import os
from typing import Dict, Any

def parse_config_file(file_path: str) -> Dict[str, Any]:
    """Parse a simple configuration file."""
    config = {}
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            
        for line in lines:
            # Skip comments and empty lines
            line = line.strip()
            if not line or line.startswith('#'):
                continue
                
            # Split key and value
            if ':' in line:
                key, value = [part.strip() for part in line.split(':', 1)]
                
                # Convert value to appropriate type
                if value.lower() == 'true':
                    value = True
                elif value.lower() == 'false':
                    value = False
                elif value.replace('.', '', 1).isdigit():  # Allow one decimal point
                    if '.' in value:
                        value = float(value)
                    else:
                        value = int(value)
                
                config[key] = value
    
    except Exception as e:
        print(f"Error loading config file: {e}")
        return {}
    
    return config


def load_config(config_path: str = "config.yaml") -> Dict[str, Any]:
    """Load configuration from file or create default config."""
    # Default configuration
    default_config = {
        "mode": "matplotlib",
        "arena_size": 100.0,
        "robot_radius": 2.0,
        "speed": 2.0,
        "time_step": 0.5,
        "steps": 1000,
        "duration": 60.0,
        "save_output": False,
        "output_path": "output"
    }
    
    # Load configuration from file
    if os.path.exists(config_path):
        user_config = parse_config_file(config_path)
        
        # Update default with user settings
        default_config.update(user_config)
        
        print(f"Loaded config from '{config_path}'")
    else:
        print(f"Warning: Config file '{config_path}' not found. Using default settings.")
        
        # Create default config file
        try:
            os.makedirs(os.path.dirname(config_path) or '.', exist_ok=True)
            with open(config_path, 'w', encoding='utf-8') as f:
                f.write("""# Brownian Motion Robot Simulation Configuration

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
""")
            print(f"Created default config file '{config_path}'")
        except Exception as e:
            print(f"Error creating default config file: {e}")
            
    return default_config