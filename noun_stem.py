import bloom_filter
from noun_functions import remove_behind_ku_suffixes, remove_idam_udan_vetrumai_mei_mudhal_suffixes, remove_behind_ai_suffixes, remove_ku_vetrumai_suffix, remove_vetrumai_uyir_mudhal_suffixes, remove_plural_suffix

data_store = bloom_filter.DataStore()
data_store.populate_words('unique_sorted_noun_master.txt', 200000, 0.001)    # Nouns: 1,53,548  -> 200000

# Define the list of affix stripping functions
affix_stripping_functions = [
    remove_behind_ku_suffixes,
    remove_idam_udan_vetrumai_mei_mudhal_suffixes,
    remove_behind_ai_suffixes,
    remove_ku_vetrumai_suffix,
    remove_vetrumai_uyir_mudhal_suffixes,
    remove_plural_suffix,
]
def noun_stemmer(word):
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
        print(word)
    else:
        is_affix_removed = False
        word = noun_stemmer(word)      # Recursive call to stem the word iteratively
    return word

word = "மரங்களுக்கருகிலிருந்து"  

# If the word has a match in the lexicon, we have the stem already. Nothing further needs to be done.
if data_store.is_word_in_lexicon(word):
    print(word)
else:
    word = noun_stemmer(word)     
