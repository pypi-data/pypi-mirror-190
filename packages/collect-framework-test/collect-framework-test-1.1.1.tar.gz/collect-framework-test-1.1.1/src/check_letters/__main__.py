import argparse
from collect_framework_test.src.check_letters.main import count_unique_chars, count_unique_chars2


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--string", type=str, help="A string to process")
    parser.add_argument("--file", type=str, help="A path to a text file to process")
    args = parser.parse_args()
    # Priority goes to the --file argument
    if args.file:
        with open(args.file, "r") as f:
            text = f.read()
    elif args.string:
        text = args.string
    else:
        print("Please provide either a --string or --file argument.")
        return
    cache = {}
    unique_chars = count_unique_chars(text, cache)
    print(f"Number of unique characters in text (method 1): {unique_chars}")
    unique_chars = count_unique_chars2(text)
    print(f"Number of unique characters in text (method 2): {unique_chars}")


if __name__ == "__main__":
    main()