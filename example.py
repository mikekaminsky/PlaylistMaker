from searcher import *
from query_api import *



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

results = []
for sentence in clean_text(block):
    result = search_sentence(clean_sentence(sentence))
    results.append(result)

for result in results:
    for word in result:
        print word

#cleaned = clean_text(block)
#test = clean_sentence(cleaned[3])
#res = search_sentence(test, 10, get_url)
