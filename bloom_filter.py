import pybloom_live

class DataStore:
    def __init__(self):
        self.nouns = None

    def populate_words(self, filename, cap, err):
        self.nouns = pybloom_live.BloomFilter(capacity=cap, error_rate=err)       
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                for line in file:
                    line = line.strip()  # Remove leading/trailing whitespace and newline characters
                    self.nouns.add(line)
        except FileNotFoundError:
            print(f"File {filename} not found.")

    # Check if a word is in the lexicon using the Bloom filter
    # This method returns True if the word is possibly in the lexicon, and False if it is definitely not in the lexicon.
    def is_word_in_lexicon(self, word):
        return word in self.nouns
    
# print(len(nouns))
# print('பழம்' in nouns)
# print('வண்டு' in nouns)