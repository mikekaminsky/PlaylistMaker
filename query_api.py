import json
import requests

stopwords = set(["a", "the", "in", "of", "or", "and", "but", "for", "at", "which", "on", "we", "i", "by", "if", "is", "was", "so", "nor", "into"])

class queryer(object):
  """
  Class to serve as a container for the API query box
  """
  def __init__(self):
    print "queryer object created"
    self.searches = {}

  def __updater(self, query, result):
    self.searches[query] = result
    return result

  def query_api(self, query, maxpage = 10):
    if query in stopwords:
      return self.__updater(query, "None")
    #Loop for paginagtion
    for i in range(0,maxpage):
      print i
      url = 'https://api.spotify.com/v1/search?'
      url = url + 'q=track:%22' + query.replace(" ","+") + '%22&type=track&limit=50&offset='+str(i*50)
      print url
      response = requests.get(url)
      if response.status_code != 200:
        print "Bad status code!" + response.status_code
        break
      options = response.json()['tracks']['items']
      # If we run out results, break
      if len(options) < 1:
        break
      print "Number of options:" + str(len(options))
      # See if any of the nams *actually* match
      for option in options:
        track_name = option['name']
        album_name = option['album']['name']
        artist_name = option['artists'][0]['name']
        spotify_url = option['external_urls']['spotify']
        assert 'track' in spotify_url
        if track_name.lower() == query:
          return self.__updater(query, spotify_url)
          break
    return self.__updater(query,"None")
