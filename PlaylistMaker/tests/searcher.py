# -*- coding: utf-8 -*-
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


class testqueryer(object):
  def __init__(self):
    print "queryer object created"
    self.searches = {}

  def query_api(self, string, maxpage = 10):
    if string == "four score and seven":
      return "url1"
    if string == "four":
      return "url2"
    if string == "and seven":
      return "url3"
    else:
     return False

q = testqueryer()


def test_clean_sentence_strip():
    print(sentence)
    assert clean_sentence(sentence) == ["four", "score", "and", "seven"]

def test_clean_sentence_utf8():
    print(sentence)
    assert clean_sentence('Du får göra som du vill') == ['du', 'får', 'göra', 'som', 'du', 'vill']

def test_search_sentence_1():
    results = search_sentence(sentence_split, q, 1)
    assert results == [("four","url2"),("score","None"),("and","None"),("seven","None")]

def test_search_sentence_2():
    results = search_sentence(sentence_split, q, 2)
    print(results)
    assert results == [("four","url2"),("score","None"),("and seven","url3")]

def test_search_sentence_3():
    results = search_sentence(sentence_split, q, 3)
    print(results)
    assert results == [("four","url2"),("score","None"),("and seven","url3")]

def test_search_sentence_4():
    results = search_sentence(sentence_split, q, 4)
    print(results)
    assert results == [("four score and seven","url1")]

def test_search_sentence_5():
    results = search_sentence(sentence_split, q, 5)
    print(results)
    assert results == [("four score and seven","url1")]

def test_search_sentence_100():
    results = search_sentence(sentence_split, q, 100)
    print(results)
    assert results == [("four score and seven","url1")]

def test_search_sentence_nomatch():
    results = search_sentence(["these", "are"], q, 3)
    print(results)
    assert results == [("these","None"), ("are","None")]

def test_clean_text():
    assert clean_text(block) == ['Half a league, half a league,', 'Half a league onward,', 'All in the valley of Death', 'Rode the six hundred', '"Forward, the Light Brigade', 'Charge for the guns', '" he said', 'Into the valley of Death', 'Rode the six hundred']
