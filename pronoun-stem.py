import bloom_filter
from noun_functions import remove_behind_ku_suffixes, remove_idam_udan_vetrumai_mei_mudhal_suffixes, remove_behind_ai_suffixes, remove_ku_vetrumai_suffix, remove_vetrumai_uyir_mudhal_suffixes, remove_plural_suffix

data_store = bloom_filter.DataStore()
data_store.populate_words('pronouns.txt', 200, 0.001)    # Pronouns: 26  -> 200

# உம், எம் arise from stripping the plural/respect suffix கள் from உங்கள், எங்கள்
irregular_pronouns = {
    'என்': 'நான்',
    'என': 'நான்',
    'உன்': 'நீ',
    'உன': 'நீ',
    'நம்': 'நாம்',
    'தன்': 'தான்',
    'தம்': 'தாம்',
    'உம்': 'நீங்கள்',
    'எம்': 'நாங்கள்',
    'இவற்று': 'இவை',
    'அவற்று': 'அவை',
    }

# Define the list of affix stripping functions of nouns that work as is for pronouns as well
affix_stripping_functions = [
    remove_behind_ku_suffixes,
    remove_idam_udan_vetrumai_mei_mudhal_suffixes,
    remove_behind_ai_suffixes,
    remove_ku_vetrumai_suffix,
    remove_vetrumai_uyir_mudhal_suffixes,
    remove_plural_suffix,
    ]
def pronoun_stemmer(word):
    is_affix_removed = False
    # Iterate through each affix stripping function, and execute it
    for func in affix_stripping_functions:
        word, is_affix_removed = func(word, is_affix_removed)
        if is_affix_removed:
            if data_store.is_word_in_lexicon(word):
                print(word)
                return
    # If no suffix is found in this iteration, nothing further can be done.
    if is_affix_removed == False:
        if word in irregular_pronouns:
            word = irregular_pronouns[word]
        print(word)
    else:
        is_affix_removed = False
        word = pronoun_stemmer(word)      # Recursive call to stem the word iteratively
    return word

word = "எங்களுக்குப்பிறகு" 

# If the word has a match in the lexicon, we have the stem already. Nothing further needs to be done.
if data_store.is_word_in_lexicon(word):
    print(word)
else:
    word = pronoun_stemmer(word)