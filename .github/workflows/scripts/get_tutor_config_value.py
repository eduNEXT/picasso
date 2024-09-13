"""Extract a specific value given a key from the config.yml file in the current
directory and print it to the console so it can be used by GitHub Actions steps
by using the following syntax:

VALUE=$(python ./scripts/get_tutor_config_value.py KEY)
"""

import os
import sys

import yaml

CONFIG_FILE_PATH = "./config.yml"


def check_config_file_exists(file_path):
    """Check if the config.yml file exists.

    Args:
        file_path (str): The path to the config.yml file.

    Raises:
        SystemExit: If the config.yml file doesn't exist.
    """
    if not os.path.exists(file_path):
        print("ERROR: file config.yml doesn't exist")
        sys.exit(1)


def load_yaml_config(file_path):
    """Load the YAML configuration file.

    Args:
        file_path (str): The path to the config.yml file.

    Returns:
        dict: The content of the config.yml file.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        return yaml.safe_load(file)


def get_config_value(key, config_file_path):
    """Extract a specific key value from the YAML configuration.

    Args:
        key (str): The name of the key to get from the
        config.yml file.
        config_file_path (str): The path to the config.yml file.

    Returns:
        str: The value of the key.
    """
    check_config_file_exists(config_file_path)
    config = load_yaml_config(config_file_path)
    value = config.get(key)

    if not value:
        print(f"ERROR: {key} not found in the given config.yml", file=sys.stderr)
        sys.exit(1)

    return value


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(
            "ERROR: Please provide the key to extract from config.yml",
            file=sys.stderr,
        )
        sys.exit(1)

    config_key = sys.argv[1]
    config_value = get_config_value(config_key, CONFIG_FILE_PATH)
    print(config_value)
