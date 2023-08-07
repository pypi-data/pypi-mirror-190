from clippings import main


if __name__ == "__main__":
    # read cli arguments
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", type=str)
    parser.add_argument("language", type=str)
    args = parser.parse_args()

    main(args.input_file, args.language)
