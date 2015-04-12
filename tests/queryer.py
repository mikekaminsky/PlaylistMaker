execfile("queryer.py")


q = queryer()

def test_stopword():
    assert q.query_api("a") == "None"

def test_empty():
    assert q.query_api("") == "None"
