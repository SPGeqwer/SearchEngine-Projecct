import requests, nltk, string
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
nltk.download('punkt')
nltk.download('stopwords')
from inputs import links

## BUILD TRIE
class Node:
    def __init__(self):
        self.key = None
        self.value = None
        self.is_word = False
        self.children = {}        
class Trie:
    def __init__(self):
        self.root = Node()

    ## Insert
    def insert(self, word, value=None):
        currentNode = self.root
        for char in word:
            if char not in currentNode.children:
                currentNode.children[char] = Node()
            currentNode = currentNode.children[char]
            currentNode.key = char
        currentNode.value = value
        currentNode.is_word = True

    ## CHECK IF THE WORD IN THE TRIE OR NOT
    def inTrie(self,word): 
        currentNode = self.root
        for char in word:
            if char in currentNode.children:
                currentNode = currentNode.children[char]
            else:
                return False
        if currentNode.is_word:
            return True
        else:
            return False

    ## RETURN THE VALUE OF A WORD. IF THE WORD IS TOTALLY NOT IN TRIE, RETURN NONE. IF THE WORD IS PARTLY IN TRIE, RETURN FLASE. 
    def getValue(self, word):
        currentNode = self.root
        for char in word:
            if char in currentNode.children:
                currentNode = currentNode.children[char]
            else:
                return None
        if currentNode.is_word:
            return currentNode.value
        else:
            return -1
  
    ## RETURN A NODE BY THE GIVEN WORD
    def getNode(self, word):
        currentNode = self.root
        for char in word:
            if char in currentNode.children:
                currentNode = currentNode.children[char]
            else:
                return None
        return currentNode

    ## USE DFS TO GET THE LIST WHICH CONTAIN ALL WORD IN TRIE WHICH ROOT IS GIVEN
    def dfs(self, node): 
        keyList = []
        if node.children:
            for char in node.children:
                subList = self.dfs(node.children[char])
                if len(subList) == 0:
                    keyList.append(char)
                elif node.children[char].is_word:
                    for word in subList:
                        keyList.append(char + word)
                    keyList.append(char)
                else:
                    for word in subList:
                        s = char + word
                        keyList.append(s)
        else:
            return []
        return keyList

## BUILD INVERTEDFILE
class invertedFile():
    def __init__(self):
        self.trie = Trie()
        self.occurrenceList = []
        self.listLength = 0

    ## PUT ELEMENT INTO INVERTEDFILE
    def put(self,key,freq,link):
        ## EXIST KEY
        if self.trie.inTrie(key):
            index = self.trie.getValue(key)
            self.occurrenceList[index][1] += freq
            self.occurrenceList[index][2].append((freq,link))
            self.occurrenceList[index][2].sort(key = lambda x:x[0], reverse = True) ## SORT FOR RANKING
        ## NEW KEY
        else: 
            self.trie.insert(key,self.listLength)
            self.occurrenceList.append([key,freq,[(freq,link)]])
            self.listLength += 1
    
    ## SAVE THE WHOLE OCCURRENCE LIST
    def save(self,fileName = "occurrenceList.dat"):
        f = open(fileName,'w',encoding='utf-8')
        for [key,freq,occurrenceList] in self.occurrenceList:
            f.write(key+"||"+str(freq)+"||")
            for (freqInPage,link) in occurrenceList:
                f.write(str(freqInPage)+"||"+link+"||")
            f.write("\n")
        f.close()

def readfile():
    inverted_File = invertedFile()
    
    LEN_SHORT_WORD = 2                                  ####### THIS USED TO FILTER THE WORD SMALLER THAN THIS LENGTH.  
    stopWords = stopwords.words('english')              ####### CREAT THE STOP WORD LIST.
    remo = string.punctuation + string.digits + "¶"     
    tab = str.maketrans(remo," " * len(remo))           ####### REPLACE PUNCTUATIONS AND DIGITS TO SPACE
    
    ####### READ WEB PAGES AND FILTERATE TEXT#######
    for link in links:              
        req = requests.get(link)
        soup = BeautifulSoup(req.text,'html5lib')
        
        text = soup.get_text(strip=True)
        text = text.translate(tab)
        text = word_tokenize(text)      ## SPLIT TEXT
        text = [word.lower() for word in text if word.lower() not in stopWords and len(word)>LEN_SHORT_WORD] ## CONVERT TO LOWER CASE, REMOVE STOP WORDS/SHORT WORDS
        
        dist = nltk.FreqDist(text)      ## USE FreqDist TO GET FREQUENCY OF KEYS get the freqency of all key that used to rank the sort result.
        
        for key,freq in dist.items():   ## PUT IT INTO THE INVERTED FILE
            inverted_File.put(key,freq,link)

    inverted_File.save()    ####### SAVE THE OCCURRENCE LIST
    return inverted_File.trie