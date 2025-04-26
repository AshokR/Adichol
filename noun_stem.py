import bloom_filter

data_store = bloom_filter.DataStore()
data_store.populate_words('unique_sorted_noun_master.txt', 200000, 0.001)    # Nouns: 1,53,548  -> 200000
is_affix_removed = False
vallinam = ("க", "ச", "ட", "த", "ப", "ற")
nedil_ah_yay_oh = ["ா","ே","ோ"]
nedil_ah_ee = ["ா", "ீ"]

# Define behind ஐ வேற்றுமை மெய் முதல் suffixes
behind_ai_suffixes = ["ப்பற்றி", "க்குறித்து", "ப்பார்த்து", "நோக்கி", "ச்சுற்றி", "த்தாண்டி", "த்தவிர்த்து", "த்தவிர", "க்கொண்டு", "வைத்து", "விட்டு", "ப்போல", "மாதிரி", "விட"] 
def remove_behind_ai_suffixes(word):
    # Iterate through each behind ஐ வேற்றுமை suffix, remove it if found and also fix the ending
    for s in behind_ai_suffixes:
        if word.endswith(s):                # மரத்தைத்தாண்டி, மரத்தைவிட
            global is_affix_removed 
            is_affix_removed = True
            word = word[:-len(s)]
            return word    
    return word

# Define ஐ, ஆல், இல், இன், இடம், உடன், உடைய, ஓடு வேற்றுமை உயிர் முதல் suffixes
vetrumai_uyir_mudhal_suffixes = ["ிடம்", "ுடன்", "ுடைய", "ோடு", "ண்டை", "ருகே", "ருகில்", "ில்லாமல்", "ல்லாமல்", "ாட்டம்", "ொழிய", "ொட்டி", "ிருந்து", "ிலிருந்து", "ை", "ால்", "ில்", "ின்", "து"] 
def remove_vetrumai_uyir_mudhal_suffixes(word):
    for s in vetrumai_uyir_mudhal_suffixes:
        if word.endswith(s):
            global is_affix_removed 
            is_affix_removed = True
            vallinam_list = list(vallinam)
            vallinam_list.remove("ட")
            vallinam_less_ta = tuple(vallinam_list)
            word = word[:-len(s)]
            if word.endswith("வ"): 
                if word[-2:-1] in nedil_ah_ee:          # if the prior உயிர் is ஆ, ஈ
                    if len(word) < 4:                   # ஓரசை is max 4 code points # சாவு, காவு, மாவு, தீவு
                        return word + "ு"
                    else:                               # பைசா, நாடா, மாதா, அம்மா, கோவா, பிரமிளா, புறா, பாட்னா, ராஜா
                        return word[:-len("வ")] 
                else:
                    return word + "ு"                  # கழிவு, செலவு, கனவு
            elif word.endswith("ய"):
                if word[-2:-1] in nedil_ah_yay_oh:       # if the prior உயிர் is ஆ, ஏ, ஓ
                    return word + "்"                    # வாய், பாய், தாய், குழாய், நோய், பேய், ஓநாய்
                else:
                    return word[:-len("ய")]             # பொய், கை, தீ, பசை, வாழை, பிறவி
            elif word[-1:] == word[-3:-2]:               # if repeat மெய் 
                if word.endswith("த்த"):                 # மரம், கோகிலம்
                    return word[:-len("த்த")] + "ம்"
                elif word.endswith("ட"):
                    return word[:-len("்ட")] + "ு"     # கோடு, ஏடு, வீடு, ஆடு, மேடு, காடு
                elif word.endswith(vallinam_less_ta):    # நெருப்பு, செக்கு, மத்து, காற்று  
                    return word + "ு"
                else:                                    # செங்கல், கள், கண், மண்
                    return word[:-1]
            elif word.endswith(vallinam):                # மிளகு, கிணறு, பாகு, காசு
                return word + "ு"
            else:
                return word + "்"                        # சுவர், தண்ணீர், மரத்தின், மரங்கள், வாழையின், மிளகின், புறாவின்
    return word                                      

