"""
This module is the main entry point to the program.
It contains the main function and the test function.
"""

import argparse
from typing import Dict
import pytest
from logger import clear_logs, silence, unsilence
from gui import Game

def main() -> None:
    """
    Main entry point function to run the application.
    """
    game = Game()
    game.run()

def test(flags: Dict) -> None:
    """
    Run the tests for the application.

    :param flags: A dictionary containing the flags for the test.
    :type flags: dict
    """
    silence()
    local_flags = flags.copy()
    if not any(local_flags.values()):
        local_flags["st"] = True
    if list(local_flags.values()).count(True) > 1:
        print("Only one test flag can be used at a time. Use -h for help.")
        return

    ignore_standard = "--ignore=tests/standard_tests"
    ignore_full = "--ignore=tests/full_tests"

    if local_flags["qt"]:
        with open("pytest.ini", "w", encoding="UTF-8") as f:
            f.write(f"[pytest]\naddopts = {ignore_full} {ignore_standard}")
    if local_flags["st"]:
        with open("pytest.ini", "w", encoding="UTF-8") as f:
            f.write(f"[pytest]\naddopts = {ignore_full}")
    if local_flags["ft"]:
        with open("pytest.ini", "w", encoding="UTF-8") as f:
            f.write("[pytest]\n")
    pytest.main(["tests/", "-v"])
    unsilence()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("operation",
help="""Indicates the operation to be performed. Options: run, test, clear_logs""")

    parser.add_argument("-qt", "--quick-test",
                        help="Runs quick test when testing",
                        action="store_true")

    parser.add_argument("-st", "--standard-test",
                        help="Default testing option",
                        action="store_true")

    parser.add_argument("-ft", "--full-test",
                        help="Runs full test when testing",
                        action="store_true")

    args = parser.parse_args()
    cmd_flags = {"qt":args.quick_test,
            "st": args.standard_test,
            "ft": args.full_test}
    if args.operation == "run":
        main()
    elif args.operation == "test":
        test(cmd_flags)
    elif args.operation == "clear_logs":
        clear_logs()
    else:
        print("Invalid command. Use -h for help.")
