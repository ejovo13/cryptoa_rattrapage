"""Command line interface for hashing files."""

from argparse import ArgumentParser

from . import challenge

def main():

    parser = ArgumentParser()
    parser.add_argument('-p', default=challenge.p)
    args = parser.parse_args()
    print(f"p: {args.p}")



if __name__ == '__main__':
    main()
