import json
import os
from shlex import join
import subprocess
import sys
import argparse
from jax import config
import utils

def load_configuration_template(file_path):
    """Load json file"""
    try:
        with open(file_path,'r',encoding='utf-8') as file:
            config_data_loaded = json.load(file)
            return config_data_loaded
    except FileNotFoundError:
            raise FileNotFoundError(f"File {file_path} not found")
    except json.JSONDecodeError as e:
            raise ValueError(f"Error decoding json file {e}")

configuration = load_configuration_template("config.json")        

def create_project_structure(project_name):
    print("Create folder project:{projec_name}")
    os.makedirs(project_name,exist_ok=True)

    for folder in configuration["STRUCTURE"]:
        path = os.path.join(".",project_name,folder)
        os.makedirs(path, exist_ok=True)
        print(f"Folder create: {path}")
    print("Structure completed.\n")


def create_virtual_env(project_name,eniroment_name):
    print("Create virtual environment...")
    venv_path = os.path.join(".", project_name,eniroment_name)
    subprocess.run([sys.executable, "-m", "venv", venv_path])
    print(f"Environment completed: {venv_path}\n")

def create_base_files(project_name):
    print("Create base files")
    files = configuration["BASE_FILES"]

    for file in files:
        file_path = os.path.join(".",project_name,file)
        with open(file_path, "w") as f:
            f.write("")
        print(f"Create file: {file_path}")
    print("Base files completed.\n")


def main(): 
    """Create parser"""
    parser = argparse.ArgumentParser(description="This script creates a template project for working with neural networks")
    parser.add_argument("-pjn","--project_name",type=str,required=False,help="This is set the name folder project")
    parser.add_argument("-env","--environment",type=str,required=False,help="This is set the name environment python")

    args = parser.parse_args()

    project_name = args.project_name if utils.stringIsNotNulOfEmpty(args.project_name) else configuration["PROJECT_NAME_DEFAULT"] 
    environment_name = args.environment if utils.stringIsNotNulOfEmpty(args.environment) else configuration["ENVIRONMENT_NAME_DEFAULT"]

    create_project_structure(project_name)
    create_virtual_env(project_name,environment_name)
    create_base_files(project_name)


if __name__ == "__main__":
     main()
     