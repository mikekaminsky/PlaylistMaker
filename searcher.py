import re

sentence = "tHis is, A. very long troubling senTence with a shitload of words"
#sentence = "tHis is, A. very long test"
#sentence = "tHis is"

def clean_sentence(sentence):
  return re.sub('[^a-z ]', '', sentence.lower())

sentence_clean = clean_sentence(sentence)

sentence_split = sentence_clean.split()

def query_api(string):
  print "searching " + string
  if string == "a very long":
    return "www.google.com"
  if string == "troubling sentence":
    return "www.rhymeremix.com"
  if string == "a shitload of":
    return "www.example.com"
  if string == "this":
    return "www.yahoo.com"
  if string == "is":
    return "www.myspace.com"
  else:
   return False


def search_sentence(remaining, clefts):

  if len(remaining) == 0 or clefts == 0:
    return []

  #Base Case
  if clefts == 1 and len(remaining) == 1:
    wedge = ' '.join(remaining)
    result = query_api(wedge)
    if result:
      return list((wedge, result))
    else:
      return list((wedge, "No song :("))

  if clefts == 1 and len(remaining) > 1: 
    output = []
    for cleft in range (0, len(remaining)):
      wedge = remaining[cleft]
      result = query_api(wedge)
      if result:
        output.append((wedge, result))
      else:
        output.append((wedge, "No song :("))
    return output

  #Recursion piece
  if clefts > 1 or len(remaining) > 1:
    if len(remaining)>clefts:
      found_flag = 0
      for cleft in range (0, len(remaining) - (clefts - 1)):
        wedge = ' '.join(remaining[cleft:cleft+clefts])
        result = query_api(wedge)
        if result:
          found_flag = 1
          remaining_left = remaining[0:cleft]
          remaining_right = remaining[cleft+clefts:]

          middle = list((wedge, result))
          left = search_sentence(remaining_left, clefts-1)
          right = search_sentence(remaining_right, clefts)

          if left and right:
            return left + middle + right
          if left:
            return left + middle
          if right:
            return middle + right

          #After we search again, we have to break out of the loop
          break

      # If you don't find anything, start back at the beginning with a smaller search size
      if found_flag == 0 and clefts > 0: 
        return search_sentence(remaining, clefts - 1)

    if len(remaining)==clefts:
      wedge = ' '.join(remaining)
      result = query_api(wedge)
      if result:
        return list((wedge, result))
      else:
        return search_sentence(remaining, clefts-1)
    if len(remaining) < clefts:
      return search_sentence(remaining, clefts-1)

starting_clefts = 5
res = search_sentence(sentence_split, starting_clefts)
