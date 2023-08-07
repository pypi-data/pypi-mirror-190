import re
from wiktionaryparser import WiktionaryParser
import json
from tqdm import tqdm

from flashcards import get_flashcard
from anki import save_to_text


def main(input_file, language):
    #! read the clippings file
    with open(input_file, "r") as f:
        clippings = f.read()
    
    clip_re = re.compile(r"(.*)\n==========")
    
    # find all matches
    clips = clip_re.findall(clippings)
    
    clips_set = set()
    
    for clip in clips:
        if not clip:
            continue

        # remove punctuation from the clip
        clip = re.sub(r"[^\w\s]", "", clip)

        # print(clip)
        clips_set.add(clip)
        
    print(f"{len(clips_set)} clippings found")
    print()

    #! get the definitions of the words from wiktionary
    parser = WiktionaryParser()
    parser.set_default_language(language)
    
    flashcards = {}

    for i in tqdm(clips_set):
        word, f = get_flashcard(i, parser)
        
        if not word:
            continue
        
        flashcards[word] = f
    
    # save the flashcards to json file
    with open("flashcards.json", "w") as f:
        json.dump(flashcards, f, indent=4)
    print("flashcards saved to flashcards.json")
    
    #! save the flashcards to anki-friendly text file
    save_to_text(flashcards)
    print("flashcards saved to flashcards.txt")


if __name__ == "__main__":
    input_file = "Kindle My Clippings.txt"
    language = "english"
    
    main(input_file, language)
