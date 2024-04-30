"""Command line interface for hashing files."""

from argparse import ArgumentParser

from . import challenge
from .hash import Schwa
import os

def main():

    parser = ArgumentParser()
    parser.add_argument('-p', default=challenge.p, type=int)
    parser.add_argument('file', type=str)
    args = parser.parse_args()


    # First check if our input is a file
    if not os.path.isfile(args.file):
        print("First argument must be a file - exiting now!")
        exit(-1)

    schwa7 = Schwa(args.p)
    print(schwa7)

    with open(args.file, 'rb') as file:

        contents = file.read()
        bs = schwa7.hash_bytes(contents)

        as_int = int.from_bytes(bs)
        print(80 * "=")
        print(hex(as_int)[2:])



if __name__ == '__main__':
    main()
