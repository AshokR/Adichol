import bloom_filter

data_store = bloom_filter.DataStore()
data_store.populate_words('verbs.txt', 3000, 0.001)      # Verbs: 2764 -> 3000
is_affix_removed = False
mei = ("க", "ங", "ச", "ஞ", "ட", "ண", "த", "ந", "ப", "ம", "ய", "ர", "ல", "வ", "ழ", "ள", "ற", "ன")
# word_ending_mei = ("ண", "ம", "ய", "ர", "ல", "ழ", "ள", "ன")
u_ending_mei = ("க", "ச", "ட", "த", "ப", "ற", "வ")
pulli_ending_mei = ("ர", "ழ", "ள")
nedil = ["ா", "ீ", "ூ", "ே", "ை", "ோ", "ௌ"]
migumvali = ("க்", "ச்", "த்", "ப்")
nedil_ah_ee = ["ா", "ீ"]

irregular_infinitives = {
    'வர': 'வா',
    'போக': 'போ',
    'சாக': 'சா',
    'எழ': 'எழு',
    'விழ': 'விழு',
    'அழ': 'அழு',
    'உழ': 'உழு',
    'கோர': 'கோரு',
    'அள்ள': 'அள்ளு',
    'துள்ள': 'துள்ளு',
    'கிள்ள': 'கிள்ளு',
    'தள்ள': 'தள்ளு'
    }

irregular_avps = {
    'வந்து': 'வா',
    'போய்': 'போ',
    'சொல்லி': 'சொல்',
    'செத்து': 'சா',
    'கேட்டு' : 'கேள்',
    'மீட்டு' : 'மீள்',
    'உண்டு' : 'உண்',
    'கண்டு' : 'காண்',
    'தின்று' : 'தின்',
    'என்று' : 'என்',
    'பெற்று' : 'பெறு',
    'விடைபெற்று' : 'விடைபெறு',
    'நோயுற்று' : 'நோயுறு',
    'துன்புற்று' : 'துன்புறு',
    'ஐயுற்று' : 'ஐயுறு',
    'தோல்வியுற்று' : 'தோல்வியுறு'
    }

# Define பன்மை/மதிப்பு suffix
plural_suffix = "கள்"
# Check பன்மை/மதிப்பு suffix, remove it if found
def remove_plural_suffix(word):     
    if word.endswith(plural_suffix):    # செய்யமாட்டார்கள், வாங்கினீர்கள், வாங்கினார்கள்
            global is_affix_removed 
            is_affix_removed = True
            word = word[:-len(plural_suffix)]
            return word
    return word

# Define verb negative suffixes - past/prsent; இல்லை, future: மாட்டேன்..., அஃறிணை: ஆது
negative_suffixes = ["வில்லை", "மாட்டேன்", "மாட்டோம்", "மாட்டான்", "மாட்டாள்", "மாட்டார்", "ாது"] 
def remove_negative_suffixes(word):
    # Iterate through each verb negative suffix, remove it if found and also fix the ending
    for s in negative_suffixes:
        if word.endswith(s):            # உண்ணவில்லை, வாங்கிக்கொள்ளவில்லை, வாங்கமாட்டேன், செய்யமாட்டார்கள், செய்யாது        
            global is_affix_removed 
            is_affix_removed = True
            word = word[:-len(s)]
            word = convert_infinitive_to_the_root_verb(word)
            return word    
    return word

# Define verb level 4 மெய் முதல் suffixes
# Should look for "தீர்" only after "த்தீர்" in level 3 PNG suffixes
level4_mei_mudhal_suffixes = [
    "காட்டு", "காட்டி", "கொடு", "வை", "பார்", "கொண்டிரு", "கொள்", "கொண்", "போடு", "போட்", 
    "விடு", "விட்", "போ", "தொலை", "தள்ளு", "தள்ளி", "கிழி", "கிட", "தீர்", "முடி"
    ] 
