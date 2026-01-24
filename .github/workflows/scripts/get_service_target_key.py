"""
Script to get the target key for a service from the service_tag_map.

This script is used to determine which config key corresponds to a given service
when dynamic image tags are not being used.
"""

import sys
import argparse
from service_tag_map import service_tag_map


def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Get the target key for a service from service_tag_map"
    )
    
    parser.add_argument(
        "--service",
        required=True,
        help="Service name to look up in service_tag_map"
    )
    
    return parser.parse_args()


def main():
    """Get and print the target key for the given service."""
    args = parse_args()
    
    if args.service not in service_tag_map:
        sys.exit(f"ERROR: Service '{args.service}' not found in service_tag_map")
    
    target_key = service_tag_map[args.service]
    print(target_key)


if __name__ == "__main__":
    main()
