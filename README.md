# PlaylistMaker

###To-Do:
* [x] Write tests
* [x] Refactor
* [ ] Hook into real API

##Installation instructions

##Example

##Discussion
Inspired by the [Spotify Poetry tumblr](http://spotifypoetry.tumblr.com/), this tool takes a block of text as input and returns a list of songs in ordered tuples `(title, url)` where the title of the song matches the text of the input and the url is a link to the spotify track with that title.

In order to be able to work efficiently with any block of text, this algorithm first splits text chunks up into 'sentences' using the following characters as delimiters:

  * `!`
  * `.`
  * `?`
  * `(` or `)`
  * `;`
  * `:`
  * `\n` (carriage returns) ` `
  

Once the block of text is split into sentences, the text is lowercased and stripped of non-characters (including numerals!) and leading and trailing whitespace.

The search algorithm to find a match is performed at the sentence level for comprehension reasons. This way the titles of the songs that are found don't split across different 'thoughts'.

Imagine the following block of text:

> Do I contradict myself?

> Very well then I contradict myself,

> (I am large, I contain multitudes.)

which is then parsed into the following sentence-lists:

1. ["do", "i", "contradict", "myself"]
2. ["very", "well", "then", "i", "contradict", "myself"]
3. ["i", "am", "large", "i", "contain", "multitudes"]

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

>  right: `["mysyelf"]`

The algorithm then _recursively_ repeats the search on the left (decrementing the search group length) and the right (without decrementing).

In the worst-case scenario (no matches >1 word), the algorithm will complete with n(n+1)/2 searches where n is the number of words in the sentence:

1. "do i contradict myself"
2. "do i contradict"
3. "i contradict myself"
4. "do i"
5. "i contradict"
6. "contradict myself"
7. "do"
8. "i"
9. "contradict"
10. "myself"

I _think_ this might be an optimal algorithm. Notice how it handles the following sentence

    ["two", "roads", "diverged", "in", "a", "yellow", "wood"]

where only the following song titles are in our database:

1. two roads
2. roads diverged
3. in a 
4. yellow wood

The algorithm matches
    `["two roads", "in a", "yellow wood"]`