def remove_level4_mei_mudhal_suffixes(word):
    # Iterate through each verb level 4 மெய் முதல் suffix, if found, remove it and everything that comes after
    for s in level4_mei_mudhal_suffixes:
        index = word.find(s)
        if index > 0:                   # செய்துகொண்டிரு, செய்துகொண்டிருந்தேன், செய்துகொண்டிருக்கின்றார்கள், செய்துகொண்டிருக்கும்
            global is_affix_removed    # வாங்கிப்போனார்கள், செய்துமுடித்தான்
            is_affix_removed = True    # காட்டு -> காட்டி, கொள் -> கொண், போடு -> போட், விடு -> விட், தள்ளு -> தள்ளி
            word = word[:index]
            if word.endswith(migumvali):
                word = word[:-len("க்")]   # விட்டுத்தொலை -> விட்டுத், வாங்கிக்கொள் -> வாங்கிக்                
            # word = convert_avp_to_the_root_verb(word)
            return word    
    return word

# Define verb level 3 and 4 உயிர் முதல் suffixes
level3_4_uyir_mudhal_suffixes = ["ிரு", "ாயிற்று", "ியல"] 
def remove_level3_4_uyir_mudhal_suffixes(word):
    # Iterate through each verb level 4 மெய் முதல் suffix, remove it if found and also fix the ending
    for s in level3_4_uyir_mudhal_suffixes:
        index = word.find(s)
        if index > 0:                # நினைத்திரு, பார்த்தாயிற்று, பார்க்கவியலும், பார்க்கவியலாது, சொல்லயியலாது, சொல்லியாயிற்று
            global is_affix_removed 
            is_affix_removed = True
            word = word[:index]
            if word.endswith("வ") or word.endswith("ய"):
                word = word[:-len("வ")]
            return word    
    return word

# Define verb level 3 மெய் முதல் suffixes
level3_mei_mudhal_suffixes = [
    "செய்", "பண்ணு", "வை", "பார்", "வா", "போ", "வேண்டியிரு", "வேண்டிவா", "வேண்டிவ", 
    "முடி", "மாட்", "கூடாது", "கூடும்", "வேண்டாம்", "வேண்டும்", "ட்டும்"
    ] 
def remove_level3_mei_mudhal_suffixes(word):
    # Iterate through each verb level 3 மெய் முதல் suffix, if found, remove it and everything that comes after
    for s in level3_mei_mudhal_suffixes:
        index = word.find(s)                # பார்க்கப்போனேன், பார்க்கப்போவதில்லை, பார்க்கமுடியாது
        if index > 0:                
            global is_affix_removed 
            is_affix_removed = True
            word = word[:index]
            return word             # பார்க்கப்போகவில்லை, பார்க்கப்போனேன்/போகிறேன்/போவேன், பார்க்கட்டும்
    return word

# Define past tense னேன் PNG (Person/Number/Gender) suffixes
past_tense_neen_PNG_suffixes = ["னேன்", "னோம்", "னாய்", "னீர்", "னான்", "னாள்", "னார்", "யது", "னது", "ிற்று", "ன"] 
def remove_past_tense_neen_PNG_suffixes(word):
    # Iterate through each past tense னேன் PNG suffix, remove it if found and also fix the ending
    for s in past_tense_neen_PNG_suffixes:
        if word.endswith(s):
            global is_affix_removed 
            is_affix_removed = True
            word = word[:-len(s)]
            if word in ("போ", "போய"):                     # போனேன், ... போனது, போயிற்று, போயின 
                return "போ"
            elif word in ("சொன்", "சொல்ல"):               # சொன்னேன், ... சொன்னது, சொல்லிற்று, சொல்லின
                return "சொல்"                 
            elif word in ("ஆ", "ஆகி", "ஆய"):              # ஆனேன்/ஆகினேன், ... ஆனது, ஆயிற்று, ஆகின
                return "ஆகு" 
            elif word.endswith("ி"):                            # வாங்கு, உதவு, எழுது, எழுப்பு, ஆடு, விரட்டு, அள்ளு, மாற்று, நீக்கு, அணுகு
                return word[:-1] + "ு"                       
            elif word.endswith(mei):                             # ஓடிற்று, ஆடிற்று
                return word + "ு"
    return word

