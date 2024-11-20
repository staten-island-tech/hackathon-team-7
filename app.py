import os
import sys
import subprocess

def create_virtualenv(env_name="venv"):
    # Get the current working directory
    current_directory = os.getcwd()
    
    # Path for the virtual environment
    env_path = os.path.join(current_directory, env_name)
    
    # Check if the virtual environment already exists
    if not os.path.exists(env_path):
        # Create the virtual environment using subprocess
        subprocess.check_call([sys.executable, "-m", "venv", env_name])
        print(f"Virtual environment '{env_name}' created successfully at {env_path}.")
    else:
        print(f"Virtual environment '{env_name}' already exists at {env_path}.")

if __name__ == "__main__":
    create_virtualenv("venv")