from queryer import *
from searcher import *

def playlistmaker(
        textforplaylist,
        requireuniquesongs = True,
        maxwordsearchlength = 10,
        maxpagesearch = 10
        ):

  if textforplaylist is None:
    print "You must provide text to search!"
    raise

  q = queryer(
      uniquesongs = requireuniquesongs,
      maxpage = maxpagesearch)

  result_sentences = []

  for sentence in clean_text(textforplaylist):
      result = search_sentence(clean_sentence(sentence), q, maxwordsearchlength)
      result_sentences.append(result)

  results = []

  for sentence in result_sentences:
    for word in sentence:
      results.append(word)

  return results
