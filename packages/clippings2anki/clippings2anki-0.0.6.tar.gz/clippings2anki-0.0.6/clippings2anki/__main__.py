import sys
sys.path.append("")

import clippings2anki.clippings as clippings

if __name__ == "__main__":
    # read cli arguments
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", type=str)
    parser.add_argument("language", type=str)
    args = parser.parse_args()

    clippings.main(args.input_file, args.language)
