import argparse
import pytest

def main():
    from gui import Game
    print("Running main")
    game = Game()
    game.run()

def test(flags):
    print("Running tests")
    if not any(flags.values()):
        flags["st"] = True
    if list(flags.values()).count(True) > 1:
        print("Only one test flag can be used at a time. Use -h for help.")
        return
    if flags["qt"]:
        with open("pytest.ini", "w") as f:
            f.write("[pytest]\naddopts = --ignore=lib --ignore=tests/full_tests --ignore=tests/standard_tests")
    if flags["st"]:
        with open("pytest.ini", "w") as f:
            f.write("[pytest]\naddopts = --ignore=tests/full_tests ")
    if flags["ft"]:
        with open("pytest.ini", "w") as f:
            f.write("[pytest]\naddopts = --ignore=lib")
    pytest.main(["tests/"])

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("operation", help="Indicates the operation to be performed. Options: run, test, clear_logs")

    parser.add_argument("-qt", "--quick-test", help="Runs quick test when testing", action="store_true")
    parser.add_argument("-st", "--standard-test", help="Default testing option", action="store_true")
    parser.add_argument("-ft", "--full-test", help="Runs full test when testing", action="store_true")

    args = parser.parse_args()
    flags = {"qt":args.quick_test,
            "st": args.standard_test,
            "ft": args.full_test}
    if args.operation == "run":
        main()
    elif args.operation == "test":
        test(flags)
    elif args.operation == "clear_logs":
        from logger import clear_logs
        clear_logs()
    else:
        print("Invalid command. Use -h for help.")