import sys
from wordlepy import Wordle, getWordsList
import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", type=str, required=False, help="Directory in which to export the words")
    parser.add_argument("-d", action="store_true", help="Play don't wordle instead (https://dontwordle.com/)")
    parser.add_argument("-w", type=str, required=False, help="Automatically play against the specified word")
    parser.add_argument("-a", action="store_true", help="Automatically play against all words")
    args = parser.parse_args()
    if args.w is not None:
        wordle = Wordle(args.d, args.o)
        if len(args.w) != 5 or args.w not in wordle.winning_words:
            print("Invalid word")
            return 1
        wordle.playAutomatically(args.w)
    elif args.a:
        results = {}
        winning_words, _ = getWordsList()
        for word in winning_words:
            wordle = Wordle(args.d, args.o)
            guesses = wordle.playAutomatically(word)
            if guesses not in results:
                results[guesses] = 0
            results[guesses] += 1
        print(f"And the results are.....\nGuesses\tCounts\n")
        for i in sorted(results.keys()):
            print(f"{i}\t{results[i]}")
    else:
        wordle = Wordle(args.d, args.o)
        wordle.playInteractive()


if __name__ == "__main__":
    sys.exit(main())