# Define past tense டேன் PNG (Person/Number/Gender) suffixes
# உண்டேன், கண்டேன், கேட்டேன், மீட்டேன், ஆண்டேன், விட்டேன், பட்டேன், தொட்டேன்
past_tense_Teen_PNG_suffixes = ["டேன்", "டோம்", "டாய்", "டீர்", "டான்", "டாள்", "டார்", "டது", "டன"] 
def remove_past_tense_Teen_PNG_suffixes(word):
    # Iterate through each past tense னேன் PNG suffix, remove it if found and also fix the ending
    for s in past_tense_Teen_PNG_suffixes:
        if word.endswith(s):
            global is_affix_removed 
            is_affix_removed = True
            word = word[:-len(s)]
            if word in ("உண்"):                  # உண்டேன்
                return word
            elif word in ("கண்"):                 # கண்டேன்
                return "காண்"                 
            elif word.endswith("ண்"):              # ஆண்டேன், உருண்டேன், கொண்டேன்...
                return word[:-len("ண்")] + "ள்"
            elif word.endswith("ட்"):  
                # if the prior uyir is nedil (கேள், மீள்)            
                if word[-3:-2] in nedil:            # கேட்டேன், மீட்டேன்...
                    return word[:-len("ட்")] + "ள்"
                else:                                # விடு, படு, தொடு, இடு
                    word = word[:-1]
                    return word + "ு"    
    return word

# Define past tense ந்தேன் PNG (Person/Number/Gender) suffix
past_tense_ndteen_PNG_suffix = "ந்தேன்" 
def remove_past_tense_ndteen_PNG_suffix(word):
    # Remove past tense றேன் PNG suffix if found and also fix the ending
    if word.endswith(past_tense_ndteen_PNG_suffix):
        global is_affix_removed 
        is_affix_removed = True
        word = word[:-len(past_tense_ndteen_PNG_suffix)]    # நட, கட, கர, இரு, மற, பற, இழ, விய
        return word
    return word

# Define past tense தேன் PNG (Person/Number/Gender) suffixes
past_tense_teen_PNG_suffixes = ["தேன்", "தோம்", "தாய்", "தீர்", "தான்", "தாள்", "தார்", "தது", "தன"] 
def remove_past_tense_teen_PNG_suffixes(word):
    # Iterate through each past tense தேன் PNG suffix, remove it if found and also fix the ending
    for s in past_tense_teen_PNG_suffixes:
        if word.endswith(s):
            global is_affix_removed 
            is_affix_removed = True
            word = word[:-len(s)]
            if word.endswith("த்"):
                if word == "செத்":                 # செத்தேன்
                    return "சா"
                else:                               # கொடு, பொறு, இழு, சிரி, உதை, இணை, பார், கா
                    return word[:-len("த்")]
            else:                                   # செய். வை (scold), அழு
                return word
    return word

# Define past tense றேன் PNG (Person/Number/Gender) suffix
past_tense_Reen_PNG_suffix = "றேன்" 
def remove_past_tense_Reen_PNG_suffix(word):
    # Remove past tense றேன் PNG suffix if found and also fix the ending
    if word.endswith(past_tense_Reen_PNG_suffix):
        global is_affix_removed 
        is_affix_removed = True
        word = word[:-len(past_tense_Reen_PNG_suffix)]
        if word in ["தின்", "என்"]:          # தின், என்
            return word
        else:                                  # நில், வெல், கொல், செல், மெல்
            return word[:-len("ன்")] + "ல்"     
    return word        

