from searcher import *
from queryer import *



block = """
Half a league, half a league,
Half a league onward,
All in the valley of Death
Rode the six hundred.
"Forward, the Light Brigade!
Charge for the guns!" he said:
Into the valley of Death
Rode the six hundred.
"""

q = queryer(uniquesongs = True)
results = []
for sentence in clean_text(block):
    result = search_sentence(clean_sentence(sentence), q, 10)
    results.append(result)

for result in results:
    for word in result:
        print word

#cleaned = clean_text(block)
#test = clean_sentence(cleaned[0])
#res = search_sentence(test, q, 10)
