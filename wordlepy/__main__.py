import sys
from wordlepy import Wordle
import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", action="store_true", help="Play don't wordle instead (https://dontwordle.com/)")
    args = parser.parse_args()
    Wordle(args.d)


if __name__ == "__main__":
    sys.exit(main())