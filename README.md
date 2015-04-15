# PlaylistMaker
Inspired by the [Spotify Poetry tumblr](http://spotifypoetry.tumblr.com/), this tool takes a block of text as input and returns a list of songs in ordered tuples `(title, url)` where the title of the song matches the text of the input and the url is a link to the spotify track with that title.

##Installation instructions

    $ git clone https://github.com/mikekaminsky/PlaylistMaker
    $ cd PlaylistMaker
    $ python setup.py install

If you get an insecure platform warning

    InsecurePlatformWarning: A true SSLContext object is not available. This prevents urllib3 from configuring SSL appropriately and may cause certain SSL connections to fail.

You may need to install pyopenssl:

    pip install pyopenssl ndg-httpsclient pyasn1

##Examples

From the command line:

    $ PlaylistMaker "The rain falls heavy on the plains in spain"

From Python:

    $ Python
    >>> from PlaylistMaker import playlistmaker as pm
    >>> text = """
    Because I could not stop for Death,
    He kindly stopped for me;
    The carriage held but just ourselves
    And Immortality.
    """
    print pm.playlistmaker(
                    textforplaylist = text, 
                    requireuniquesongs = True,
                    maxwordsearchlength = 10,
                    maxpagesearch = 20
                    )
    
Arguments:

  * `textforplaylist`: String. The block of text you want to search for.
  * `requireuniquesongs`: Boolean. Default: `True`. Requires that songs are not repeated.
  * `maxwordsearchlength`: Integer. Default: `10`. The maximum number of consecutive words that will be searched in the recursive algorithm. Lower numbers will return results faster, but no longer guarantee the globally optimal solution.
  * `maxpagesearch`: Integer. Default: `10`. The number of 50-result pages to search through using the Spotify API. This is the slowest part of the search, so setting this value to a lower number guarantees a result much faster, but you might miss a valid result you searched for depending on the order the API's results are returned.

##Discussion

###The Search Algorithm

In order to be able to work efficiently with any block of text, this algorithm first splits text chunks up into 'sentences' using the following characters as delimiters:

  * `!`
  * `.`
  * `?`
  * `(` or `)`
  * `;`
  * `:`
  * `\n`  (carriage returns) 
  
Once the block of text is split into sentences, the text is lowercased and stripped of punctuation and leading and trailing whitespace. UTF-8 Characters are allowed. Note: this is a feature to avoid having song titles that split across 'thoughts' in a sentence/poem. Removing this feature would be trivial, although it would result in longer search times.

The search algorithm to find a match is performed at the sentence level for comprehension reasons. This way the titles of the songs that are found don't split across different 'thoughts'.

Imagine the following block of text:

> Do I contradict myself?

> Very well then I contradict myself,

> (I am large, I contain multitudes.)

which is then parsed into the following sentence-lists:

1. `["do", "i", "contradict", "myself"]`
2. `["very", "well", "then", "i", "contradict", "myself"]`
3. `["i", "am", "large", "i", "contain", "multitudes"]`

Focusing on the first sentence only, we'll walk through what the algorithm is doing. The same algorithm is then applied to sentences 2 and 3 in turn. The search algortihm starts by searching for a group of words equal to the sentence length: 

    "do i contradict myself"

If no result is found, then the algorithm tries using groups of words one shorter:

    "do i contradict"
    "i contradict myself"

And again, if no result is found, the search is repeated:

    "do i"
    "i contradict"
    "contradict myself"

Now, what if we find a song called 'I Contradict'? Here, the algorithm splits the sentence along the search term that was found:

>  left: `["do", "i"]`

>  found: `i contradict`

>  right: `["myself"]`

The algorithm then recursively repeats the search on the left (decrementing the number of words in a single search) and the right (without decrementing).

In the worst-case scenario (no matches >1 word), the algorithm will complete with n(n+1)/2 searches where n is the number of words in the sentence:

1. `do i contradict myself`
2. `do i contradict`
3. `i contradict myself`
4. `do i`
5. `i contradict`
6. `contradict myself`
7. `do`
8. `i`
9. `contradict`
10. `myself`

####Sub-Optimality

Because this algorithm is greedy, there are some cases in which this algorithm will **not** find the globally optimal solution. For example, if we have the sentence:

> Roses are red violets are blue

and our database contains the following song titles:
* roses are red violets 
* red violets are blue
* roses are

The optimal solution is "roses are" + "red violets are blue". However, this algorithm will identify _only_ the song title "roses are red violets". An algorithm that could solve this problem might search for all two-song combinations then all three-song combinations, then all 4-song combinations, stopping as soon as it finds a combination that is valid.

###The API Query

Because the Spotify API search feature does not allow you to specify an exact title match, the following list of stopwords are not searched if they are alone:

    stopwords = set(["a", "the", "in", "of", "or", "and", "but", "for", "at", "which", "on", "we", "i", "by", "if", "is", "was", "so", "nor", "into"])

The querying algorithm keeps track of every succesful search within a given block of text. If you do not require that the results contain unique songs, the algorithm will not query the API for the same search that's already been completed. In the case where you do require unique songs, the algorithm will page through search results until it finds an exact match that hasn't already been returned for that query.

This logic/implementation could easily be extended to caching for a webapp, or even saving frequent ngrams with their results for efficiency.

##To-Do:
* [x] Write tests
* [x] Refactor
* [x] Hook into real API
* [x] Convert the query_api function into an object so we can have an 'already_queried' list
* [x] Don't repeat searches where "None" was found!!!
* [x] Pass argument to either:
  * [x] Maximize song diversity (i.e., try not to repeat songs)
  * [x] Maximize efficiency (i.e., use the results of previous queries)
* [x] Wrap for CLT
* [x] Improve test coverage
* [x] Handle non-latin characters?
* [x] Return properly capitalized track titles?
