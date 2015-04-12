execfile("query_api.py")

def test_stopword():
    assert query_api("a") == "None"

def test_empty():
    assert query_api("") == "None"
