"""Extract a specific variable value from the config.yml file in the current
directory and print it to the console so it can be used by GitHub Actions steps
by using the following syntax:

VALUE=$(python ./scripts/get_tutor_config_value.py VARIABLE_NAME)
"""

import os
import sys

import yaml


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
    with open(file_path, "r") as file:
        return yaml.safe_load(file)


def get_config_value(variable_name, config_file_path):
    """Extract a specific variable value from the YAML configuration.

    Args:
        variable_name (str): The name of the variable to get from the config.yml
        file.
        config_file_path (str): The path to the config.yml file.

    Returns:
        str: The value of the extracted variable.
    """
    check_config_file_exists(config_file_path)
    config = load_yaml_config(config_file_path)
    value = config.get(variable_name)

    if not value:
        print(
            f"ERROR: {variable_name} not found in the given config.yml",
            file=sys.stderr
        )
        sys.exit(1)

    return value


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(
            "ERROR: Please provide the variable name to extract from config.yml",
            file=sys.stderr,
        )
        sys.exit(1)

    variable_name = sys.argv[1]
    config_file_path = "./config.yml"
    value = get_config_value(variable_name, config_file_path)
    print(value)
