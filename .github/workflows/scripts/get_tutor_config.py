"""Script to get Tutor configuration from a specified configuration file.

To use this script, you need to:

1. Install the `pyyaml` package by running `pip install pyyaml`.
2. Run the script from the root of the repository or from where it can find the `config.yml` file.
3. Pass the required and optional keys as command-line arguments.
4. The script will print the environment variables based on the keys.
5. Set the environment variables in the GitHub Actions workflow.

You can run the script using the following command:

python ./scripts/get_tutor_config.py --config-file config.yml --required-keys TUTOR_VERSION TUTOR_APP_NAME --optional-keys DOCKER_REGISTRY

See the `parse_args` function for more details on the command-line arguments. Find a usage example in the `.github/workflows/build.yml` file.
"""

import os
import sys
import yaml
import argparse


def load_config(config_file: str) -> dict:
    """Loads the YAML configuration from the specified file.

    Args:
        config_file (str): The path to the configuration file.

    Returns:
        dict: The configuration data.
    """
    file_path = os.path.join(os.getcwd(), config_file)
    if not os.path.exists(file_path):
        sys.exit("ERROR: file config.yml doesn't exist")

    with open(file_path, "r", encoding="utf-8") as file:
        return yaml.safe_load(file)


def check_required_keys(config: dict, required_keys: list):
    """Checks if the required keys are present in the config.

    Args:
        config (dict): The configuration data.
        required_keys (list): The list of required keys.
    """
    for key in required_keys:
        if key not in config:
            sys.exit(f"ERROR: key {key} not found in config.yml")


def collect_env_vars(config: dict, required_keys: list, optional_keys: list) -> list:
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
    parser = argparse.ArgumentParser(
        description="Process required and optional keys for config."
    )

    parser.add_argument(
        "--config-file",
        default="config.yml",
        help="The path to the configuration",
    )
    parser.add_argument(
        "--required-keys",
        nargs="+",
        default=["TUTOR_VERSION", "TUTOR_APP_NAME"],
        help="List of required keys to look for in config.yml.",
    )
    parser.add_argument(
        "--optional-keys",
        nargs="+",
        default=["DOCKER_REGISTRY"],
        help="List of optional keys to look for in config.yml.",
    )

    return parser.parse_args()


def main(config_file="config.yml", required_keys=None, optional_keys=None):
    """Main function to load config, validate keys, and print environment variables.

    Args:
        config_file (str): The path to the configuration file.
        required_keys (list): The list of required keys.
        optional_keys (list): The list of optional keys.
    """
    tutor_config = load_config(config_file)

    check_required_keys(tutor_config, required_keys)

    env_vars = collect_env_vars(tutor_config, required_keys, optional_keys)

    print("\n".join(env_vars))


if __name__ == "__main__":
    main(**vars(parse_args()))
