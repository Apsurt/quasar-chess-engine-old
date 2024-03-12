import argparse
from quasar.gui import Game

def main():
    print("Running main")
    game = Game()
    game.run()

def test():
    print("Running tests")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("operation", help="Indicates the operation to be performed. Options: run, test")

    parser.add_argument("-qt", "--quick-test", help="Runs quick test when testing", action="store_true")
    parser.add_argument("-st", "--standard-test", help="Default testing option", action="store_true")
    parser.add_argument("-ft", "--full-test", help="Runs full test when testing", action="store_true")

    args = parser.parse_args()
    if args.operation == "run":
        main()
    elif args.operation == "test":
        test()
    else:
        print("Invalid command. Use -h for help.")