"""
Script for generating dynamic Docker image tags and updating configuration.

This script is designed to support the Picasso build system for Open edX by generating
dynamic Docker image tags based on a configurable pattern. Tags are built using elements
like Tutor version, a user-defined prefix, timestamps, and optionally a random alphanumeric
suffix.

The script offers two modes of operation:
1. Generate and print a dynamic image tag to be used in GitHub Actions (for setting environment variables).
2. Update the specified Docker image tag directly in a given `config.yml` file.

Functionality:
- Dynamically create a Docker image tag based on input parameters.
- Optionally append a random alphanumeric suffix to the tag.
- Optionally overwrite the tag in `config.yml` if `--save-config` is enabled.
- Print `TARGET_KEY` and `DYNAMIC_IMAGE_TAG` as environment variables for GitHub Actions.

Usage (in command line or GitHub Actions):
    python update_image_tag.py \
        --config-file strains/example/config.yml \
        --service openedx \
        --image-tag-prefix olive \
        --timestamp-format "%Y%m%d-%H%M" \
        --add-random-suffix-to-image-tag true

Arguments:
- --config-file: Path to the `config.yml` file to read/update.
- --service: Service key mapped to a Docker image name (e.g., openedx, mfe).
- --image-tag-prefix: Prefix for the image tag, typically the Open edX release name.
- --timestamp-format: Format of the timestamp to use in the tag.
- --add-random-suffix-to-image-tag: Whether to append a random string to the tag.
- --save-config: If true, the image name will be saved back into `config.yml`.
- --image-tag: The full image tag to save in config (only used with --save-config).

Requirements:
- Python 3.6+
- PyYAML installed (`pip install pyyaml`)

Dependencies:
- get_tutor_config.load_config: Used to load YAML config files.
- service_tag_map.yml: Mapping of service names to config keys.

Example Output:
    TARGET_KEY=open_edx_docker_image
    DYNAMIC_IMAGE_TAG=docker.repo.com/openedx:v19.0.3-olive20250606-1012-a1b2
"""
import os
import sys
import yaml
import argparse
import random
import string
from datetime import datetime
from get_tutor_config import load_config

def str_to_bool(value):
    """
    Convert a string to a boolean.

    Accepts 'true' (case-insensitive) as True; anything else as False.
    """
    return value.lower() == 'true'


def write_config_file(config_file: str, config: dict):
    """Saves the modified configuration back to the file."""
    file_path = os.path.join(os.getcwd(), config_file)
    with open(file_path, "w", encoding="utf-8") as file:
        yaml.dump(config, file, default_flow_style=False)


def generate_image_tag(current_image_name: str,  tutor_version: str, service: str, 
                      image_tag_prefix: str, timestamp_format: str, add_random_suffix_to_image_tag: bool, 
                      length: int = 4) -> str:
    """
    Generate a new image tag based on the base name, timestamp, and optional random suffix.

    Args:
        current_image_name (str): The original image name with tag.
        service (str): The name of the service (not used directly here but passed through).
        image_tag_prefix (str): Prefix for the generated tag (usually the Open edX release name).
        timestamp_format (str): Format string for the timestamp (used by strftime).
        use_random_suffix (bool): Whether to append a random string to the tag.
        length (int): Length of the random string (if used).

    Returns:
        str: The updated image name with the new tag.
    """
    now = datetime.now()
    timestamp = now.strftime(timestamp_format)
    random_part = "".join(random.choices(string.ascii_lowercase + string.digits, k=length))
    current_image_name_without_tag = current_image_name.split(":")[0]
    updated_image_tag = f"{current_image_name_without_tag}:{tutor_version}-{image_tag_prefix}{timestamp}"

    if add_random_suffix_to_image_tag:
        suffix = f"-{random_part}"
        updated_image_tag = f"{updated_image_tag}{suffix}"

    return updated_image_tag


def parse_args():
    """
    Parse command-line arguments passed to the script.

    Returns:
        argparse.Namespace: Parsed arguments including config path, service name,
                            tag prefix, timestamp format, and suffix flag.
    """
    parser = argparse.ArgumentParser(
        description="Create a dynamic tag for the image that needs to be built."
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
        "--image-tag-prefix",
        default="openedx",
        help="Prefix to prepend to the image tag. Typically the Open edX release name (e.g., 'olive').",
    )
    parser.add_argument(
        "--timestamp-format",
        default="%Y%m%d-%H%M",
        help="Timestamp format to include in the image tag. Uses Python's strftime syntax.",
    )
    parser.add_argument(
        "--add-random-suffix-to-image-tag",
        default=False,
        type=str_to_bool,
        help="Whether to append a random alphanumeric suffix to the image tag (e.g., -a1b2).",
    )
    parser.add_argument(
        "--save-config",
        default=False,
        type=str_to_bool,
        help="If set to true, the dynamic image tag will be saved back to the config.yml file.",
    )
    parser.add_argument(
        "--image-tag",
        default=None,
        help="Image name to override the one defined in config.yml before building the new image.",
    )

    return parser.parse_args()


def main(config_file: str = "config.yml", service: str = None, image_tag_prefix: str = "", 
         timestamp_format: str = "%Y%m%d-%H%M", add_random_suffix_to_image_tag: bool = False, 
         save_config: bool = False, image_tag: str = None) -> None:
    """
    Load configuration, generate a dynamic image tag, and print or update config.

    Args:
        config_file (str): Path to the Tutor config file.
        service (str): Name of the service to be tagged.
        image_tag_prefix (str): Prefix to use in the image tag.
        timestamp_format (str): Format for the timestamp.
        use_random_suffix (bool): Whether to append a random suffix to the tag.
        save_config (bool): If True, the image name will be saved directly to config.yml.
        image_tag (str): The image name to save (used only if save_config is True).
    """
    target_key_map_path = f"{os.path.dirname(os.path.abspath(__file__))}/service_tag_map.yml"
    tutor_config = load_config(config_file)
    target_key_map = load_config(target_key_map_path)

    if service not in target_key_map:
        sys.exit(f"ERROR: Service '{service}' not found in service_tag_map.yml")

    target_key = target_key_map[service]

    if target_key not in tutor_config:
        sys.exit(f"ERROR: key {target_key} not found in config.yml")

    if save_config:
        if not image_tag:
            sys.exit("ERROR: --image-name must be provided when --save-config is true")

        tutor_config[target_key] = image_tag
        write_config_file(config_file, tutor_config)
    else:
        dynamic_image_tag = generate_image_tag(
            current_image_name=tutor_config[target_key],
            tutor_version=tutor_config["TUTOR_VERSION"],
            service=service,
            image_tag_prefix=image_tag_prefix,
            timestamp_format=timestamp_format,
            add_random_suffix_to_image_tag=add_random_suffix_to_image_tag,
        )

        env_vars = []
        env_vars.append(f"TARGET_KEY={target_key}")
        env_vars.append(f"DYNAMIC_IMAGE_TAG={dynamic_image_tag}")
        print("\n".join(env_vars))


if __name__ == "__main__":
    main(**vars(parse_args()))
