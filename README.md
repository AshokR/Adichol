# Adichol
Rule based Tamil Adichol extractor
This is an attempt at creating the first part of a rule based Tamil stemmer - it only handles nouns and verbs for now. I am using the following resources and thank them for the same:
 - Python 3.12
 - The list of Tamil nouns, unique_sorted_noun_master.txt, from [Kaniyam Foundation](https://github.com/KaniyamFoundation/all_tamil_nouns).
 - Bloom filter to check whether a given word is in the list of lexicon words: [pybloom_live](https://github.com/joseph-fox/python-bloomfilter).
 - The Flowchart of Tamil Noun and Verb Forms is from [AU-KBC கணக்கீட்டு மொழியியல் ஆராய்ச்சி குழு](https://www.au-kbc.org/nlp/).
 - The list of Tamil verbs is extracted from the crea.babylon file shared by [stardict-tamil site](https://github.com/indic-dict/stardict-tamil).

## அடிச்சொல் ஏன்?
நாம் ஒரு சொல்லைப் பற்றித் தேடும்போது, தேடல் பெட்டியில் உள்ளிட்டது மட்டுமல்லாமல் அதன் பிற சாத்தியமான வடிவங்களுக்கும் பொருத்தமான முடிவுகளைக் கண்டுபிடிக்கத்தான் விரும்புகிறோம். எடுத்துக்காட்டாக “மின்னூல்” என்று தேடல் பெட்டியில் உள்ளிடுகிறோம் என்று வைத்துக் கொள்வோம். நமக்கு ‘மின்னூல்கள்’, ‘மின்னூலை’, ‘மின்னூலின்’ என்ற சொற்கள் இருக்கும் பக்கங்களும் தேவைதானே? இதைச் செயல்படுத்த நாம் வேறுபாடுகளை நீக்கி சொற்களை அவற்றின் அடிப்படை வடிவத்திற்குக் குறைக்க வேண்டும். 

## Stemmer (தண்டுச்சொல் பிரிப்பி) vs Lemmatizer (அடிச்சொல் பிரிப்பி)
Stemming and lemmatization are both techniques used in Natural Language Processing (NLP) to reduce words to their base form, but they differ in their approach and output. Stemming is a faster method that simply removes suffixes from words, potentially resulting in non-dictionary words. For example, the Porter stemmer reduces both "apple" and "apples" to the stem "appl". Lemmatization, on the other hand, considers the context and the part of speech of a word to produce a meaningful dictionary word, or lemma. Here, what we are attemting to do, is closer to a Lemmatizer than a Stemmer: 
 - We are writing rules that are specific to the part of speech of the word.
 - We are using a lexicon to match with and output a valid dictionary word.
 - However, the limitation in our approach is that we are not considering the context in which the word has been used. 
