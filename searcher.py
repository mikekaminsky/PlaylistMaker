import re
from queryer import *

def clean_text(block):
  # Split on sentence-ending punctuation and carriage-returns
  splits = re.split(r'[!\(\).\?\;\:\n]',block)
  # Strip leading and trailing whitespace
  splits = [x.strip(' ') for x in splits]
  #Filter out empties
  splits = filter(None, splits)
  return splits

def clean_sentence(sentence):
  return re.sub('[^a-z ]', '', sentence.lower().strip(' ')).split()

def search_sentence(remaining, queryer, clefts = 10):

  def get_url(query = '', queryer = queryer):
    track = queryer.query_api(query)
    if track != "None":
      return track
    else:
      return False

  #Clefts must be less than or equal to number of remaining items
  clefts = min(clefts,len(remaining))

  #Base Case
  if clefts == 1:
    if len(remaining) == 1:
      wedge = ' '.join(remaining)
      result = get_url(wedge)
      if result:
        return [(wedge, result)]
      else:
        return [(wedge, "None")]

    if len(remaining) > 1: 
      output = []
      for cleft in range (0, len(remaining)):
        wedge = remaining[cleft]
        result = get_url(wedge)
        if result:
          output.append((wedge, result))
        else:
          output.append((wedge, "None"))
      return output

  #Recursion piece
  if clefts > 1 or len(remaining) > 1:
    if len(remaining)>clefts:
      found_flag = 0
      for cleft in range (0, len(remaining) - (clefts - 1)):
        wedge = ' '.join(remaining[cleft:cleft+clefts])
        result = get_url(wedge)
        if result:
          found_flag = 1

          #Split around the phrase that was found
          remaining_left = remaining[0:cleft]
          remaining_right = remaining[cleft+clefts:]

          middle = [(wedge, result)]
          #Decrement the cleft size for left search
          left = search_sentence(remaining_left, queryer, clefts-1)
          #Keep searching to the right
          right = search_sentence(remaining_right, queryer, clefts)

          if left and right:
            return left + middle + right
          if left:
            return left + middle
          if right:
            return middle + right

      # If you don't find anything, start back at the beginning with a smaller search size
      if found_flag == 0 and clefts > 1:
        return search_sentence(remaining, queryer, clefts - 1)

    if len(remaining)==clefts:
      wedge = ' '.join(remaining)
      result = get_url(wedge)
      if result:
        return [(wedge, result)]
      else:
        return search_sentence(remaining, queryer, clefts-1)