# Define present tense கிறேன் PNG (Person/Number/Gender) suffixes
present_tense_kiReen_PNG_suffixes = ["கிறேன்", "கிறோம்", "கிறாய்", "கிறீர்", "கிறான்", "கிறாள்", "கிறார்", "கிறது", "கின்றன"] 
def remove_present_tense_kiReen_PNG_suffixes(word):
    # Iterate through each present tense கிறேன் PNG suffix, remove it if found and also fix the ending
    for s in present_tense_kiReen_PNG_suffixes:
        if word.endswith(s):
            global is_affix_removed 
            is_affix_removed = True
            word = word[:-len(s)]
            if word.endswith("க்"):                                                   # கொடு, அழி, சிரி, உதை, சாய், சேர், வை (put), கா
                return word[:-len("க்")]
            elif word.endswith("ற்"):                                                  # நில், தோல் (lose), வில் (sell), கல் (learn)
                return word[:-len("ற்")] + "ல்"
            elif word.endswith("ட்"):                                                  # கேள், மீள்
                return word[:-len("ட்")] + "ள்"
            elif word.endswith("ஆ") or word.endswith("ா"):                         # ஆகு, அடிமையாகு, தூய்மையாகு...
                return word + "கு"
            elif word.endswith("ரு"):                                                  # வா, தா
                return word[:-len("ரு")] + "ா"
            else:                                
                return word    
    return word

# Define future tense பேன் PNG (Person/Number/Gender) suffixes
future_tense_peen_PNG_suffixes = ["பேன்", "போம்", "பாய்", "பீர்", "பான்", "பாள்", "பார்"] 
def remove_future_tense_peen_PNG_suffixes(word):
    # Iterate through each future tense பேன் PNG suffix, remove it if found and also fix the ending
    for s in future_tense_peen_PNG_suffixes:
        if word.endswith(s):
            global is_affix_removed 
            is_affix_removed = True
            word = word[:-len(s)]
            if word.endswith("ப்"):                 # கொடு, அழி, சிரி, உதை, சாய், சேர், வை (put), கா
                return word[:-len("ப்")]
            elif word.endswith("ற்"):               # நில், தோல் (lose), வில் (sell), கல் (learn)
                return word[:-len("ற்")] + "ல்"
            elif word.endswith("ட்"):               # கேள், மீள்
                return word[:-len("ட்")] + "ள்"
            else:                                
                return word    
    return word

# Define future tense வேன் PNG (Person/Number/Gender) suffixes
future_tense_veen_PNG_suffixes = ["வேன்", "வோம்", "வாய்", "வீர்", "வான்", "வாள்", "வார்"] 
def remove_future_tense_veen_PNG_suffixes(word):
    # Iterate through each future tense வேன் PNG suffix, remove it if found and also fix the ending
    for s in future_tense_veen_PNG_suffixes:
        if word.endswith(s):
            global is_affix_removed 
            is_affix_removed = True
            word = word[:-len(s)]
            if word.endswith("ரு"):                 # வா, தா
                return word[:-len("ரு")] + "ா"
            elif word == "ஆ":                      # ஆகு
                return word + "கு"
            else:                                    # அழு, சா, செல், பெறு, வாங்கு, ஆடு, தள்ளு, நீக்கு, சொல், சேர், வாழ், ஆள், விடு, படு, இடு, கொள், பயில்                           
                return word    
    return word

# Define future tense அஃறிணை PNG (Person/Number/Gender) suffix
future_tense_ahrinai_PNG_suffix = "ும்" 
def remove_future_tense_ahrinai_PNG_suffix(word):
    if word.endswith(future_tense_ahrinai_PNG_suffix):
        global is_affix_removed 
        is_affix_removed = True
        word = word[:-len(future_tense_ahrinai_PNG_suffix)]
        word = convert_infinitive_to_the_root_verb(word)                 
        return word
    else:    
        return word

