import json
import requests
from sets import Set

stopwords = set(["a", "the", "in", "of", "or", "and", "but", "for", "at", "which", "on", "we", "i", "by", "if", "is", "was", "so", "nor", "into"])

class queryer(object):
  """
  Class to serve as a container for the API query box
  """
  def __init__(self, uniquesongs = False):
    print "queryer object created"
    self.searches = {}
    self.uniquesongs = uniquesongs

  def __updater(self, query, result):
    if self.uniquesongs == True:
      if query in self.searches:
        oldresult = self.searches[query]
        oldresult.update(result)
        self.searches[query] = oldresult
      else:
        self.searches[query] = Set([result])
    else:
      self.searches[query] = result

    return result

  def query_api(self, query, maxpage = 10):

    old_results = []

    if query in stopwords:
      return self.__updater(query, "None")

    if query in self.searches and self.uniquesongs == False:
        return self.__updater(query, self.searches[query])

    #Loop for paginagtion
    for i in range(0, maxpage):
      url = 'https://api.spotify.com/v1/search?'
      url = url + 'q=track:%22' + query.replace(" ","+") + '%22&type=track&limit=50&offset='+str(i*50)
      response = requests.get(url)
      if response.status_code != 200:
        print "Bad status code!" + response.status_code
        break
      options = response.json()['tracks']['items']
      # If we run out results, break
      if len(options) < 1:
        break
      # See if any of the nams *actually* match
      for option in options:
        track_name = option['name']
        album_name = option['album']['name']
        artist_name = option['artists'][0]['name']
        spotify_url = option['external_urls']['spotify']
        assert 'track' in spotify_url
        if track_name.lower() == query:
          if self.uniquesongs == True:
            if query in self.searches:
              if spotify_url not in self.searches[query]:
                return self.__updater(query, spotify_url)
                break
            else:
                return self.__updater(query, spotify_url)
                break
          if self.uniquesongs == False:
            return self.__updater(query, spotify_url)
            break
    return self.__updater(query,"None")

















