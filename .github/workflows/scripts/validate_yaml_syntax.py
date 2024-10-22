#!/usr/bin/env python3
"""
Validate the syntax of a YAML configuration file based on defined schema rules.

Checks performed:
- Valid YAML syntax.
- Presence of required keys.
- Correct formatting of optional arguments.
"""

import argparse
import logging
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml
from schema import And, Optional, Or, Regex, Schema, SchemaError, Use
from schema import __version__ as schema_version  # For version checking

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    from stack.domain.tutor_version import TutorVersion
except ImportError:
    logger.error("Module 'stack.domain.tutor_version' not found.")
    sys.exit(1)


def parse_arguments() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Validate the syntax of a YAML configuration file."
    )
    parser.add_argument(
        "file",
        type=Path,
        help="Path to the YAML configuration file.",
    )
    return parser.parse_args()


def load_yaml(file_path: Path) -> Optional[Dict[str, Any]]:
    """Load data from a YAML file."""
    try:
        with file_path.open("r", encoding="utf-8") as file:
            data = yaml.safe_load(file)
        return data
    except yaml.YAMLError as e:
        logger.error(f"Failed to parse YAML file: {file_path} | Error: {e}")
        return None
    except FileNotFoundError:
        logger.error(f"YAML file not found: {file_path}")
        return None


def define_schema() -> Schema:
    """Define the schema for the YAML configuration."""
    strain_schema = Schema(
        {
            "STRAIN_NAME": And(str, len, error="STRAIN_NAME must be a non-empty string"),
            "DEV_PROJECT_NAME": And(str, len),
            "LOCAL_PROJECT_NAME": And(str, len),
            "STRAIN_TUTOR_VERSION": Use(TutorVersion),
            Optional(Regex(r"(LMS|CMS)_HOST")): And(str, len),
            Optional(Regex(r"DISTRO_.+_DPKG")): {
                "index": And(str, len),
                "name": And(str, len),
                "repo": And(str, len),
                "domain": And(str, len),
                "path": And(str, len),
                "protocol": Or("ssh", "https"),
                "variables": dict,
                "version": And(str, len),
            },
            Optional("STRAIN_TUTOR_PLUGINS"): [
                Or(
                    {
                        "REPO": And(str, len),
                        "VERSION": And(str, len),
                        "EGG": And(str, len),
                        "PACKAGE_NAME": And(str, len),
                        Optional("PROTOCOL"): And(str, len),
                        Optional("DOMAIN"): And(str, len),
                        Optional("PATH"): And(str, len),
                    },
                    {
                        "PACKAGE_NAME": And(str, len),
                        "PACKAGE": And(str, len),
                    },
                )
            ],
            Optional("STRAIN_EXTRA_COMMANDS"): [
                {
                    "APP": And(str, len),
                    "COMMAND": And(str, len),
                }
            ],
            Optional("STRAIN_EXPORT_VOLUMES"): [
                {
                    "CONTAINER": And(str, len),
                    "LOCATION": And(str, len),
                    "DESTINATION": And(str, len),
                }
            ],
            Optional("STRAIN_VOLUME_OVERRIDES"): {
                Or("edxapp", "ecommerce", only_one=True): [
                    {
                        "DESTINATION": And(str, len),
                        "LOCATION": And(str, len),
                    }
                ]
            },
            Optional("DISTRO_THEMES_NAME"): And(list, len),
            Optional("DISTRO_THEME_DIRS"): And(list, len),
        },
        ignore_extra_keys=True,
    )
    return strain_schema


def validate_config(config: Dict[str, Any], schema: Schema) -> bool:
    """Validate the configuration data against the schema."""
    try:
        schema.validate(config)
        logger.info("Configuration is valid according to the schema.")
        return True
    except SchemaError as e:
        logger.error(f"Schema validation error: {e}")
        return False


def main() -> int:
    """Main function to validate YAML configuration syntax."""
    args = parse_arguments()
    config_data = load_yaml(args.file)

    if config_data is None:
        return 1

    schema = define_schema()
    is_valid = validate_config(config_data, schema)

    if is_valid:
        logger.info("YAML configuration file passed all syntax checks.")
        return 0
    else:
        logger.error("YAML configuration file failed syntax checks.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