# Convert infinitive form to the root verb
def convert_infinitive_to_the_root_verb(word):
    global is_affix_removed 
    is_affix_removed = True
    if word in irregular_infinitives:
        return irregular_infinitives[word]
    elif word.endswith("க்க"):            # கொடு, அழி, சிரி, உதை, சாய், சேர், வை (put), கா, நட, இரு, பற, இழ
        return word[:-len("க்க")]
    elif word.endswith(mei) and word[-1:] == word[-3:-2]:        # உண், செய், தின், செல், சொல், கொள்
        return word[:-1] 
    elif word.endswith("ட்க"):            # கேள், மீள்
        return word[:-len("ட்க")] + "ள்"                    
    elif word.endswith("ற்க"):            # தோல் (lose), நூல், வில் (sell), கல் (learn), ஏல் (accept)
        return word[:-len("ற்க")] + "ல்"
    elif word.endswith("ய"):             
        if word[-2:-1] in nedil_ah_ee:     # பாய் (jump), காய் (வெய்யிலில்), ஆராய், தேய்
            return word + "்"
        else:                              # அலை, அடை, பிழி, பிரி, அறி, நுழை, தெரி, அசை
            return word[:-1]
    elif word.endswith(u_ending_mei):      # வாங்கு, பேசு, விடு, தொடு, இடு, நடத்து, எழுப்பு, பெறு, உதவு, அள்ளு 
        return word + "ு"                
    elif word.endswith(pulli_ending_mei):  # சேர், பேர், வளர், அமர், உணர், வாழ், புகழ், கவிழ், ஆள், உருள், புரள், சுருள்
        return word + "்"                
    else:  
        is_affix_removed = False                                
        return word    

# Convert வினையெச்சம் (AvP - Adverbial Participle) form to the root verb
def convert_avp_to_the_root_verb(word):
    global is_affix_removed 
    is_affix_removed = True
    if word in irregular_avps:
        return irregular_avps[word]    
    elif word.endswith("த்து"):               # கொடு, அழி, சிரி, உதை, சாய், சேர், வை (put), கா
        return word[:-len("த்து")]
    elif word.endswith("ந்து"):               # நட, இரு, இழ, பற, துற, மற, விய
        return word[:-len("ந்து")]
    elif word.endswith("ட்டு"):               # விடு, படு (துன்பம்), சாப்பிடு, தொடு (touch), இடு 
        return word[:-len("ட்டு")] + "டு"
    elif word.endswith("ண்டு"):              # ஆள், உருள், புரள், சுருள், மருள், கொள் 
        return word[:-len("ண்டு")] + "ள்"
    elif word.endswith("ன்று"):               # நில், செல், மெல், வெல், கொல், பயில், முயல்
        return word[:-len("ன்று")] + "ல்"
    elif word.endswith("ற்று"):               # தோல் (lose), நூல், வில் (sell), கல் (learn), ஏல் (accept)
        return word[:-len("ற்று")] + "ல்"
    elif word.endswith("ி"):                 # வாங்கு, உதவு, ஆடு, ஓட்டு, கூறு, பேசு, ஆக்கு, நீக்கு, கவ்வு
        return word[:-len("ி")] + "ு"
    elif word.endswith("து"):                # செய், வை (திட்டு), அழு
        return word[:-2]     
    else:
        is_affix_removed = False
        return word                  

# Define the list of affix stripping functions
affix_stripping_functions = [
    remove_plural_suffix,
    remove_negative_suffixes,
    remove_level4_mei_mudhal_suffixes,
    remove_level3_mei_mudhal_suffixes,
    remove_level3_4_uyir_mudhal_suffixes,
    remove_past_tense_neen_PNG_suffixes,
    remove_past_tense_ndteen_PNG_suffix,
    remove_past_tense_Teen_PNG_suffixes,
    remove_past_tense_teen_PNG_suffixes,
    remove_past_tense_Reen_PNG_suffix,
    remove_present_tense_kiReen_PNG_suffixes,
    remove_future_tense_peen_PNG_suffixes,
    remove_future_tense_veen_PNG_suffixes,
    remove_future_tense_ahrinai_PNG_suffix,
    convert_infinitive_to_the_root_verb,
    convert_avp_to_the_root_verb
]
def verb_stemmer(word):
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
        word = verb_stemmer(word)      # Recursive call to stem the word iteratively
    return word

word = "போய்த்தொலையுங்கள்"  

# If the word has a match in the lexicon, we have the stem already. Nothing further needs to be done.
if data_store.is_word_in_lexicon(word):
    print(word)
else:
    # word = tamil_stemmer(word)
    word = verb_stemmer(word)