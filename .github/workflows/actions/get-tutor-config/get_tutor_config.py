"""Script to get Tutor configuration from a specified configuration file.

To use this script, you need to:

1. Install the `pyyaml` package by running `pip install pyyaml`.
2. Run the script within the same directory as the configuration file.
"""
import os
import sys
import yaml
import argparse


def load_config(file_path):
    """Loads the YAML configuration from the specified file.

    Args:
        file_path (str): The path to the configuration file.

    Returns:
        dict: The configuration data.
    """
    if not os.path.exists(file_path):
        print("ERROR: file config.yml doesn't exist")
        sys.exit(1)

    with open(file_path, "r", encoding="utf-8") as file:
        return yaml.safe_load(file)


def check_required_keys(config, required_keys):
    """Checks if the required keys are present in the config.

    Args:
        config (dict): The configuration data.
        required_keys (list): The list of required keys.
    """
    for key in required_keys:
        if key not in config:
            print(f"ERROR: key {key} not found in config.yml")
            sys.exit(1)


def collect_env_vars(config, required_keys, optional_keys):
    """Collects the environment variables from the config.

    Args:
        config (dict): The configuration data.
        required_keys (list): The list of required keys.
        optional_keys (list): The list of optional keys.
    """
    env_vars = []

    for key in required_keys:
        env_vars.append(f"{key}={config[key]}")

    for key in optional_keys:
        if key in config:
            env_vars.append(f"{key}={config[key]}")

    return env_vars

def parse_args():
    """Parse command-line arguments for required and optional keys."""
    parser = argparse.ArgumentParser(description="Process required and optional keys for config.")

    parser.add_argument(
        '--required-keys', nargs='+', default=["TUTOR_VERSION", "TUTOR_APP_NAME"], 
        help="List of required keys to look for in config.yml."
    )
    parser.add_argument(
        '--optional-keys', nargs='+', default=["DOCKER_REGISTRY"],
        help="List of optional keys to look for in config.yml."
    )

    return parser.parse_args()

def main(config_file="config.yml", required_keys=None, optional_keys=None):
    """Main function to load config, validate keys, and print environment variables.

    Args:
        config_file (str): The path to the configuration file.
        required_keys (list): The list of required keys.
        optional_keys (list): The list of optional keys.
    """
    file_path = os.path.join(os.getcwd(), config_file)
    tutor_config = load_config(file_path)

    check_required_keys(tutor_config, required_keys)

    env_vars = collect_env_vars(tutor_config, required_keys, optional_keys)

    print("\n".join(env_vars))

if __name__ == "__main__":
    main(**vars(parse_args()))
