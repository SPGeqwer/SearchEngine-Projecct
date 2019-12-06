from invertedfile import readfile
import string, linecache


listPath = "./occurrenceList.dat"

if __name__ == '__main__':
    tire = readfile()   ##  LOAD THE TRIE INTO MEMORY

    ##  SIMPLE UI
    print("#################################################")
    print("##                 SEARCH ENGINE               ##")
    print("##              (INPUT -q TO QUIT!)            ##")
    print("## (YOU COULD INPUT MULTIPLE WORDS TO SEARCH!) ##")
    print("#################################################\n")
    
    ##  SEARCHING LOOP
    while(True):
        input_String = input("\nSEARCH:  ")
        input_String = input_String.strip()
        
        if input_String.lower() == "-q":
            print("SEE YOU!!!")
            break

        ##  COLLECT MULTIPLE KEYS
        input_String = "".join((ch for ch in input_String if ch not in set(string.punctuation)))    ##  REMOVE PUNCTUATION
        inputKey = input_String.lower().split()     ##  SPLIT KEYS
        inputKey = list(set(inputKey))              ##  REMOVE REPEAT KEYS
        if inputKey == []:
            print("You input is empty!")
            continue
        
        key_occurrence_list = []  ## MAINTAIN OCCURRENCE LIST
        
        ##  SEARCH SEARCH KEY IN INVERSED FILE ######
        for key in inputKey:
            value = tire.getValue(key)

            ##  THE INPUT STRING IS NOT IN THE TRIE AND NOT PREFIX OF ANY OTHER KEY
            if value == None: 
                continue
            ##  THE INPUT STRING IS PREFIX OF CERTAIN KEYS IN THE TRIE
            elif value == -1:
                ##  COLLECT THE WORDS THAT CONTAIN THE INPUT KEY
                keys = tire.dfs(tire.getNode(key))
                ##  CONVERT TO COMPLETE WORDS LIST
                result =[]
                for word in keys:
                    s = key + word
                    result.append(s)
                ##  FIND THE MOST POSSIBLE WORDS BY COMPARING FREQUENCY
                max_freq = 0
                max_freq_word = ""
                max_freq_word_value = 0
                for word in result:
                    word_value = tire.getValue(word)
                    line = linecache.getline(listPath, word_value + 1)
                    l = line.split("||")
                    if int(l[1]) > int(max_freq):
                        max_freq = l[1]
                        max_freq_word = word
                        max_freq_word_value = word_value
                print("DO YOU MEAN: ",max_freq_word,"?")
                
                line = linecache.getline(listPath, max_freq_word_value + 1)
                l = line.split("||")
                l.pop(0)                
                l.pop(0)
                new_list = []     ##  [(freq,link)]
                while l[0] != "\n":
                    pageInfo = (l.pop(0),l.pop(0))
                    new_list.append(pageInfo)
                key_occurrence_list.append(new_list)

            else: ## The key is in trie
                line = linecache.getline(listPath, value + 1)
                l = line.split("||")
                l.pop(0)                
                l.pop(0)
                new_list = []
                while l[0] != "\n":
                    pageInfo = (l.pop(0),l.pop(0))
                    new_list.append(pageInfo)
                key_occurrence_list.append(new_list)
        ##  OUTPUT THE LIST
        if key_occurrence_list == []:
            print("NOTHING FOUND!")
            continue
        
        resultList = []
        for occurrence_list in key_occurrence_list:
            resultList += occurrence_list
        resultList.sort(key = lambda x:int(x[0]), reverse = True)
        
        print("RESULT: ")
        for i in resultList:
            print(i[1])