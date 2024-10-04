"""This script scans the build log for errors and warnings.

Warnings will be highlighted, but errors will a not-zero exit code
to signal failure in the build process and stops the workflow. 

To use this script, you need to:

1. Pass the required command-line arguments (file_path).
2. The script will print the error or warning line.
3. Prevent the execution of the next step if a error is detected.

You can run the script using the following command:

python ./scripts/identify_silent_errors.py {{ file_path }}

See the `parse_args` function for more details on the command-line arguments. Find a usage example in the `.github/workflows/build.yml` file.
"""

import re
import sys
import argparse

# List of keywords indicating critical errors
error_list = [
    "^Error",
    "ValueError",
    "Theme not found",
    "ERROR: Repository not found",
]

# List of keywords indicating warnings
warning_list = [
    "fatal: not a git repository (or any of the parent directories): .git",
    "Error: No such command 'init'",
]


def parse_error(build_logs):
    """
    Search for errors that does not stop the build process but
    result in an unusable image.

    Args:
        build_logs (file object): The build log file to scan.
    """
    for line_number, line in enumerate(build_logs, 1):
        if any(re.search(keyword, line) for keyword in warning_list):
            print("\033[33m", f"Warning at line {line_number}: {line}")
            continue

        if any(re.search(keyword, line) for keyword in error_list):
            sys.exit(
                f"\033[31m Error detected in build process at line {line_number}: {line}"
            )


def parse_args():
    """
    Parses the command-line arguments to get the log file path.

    Returns:
        argparse.Namespace: Parsed arguments including the 'file_path'.
    """
    parser = argparse.ArgumentParser(
        description="Process a build log file and search for errors and warnings."
    )
    parser.add_argument(
        "file_path",
        type=str,
        help="Path to the log file",
    )
    return parser.parse_args()


def main(args):
    """
    Main function to read the log file and call the error parsing function.

    Args:
        file_path (str): The path to the build log file that needs to be processed.
    """
    file_path = args.file_path

    with open(file_path, "r", encoding="utf-8") as build_logs_file:
        parse_error(build_logs_file)


if __name__ == "__main__":
    main(parse_args())
