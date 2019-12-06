# Search Engine

Implement the simplified Search Engine described in Section 23.5.4 for the pages of a small Web site. Use all the words in the pages of the site as index terms, excluding stop words such as articles, prepositions, and pronouns.

## Description

WE use requests to read all web pages from input to our data structure: inverted file. Then use bs4 and nltk to parser the content. Foe the ivertedfile, we keep the trie in the memory and save the occurrence list in the disk(occurrenceList.dat). When users input some words, the engine will rank the related pages by comparing the frequency of the keys. As the result, the user can get a sorted list of links about the input keys words.

## Prerequisites

* Python3
* VS Code
* bs4
* requests
* nltk

## Running the search engine

```bash
python3 search.py
```

## reference

* [beautifulsoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
* [nltk](https://www.nltk.org/)
* [ROME](https://docs.python.org/3.7/library/linecache.html#module-linecache)