# Define behind கு வேற்றுமை suffixes
behind_ku_suffixes = ["ப்பிறகு", "ப்புறம்", "ப்பால்", "மேல்", "கீழ்", "ள்ளே", "வெளியே", "வெளியில்", "டியில்", "ருகில்", "முன்", "முன்னால்", "ப்பின்", "ப்பின்னால்", "ப்பின்பு", "ப்பிந்தி", "ப்பதிலாக", "ாக"] # பின்னர், முன்னர், முன்பு, முந்தி ???
def remove_behind_ku_suffixes(word):
    # Iterate through each behind கு வேற்றுமை suffix, remove it if found and also fix the ending
    for s in behind_ku_suffixes:
        if word.endswith(s):
            global is_affix_removed 
            is_affix_removed = True
            word = word[:-len(s)]
            if word.endswith("கு"):          # மரத்துக்குப்பதிலாக
                return word
            elif word.endswith("க"):        # மரங்களுக்கருகிலிருந்து
                return word + "ு"                 
            else:
                is_affix_removed = False
                return word + s
    return word

# Define கு வேற்றுமை suffix
ku_vetrumai_suffix = "க்கு"
def remove_ku_vetrumai_suffix(word):
    # Check கு வேற்றுமை suffix, remove it if found and also fix the ending
    if word.endswith(ku_vetrumai_suffix):
            global is_affix_removed 
            is_affix_removed = True
            vallinam_list = list(vallinam)
            vallinam_list.remove("ட")
            vallinam_less_ta = tuple(vallinam_list)
            word = word[:-len(ku_vetrumai_suffix)]
            if word.endswith("வு"): 
                word = word[:-len("வு")]
                if word[-2:-1] in nedil_ah_ee:          # if the prior உயிர் is ஆ, ஈ
                    if len(word) < 3:                   # ஓரசை is max 4 code points # சாவு, காவு, மாவு, தீவு
                        return word + "வு"
                    else:                               # பைசா, நாடா, மாதா, அம்மா, கோவா, பிரமிளா, புறா, பாட்னா, ராஜா
                        return word 
                else:
                    return word + "வு"                   # கழிவு, செலவு, கனவு
            elif word[-2:-1] == word[-4:-3]:             # if repeat மெய் 
                word = word[:-len("ு")]
                if word.endswith("த்த"):                 # மரம், கோகிலம்
                    return word[:-len("த்த")] + "ம்"
                elif word.endswith("ட"):
                    return word[:-len("்ட")] + "ு"     # கோடு, ஏடு, வீடு, ஆடு, மேடு, காடு
                elif word.endswith(vallinam_less_ta):    # நெருப்பு, செக்கு, மத்து, காற்று  
                    return word + "ு"
                else:                                    # செங்கல், கள், கண், மண்
                    return word[:-1]
            elif word.endswith(vallinam):                # மிளகு, கிணறு, பாகு, காசு
                return word + "ு"
            elif word.endswith("ு"):
                word = word[:-len("ு")]
                return word + "்"                        # சுவர், தண்ணீர், மரத்தின், மரங்கள், வாழையின், மிளகின், புறாவின்
            else:
                return word                              # தாய், ஓநாய், நோய், பேய், வாழை, மலை, பாதை, சேனை, புளி, பழி, மாயை, தீ, கை, பை, பிறவி
    return word                                          

# Define இடம், உடன் வேற்றுமை மெய் முதல் suffixes
idam_udan_vetrumai_mei_mudhal_suffixes = ["மூலம்", "பக்கம்", "கிட்ட", "மேல்", "மேலே", "கீழ்","கீழே", "வரைக்கும்", "வரையில்", "முதல்", "படி", "வழியாக"]
def remove_idam_udan_vetrumai_mei_mudhal_suffixes(word):
    # Iterate through each இடம் வேற்றுமை மெய் முதல் suffix, remove it if found
    for s in idam_udan_vetrumai_mei_mudhal_suffixes:
        if word.endswith(s):                    # காடுவரைக்கும்
            global is_affix_removed 
            is_affix_removed = True
            word = word[:-len(s)]
            return word   
    return word

# Define plural suffix
plural_suffix = "கள்"
def remove_plural_suffix(word):
     # Check பன்மை suffix, remove it if found and also fix the ending
    if word.endswith(plural_suffix):
            global is_affix_removed 
            is_affix_removed = True
            word = word[:-len(plural_suffix)]
            if word.endswith("ங்"):                  # மரங்கள்
                return word[:-len("ங்")] + "ம்"
            elif word.endswith("க்"):                # பூக்கள், பசுக்கள்
                return word[:-len("க்")]
            elif word.endswith("ற்"):                # பற்கள், கற்கள்
                return word[:-len("ற்")] + "ல்"
            elif word.endswith("ட்"):                # ஆட்கள், முட்கள்
                return word[:-len("ட்")] + "ள்"
            else:                                   # கண்கள்
                return word
    return word

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
    global is_affix_removed
    # Iterate through each affix stripping function, and execute it
    for func in affix_stripping_functions:
        word = func(word)
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
