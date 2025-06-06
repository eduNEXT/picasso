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


def update_image_name(current_image_name: str,  tutor_version: str, service: str, 
                      prefix: str, timestamp_format: str, use_random_suffix: bool, 
                      length: int = 4) -> str:
    """
    Generate a new image tag based on the base name, timestamp, and optional random suffix.

    Args:
        current_image_name (str): The original image name with tag.
        service (str): The name of the service (not used directly here but passed through).
        prefix (str): Prefix for the generated tag (usually the Open edX release name).
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
    updated_image_name = f"{current_image_name_without_tag}:{tutor_version}-{prefix}{timestamp}"

    if use_random_suffix:
        suffix = f"-{random_part}"
        updated_image_name = f"{updated_image_name}{suffix}"

    return updated_image_name


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
        "--prefix",
        default="openedx",
        help="Prefix to prepend to the image tag. Typically the Open edX release name (e.g., 'olive').",
    )
    parser.add_argument(
        "--timestamp-format",
        default="%Y%m%d-%H%M",
        help="Timestamp format to include in the image tag. Uses Python's strftime syntax.",
    )
    parser.add_argument(
        "--use-random-suffix",
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
        "--image-name",
        default=None,
        help="Image name to override the one defined in config.yml before building the new image.",
    )

    return parser.parse_args()


def main(config_file: str = "config.yml", service: str = None, prefix: str = "", 
         timestamp_format: str = "%Y%m%d-%H%M", use_random_suffix: bool = False, 
         save_config: bool = False, image_name: str = None) -> None:
    """
    Load configuration, generate a dynamic image tag, and print or update config.

    Args:
        config_file (str): Path to the Tutor config file.
        service (str): Name of the service to be tagged.
        prefix (str): Prefix to use in the image tag.
        timestamp_format (str): Format for the timestamp.
        use_random_suffix (bool): Whether to append a random suffix to the tag.
        save_config (bool): If True, the image name will be saved directly to config.yml.
        image_name (str): The image name to save (used only if save_config is True).
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
        if not image_name:
            sys.exit("ERROR: --image-name must be provided when --save-config is true")

        tutor_config[target_key] = image_name
        write_config_file(config_file, tutor_config)
    else:
        dynamic_image_name = update_image_name(
            current_image_name=tutor_config[target_key],
            tutor_version=tutor_config["TUTOR_VERSION"],
            service=service,
            prefix=prefix,
            timestamp_format=timestamp_format,
            use_random_suffix=use_random_suffix,
        )

        env_vars = []
        env_vars.append(f"TARGET_KEY={target_key}")
        env_vars.append(f"DYNAMIC_IMAGE_NAME={dynamic_image_name}")
        print("\n".join(env_vars))


if __name__ == "__main__":
    main(**vars(parse_args()))
