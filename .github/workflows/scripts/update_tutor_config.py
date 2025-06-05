import os
import sys
import yaml
import argparse
import random
import string
from datetime import datetime


def load_yaml(yaml_file: str) -> dict:
    """Loads the YAML configuration from the specified file.

    Args:
        file_path (str): The path to the configuration file.

    Returns:
        dict: The configuration data.
    """
    file_path = os.path.join(os.getcwd(), yaml_file)
    if not os.path.exists(file_path):
        sys.exit("ERROR: file config.yml doesn't exist")

    with open(file_path, "r", encoding="utf-8") as file:
        return yaml.safe_load(file)


def save_config(config_file: str, config: dict):
    """Saves the modified configuration back to the file."""
    file_path = os.path.join(os.getcwd(), config_file)
    with open(file_path, "w", encoding="utf-8") as file:
        yaml.dump(config, file, default_flow_style=False)


def generate_custom_tag(openedx_release: str, client: str, service: str, length: int = 4) -> str:
    """Generates a tag like <release>-<YYYYMMDD>-<HHMM>-<random>."""
    now = datetime.now()
    date_part = now.strftime("%Y%m%d")
    time_part = now.strftime("%H%M")
    random_part = ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))
    return f"209479273378.dkr.ecr.us-east-1.amazonaws.com/{client}-{service}:{openedx_release}-{date_part}-{time_part}-{random_part}"


def parse_args():
    parser = argparse.ArgumentParser(
        description="Create a random tag for the image that needs to be built."
    )   

    parser.add_argument(
        "--config-file",
        default="config.yml",
        help="The path to the configuration",
    )
    parser.add_argument(
        "--service",
        default="openedx",
        help="Service for which the image is built.",
    )
    parser.add_argument(
        "--client",
        default="edunext",
        help="Client for which the image is built.",
    )

    return parser.parse_args()


def main(config_file="config.yml", service=None, client="edunext"):
    tag_map_path = "picasso/.github/workflows/scripts/service_tag_map.yml"
    tutor_config = load_yaml(config_file)
    tag_map = load_yaml(tag_map_path)

    if service not in tag_map:
        sys.exit(f"ERROR: Service '{service}' not found in service_tag_map.yml")

    tag_key = tag_map[service]

    tutor_config[tag_key] = generate_custom_tag(openedx_release=tutor_config["TUTOR_APP_NAME"], client=client, service=service)
    save_config(config_file, tutor_config)


if __name__ == "__main__":
    main(**vars(parse_args()))
