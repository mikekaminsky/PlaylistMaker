execfile("searcher.py")

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
sentence = "  'Four sCore- and, seven  " 
sentence_split = clean_sentence(sentence)

def query_api(string):
  #print "searching" + string
  if string == "four score and seven":
    return "url1"
  if string == "four":
    return "url2"
  if string == "and seven":
    return "url3"
  else:
   return False

def test_clean_sentence():
    print(sentence)
    assert clean_sentence(sentence) == ["four", "score", "and", "seven"]

def test_search_sentence_1():
    results = search_sentence(sentence_split, 1)
    assert results == [("four","url2"),("score","None"),("and","None"),("seven","None")]

def test_search_sentence_2():
    results = search_sentence(sentence_split, 2)
    print(results)
    assert results == [("four","url2"),("score","None"),("and seven","url3")]

def test_search_sentence_3():
    results = search_sentence(sentence_split, 3)
    print(results)
    assert results == [("four","url2"),("score","None"),("and seven","url3")]

def test_search_sentence_4():
    results = search_sentence(sentence_split, 4)
    print(results)
    assert results == [("four score and seven","url1")]

def test_search_sentence_5():
    results = search_sentence(sentence_split, 5)
    print(results)
    assert results == [("four score and seven","url1")]

def test_search_sentence_100():
    results = search_sentence(sentence_split, 100)
    print(results)
    assert results == [("four score and seven","url1")]

def test_search_sentence_nomatch():
    results = search_sentence(["these", "are"], 3)
    print(results)
    assert results == [("these","None"), ("are","None")]

def test_clean_text():
    assert clean_text(block) == ['Half a league, half a league,', 'Half a league onward,', 'All in the valley of Death', 'Rode the six hundred', '"Forward, the Light Brigade', 'Charge for the guns', '" he said', 'Into the valley of Death', 'Rode the six hundred']
