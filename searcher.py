import re

sentence = "tHis is, A. very long troubling senTence with a shitload of words"
#sentence = "tHis is, A. very long"

def clean_sentence(sentence):
  return re.sub('[^a-z ]', '', sentence.lower())

sentence_clean = clean_sentence(sentence)

sentence_split = sentence_clean.split()

def query_api(string):
  print "searching for " + string
  if string == "a very long":
    return "www.google.com"
  if string == "troubling sentence":
    return "www.google.com"
  if string == "a shitload of":
    return "www.google.com"
  if string == "this":
    return "www.google.com"
  else:
   return False

def search_sentence(remaining, clefts, results):
  #Base Case
  if clefts == 1 and len(remaining) == 1:
    wedge = ' '.join(remaining)
    result = query_api(wedge)
    if result:
      results.append((wedge, result))
    else:
      results.append((wedge, "No song :("))

  #Recursion
  elif clefts > 1 or len(remaining) > 1:
    if len(remaining)>clefts:
      found_flag = 0
      for cleft in range (0, len(remaining) - (clefts - 1)):
        wedge = ' '.join(remaining[cleft:cleft+clefts])
        result = query_api(wedge)
        if result:
          found_flag = 1
          remaining_left = remaining[0:cleft]
          remaining_right = remaining[cleft+clefts:]

          results.append((wedge, result))

          #Split the sentence along the wedge, and continue searching
          search_sentence(remaining_left, clefts-1, results)
          search_sentence(remaining_right, clefts, results)
          break
      if found_flag == 0 and clefts > 0:
        search_sentence(remaining, clefts - 1, results)
    if len(remaining)==clefts:
        wedge = ' '.join(remaining)
        result = query_api(wedge)
        if result:
          results.append((wedge, result))
        else:
          search_sentence(remaining, clefts-1, results)
    if len(remaining) < clefts:
      search_sentence(remaining, clefts-1, results)
  return results

starting_clefts = 3
results = list()
res = search_sentence(sentence_split, starting_clefts, results)

for tupes in res:
    print tupes[0] + ' URL: ' + tupes[1]





