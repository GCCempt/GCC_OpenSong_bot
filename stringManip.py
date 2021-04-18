#!/usr/bin/python
# -*- coding: utf-8 -*-

#  Feature Request - function to split a string into a list where:
#  - each element in the list is a max of 110 characters
# - element in the list must fall  on a word boundary (cannot split "words")
# - if the 110 character boundary falls on a "space" or punctuation like comma, semi-colon, period, exclamation mark), that is accepted
# -     else, back up to the nearest preceding space or punctuation mark
#-- 1st pass, break on "." | 2nd pass, break on ";" | 3rd pass, break on "," | 4th pass, break on max_character_length
# Function input: (string, max_character_length_per_line)
# Function return: (List of one or more lines)
import sys

TEST_STRING = \
    'Almighty and merciful God, we have erred and strayed from Your ways like lost sheep. We have followed too much the devices and desires of our own hearts. We have offended against Your holy laws. We have left undone those things which we ought to have done; and we have done those things which we ought not to have done. O Lord, have mercy upon us. Spare those who confess their faults. Restore those who are penitent, according to Your promises declared to the world in Christ Jesus, our Lord. And grant, O merciful God, for his sake, that we may live a holy, just, and humble life to the glory of Your holy name. Amen. '
TEST_STRING2 = \
    'And grant O merciful God for his sake that we may live a holy just and humble life to the glory of Your holy name. Amen.'
TEST_STRING3 = \
    '54“Death is swallowed up in victory.” 55“O death, where is your victory? O death, where is your sting?” 56The sting of death is sin, and the power of sin is the law. 57But thanks be to God, who gives us the victory through our Lord Jesus Christ.'

MAX_CHARACTER_LENGTH_PER_LINE = 130
WORD_FUDGE_LENGTH = 30
MAX_CHARACTER_LENGTH_PER_SPLIT_LINE = (MAX_CHARACTER_LENGTH_PER_LINE / 2) + WORD_FUDGE_LENGTH     #--- for lines without any punctuation which must be split

def stringSplit(string, max_character_length_per_line):
    stringList = []

    # Split the String into words using spaces

    textList = string.split()       #--- split string into a list where each word is a list item

    # keep count of current number of characters in the string and initilize stringVar

    currentCount = 0
    newString = ''
    for currentWord in textList:

        # # Check to see if the next word will overflow, including the space we add for formatting.

        if currentCount < MAX_CHARACTER_LENGTH_PER_LINE \
            and currentCount + len(currentWord + ' ') \
            <= MAX_CHARACTER_LENGTH_PER_LINE:
            newString = newString + ' ' + currentWord
            currentCount = len(newString)
        else:

        # The next word will overflow, so add it to the list and reset the count and newString variable.

            stringList.append(newString)
            currentCount = 0
            newString = ''

    # Add the remainder of the text leftover since there isn't any more overflow.

    stringList.append(newString)
    return stringList

    #--- end stringSplit function

#--- define wordSplit function
def wordSplit(string):
    import re

    wordList = []
    #wordList = re.split('\W+', string)
    wordList = re.split('(\W+)', string)
    return(wordList)
#--- end wordSplit function

#--- define sentenceSplit function
def sentenceSplit(string):          #--- input to the function is a string
    import re
    #print('\nStarting stringManip.sentenceSplit')
    sentenceList = []
    sentenceSplit =[]
    finalList = []      #--- to  hold the final list of sentences

    string = string.replace('\n', ' ')          #--- replace newline characters with spaces
    stringDelim = '\.'     
    sentenceList = re.split(stringDelim, string)         #--- 1st pass, break sentences by '.'

    #print('\nAfter split by "." ')
    #for sentence in sentenceList:
    #    print(sentence)

    sentenceCount = 0
    for i in range (0, len(sentenceList) - 1):
        sentence = sentenceList[i] + '.'         #--- add the periods at the end of the sentence
        sentence = sentence.strip()    #--- strip leading and trailing spaces on each sentence
        #print('\nLength of sentence =', len(sentence), 'sentence =', sentence)

        if len(sentence) >= MAX_CHARACTER_LENGTH_PER_LINE and ';' in sentence:       #--- long sentence which can be split by ';'
            stringDelim = '\;'      
            sentenceSplit = re.split(stringDelim, sentence)     #--- 2nd pass, break sentences by ';'
            if len(sentenceSplit) > 0:       #-- verify there was a break on ';'
                for j in range(0, len(sentenceSplit)):
                    sentence = sentenceSplit[j]       
                    if j < len(sentenceSplit) - 1:
                        sentence = sentence + ';'    #--- add back the ';' a the end of the line
                    finalList.append(sentence)
        elif len(sentence) >= MAX_CHARACTER_LENGTH_PER_LINE and ',' in sentence: #--- long sentence which can be split by ','
            #print('\nLength of sentence =', len(sentence), 'long sentence found=', sentence)
            stringDelim = ', '
            sentenceSplit = sentence.split(stringDelim)     #--- 3rd pass, break sentences by ','              
            sentence = ''
            for phrase in sentenceSplit:
                print('\nphrase=', phrase)
                if len(sentence) + len(phrase) >  MAX_CHARACTER_LENGTH_PER_LINE:
                    finalList.append(sentence)
                    sentence = phrase + ', '
                else:
                    sentence = sentence + phrase + ', '
                    #print('\nsentence=', sentence)
            sentence = sentence.replace('.,', '.')      #--- strip extraneous "," at the end of a sentence
            finalList.append(sentence)
        elif len(sentence) >= MAX_CHARACTER_LENGTH_PER_LINE:       #--- long sentence which will be split by max length
            #print('\nlong sentence found=', sentence)
            sentenceSplit = sentence.split()       #--- split string into a list where each word is a list item
            sentence = ''
            for word in sentenceSplit:
                #print('\nword=', word)
                if len(sentence) + len(word) > MAX_CHARACTER_LENGTH_PER_SPLIT_LINE:  #-- check if the next word would exceed the permitted length
                    finalList.append(sentence)
                    sentence = word + ' '
                else:
                    sentence = sentence + word + ' '
                    #print('\nsentence=', sentence)
            finalList.append(sentence)
        else:
            finalList.append(sentence)
        
        sentenceCount +=1

    #--- print the results
    for sentence in finalList:
        print('\nFinal lenth of sentence=', len(sentence), ' sentence=', sentence)

    return(finalList)
#--- end sentenceSplit function

#--- define paragraph sentenceSplit function
def old_paragraphSplit(string):
    import re
    #print('\nStarting stringManip.sentenceSplit')
    sentenceList = []
    secondList = []
    sentenceSplit =[]
    finalList = []      #--- to  hold the final list of sentences
    string = string.replace('\n', ' ')          #--- replace newline characters with spaces
    stringDelim = '\.'     
    sentenceList = re.split(stringDelim, string)         #--- 1st pass, break sentences by '.'

    #print('\nAfter split by "." ')
    #for sentence in sentenceList:
    #    print(sentence)
    #sys.exit(0)

    sentenceCount = 0
    for i in range (0, len(sentenceList) - 1):
        sentence = sentenceList[i] + '.'         #--- add the periods at the end of the sentence
        sentence = sentence.strip()    #--- strip leading and trailing spaces on each sentence
        #print('\nLength of sentence =', len(sentence), 'sentence =', sentence)

        if len(sentence) >= MAX_CHARACTER_LENGTH_PER_LINE and ';' in sentence:       #--- long sentence which can be split by ';'
            stringDelim = '\;'      
            sentenceSplit = re.split(stringDelim, sentence)     #--- 2nd pass, break sentences by ';'
            if len(sentenceSplit) > 0:       #-- verify there was a break on ';'
                for j in range(0, len(sentenceSplit)):
                    sentence = sentenceSplit[j]       
                    if j < len(sentenceSplit) - 1:
                        sentence = sentence + ';'    #--- add back the ';' a the end of the line
                    secondList.append(sentence)
        else:
            secondList.append(sentence)      #--- automatically include short sentence.

  
    commaList = commaSplit(secondList)         #--- check if sentences need further processing
    print('\nAfter split by "," \n')
    for sentence in commaList:
        print(sentence)
    sys.exit(0)

    finalList = lengthSplit(commaList) 

    return(finalList)
#--- end sentenceSplit function

#--- define lengthSplit function
def lengthSplit(thirdList):
    finalList = []
    for sentence in thirdList:
        if len(sentence) >= MAX_CHARACTER_LENGTH_PER_LINE:       #--- long sentence which will be split by max length
            #print('\nlong sentence found=', sentence)
            sentenceSplit = sentence.split()       #--- split string into a list where each word is a list item
            sentence = ''
            for word in sentenceSplit:
                #print('\nword=', word)
                if len(sentence) + len(word) > MAX_CHARACTER_LENGTH_PER_SPLIT_LINE:  #-- check if the next word would exceed the permitted length
                    finalList.append(sentence)
                    sentence = word + ' '
                else:
                    sentence = sentence + word + ' '
                    #print('\nsentence=', sentence)
                    finalList.append(sentence)
        else:
            finalList.append(sentence)

    return(finalList)

#--- end of lengthSplit function

#--- start Recursive split
def paragraphSplit(sentenceList):            #--- function is called with a list of sentences
    import re
    import stringsplit

    mysentenceList = []
    semicolonList = []
    commaList = []
    finalList = []      #--- to  hold the final list of sentences
    #print('\nStarting Paragraph Split!')

    #for i in range(0, len(sentenceList)):
    #    print('\ni=', i, sentenceList[i])

    paragraph_text = stringsplit.convertListToString(sentenceList)     #convert the list to a string
    #print('\nAfter string conversion\n', paragraph_text)

    mysentenceList = periodSplit(paragraph_text)         #--- call the function to split the paragraph into sentences by periods
    mysentenceList = generalSplit(mysentenceList)         #--- call the function to split the paragraph into sentences by periods
    mysentenceList = semicolonSplit(mysentenceList)         #--- call the function to break the lines down by semi-commas
    mysentenceList = commaSplit(mysentenceList)         #--- call the function to break the lines by commas
    mysentenceList = finalSplit(mysentenceList)         #--- call the function to break the lines by max character limit
    finalList = reJoin(mysentenceList)                  #--- call the function to join short sentences

    return(finalList)           #--- return List of sentences
#--- end Recursive split

#--- start period split
def periodSplit(string):            #--- function is called with a string
    import re
    import stringsplit

    mysentenceList = []
    mystring = string.replace('\n', ' ')          #--- replace newline characters with spaces
    stringDelim = '\.'    
    sentenceList = re.split(stringDelim, mystring)         #--- 1st pass, use regex to break sentences by '.' 
    
    for i in range (0, len(sentenceList) - 1):
        sentence = sentenceList[i] + '.'         #--- regex removes the '.'; add the periods back  at the end of the sentence
        sentence = sentence.strip()    #--- strip leading and trailing spaces on each sentence
        sentenceList[i] = sentence

    #for sentence in sentenceList:
    #    print(sentence)
    
    return(sentenceList)
#--- end period split

#--- start semicolon split
def semicolonSplit(sentenceList):            #--- function is called with a list of sentences
    import re
    import stringsplit

    segmentList = []
    finalList = []
    stringDelim = '\;'

    for i in range(0, len(sentenceList)-1):
        sentence = sentenceList[i]
        if len(sentence) >= MAX_CHARACTER_LENGTH_PER_LINE and ';' in sentence:       #--- long sentence which can be split by ';'
            segmentList = re.split(stringDelim, sentence)     #--- 2nd pass, each break sentences by ';'

            for j in range(0, len(segmentList)):          #--- insert the segments into the sentenceList
                if j < len(segmentList):
                    if not '.' in segmentList[j]:
                        segmentList[j] = segmentList[j] + ';'    #--- add back the ';' a the end of the line
                    finalList.append(segmentList[j])
        else:
            finalList.append(sentenceList[i])          #--copy each sentence to the output list

        i += 1
    #print('\nSemiColon Split\n')
    #for sentence in finalList:
    #    print('\nLenght of sentence=', len(sentence), 'sentence=', sentence)
    
    return(finalList)
#--- end semicolon split

#--- start general split
def generalSplit(sentenceList, stringDelim='?'):            #--- function is called with a list of sentences
    import re
    import stringsplit
    import sys

    segmentList = []
    finalList = []
    #stringDelim = '\;'

    for i in range(0, len(sentenceList)-1):
        sentence = sentenceList[i]
 
        if stringDelim in sentence:
            segmentList = sentence.split(stringDelim)     #--- 2nd pass, each break sentences by tehe specified delimiter

            if len(segmentList) > 0:
                for j in range(0, len(segmentList)):          #--- loop through the segments
                    sentence = segmentList[j]
                    sentence = sentence.strip()
                    if not sentence.endswith('.'):
                        sentence = sentence + stringDelim       #--- add back the delimiter
                    finalList.append(sentence)    #--- add to the list
        else:
            finalList.append(sentence)          #--copy each sentence to the output list

        i += 1
    print('\nAfter General Split:')
    for sentence in finalList:
        print('\nLenght of sentence=', len(sentence), 'sentence=', sentence)

    return(finalList)
#--- end semicolon split


#--- define commaSplit function
def commaSplit(sentenceList):
    finalList = []
    sentence = ''
    stringDelim = ','

    #print('\nStart Comma Split\n')
    #for sentence in sentenceList:
    #    print('\nLenght of sentence=', len(sentence), 'sentence=', sentence)
    
    for i in range(0, len(sentenceList)):
        sentence = sentenceList[i]

        if len(sentence) >= MAX_CHARACTER_LENGTH_PER_LINE and ',' in sentence: #--- long sentence which can be split by ','
            #print('\nLong sentence = ', sentence)
            segmentList = sentence.split(stringDelim)     #--- 3rd pass, break sentences by ',' 
            #print('\ni=', i, 'Long sentence split by commas\n', segmentList)

            j = 0
            #print('\nNumber of sentence segments:', len(segmentList))
            currentPhrase = segmentList[j] + ','
            for phrase in segmentList:
                #print('\nWorking on segment number:', j)
                if j + 1 > len(segmentList) -1 :
                    currentPhrase = currentPhrase.replace(',,', ',').replace(';,', ';').replace('.,', '.')
                    finalList.append(currentPhrase)
                    #print('\nfinal Phrase=', currentPhrase)
                else:
                    nextPhrase = segmentList[j +1]
                    #print('\nCurrent Phrase =', j, ' ', currentPhrase, '\nNext Phrase=', nextPhrase)

                    if len(currentPhrase) + len(nextPhrase) >  MAX_CHARACTER_LENGTH_PER_LINE:
                        currentPhrase = currentPhrase + ','
                        currentPhrase = currentPhrase.replace(',,', ',')
                        finalList.append(currentPhrase)
                        #print('\nSentence break for phrase =', len(currentPhrase), 'sentence =', currentPhrase)
                        currentPhrase = nextPhrase + ','
                    else:
                        currentPhrase = currentPhrase + nextPhrase + ','
                        #print('\nJoin Current Phrase and Next Phrase=', currentPhrase)
                        #finalList.append(sentence)
                j += 1
        else:
            sentence = sentence.replace('.,', '.')      #--- strip extraneous "," at the end of a sentence
            #print('\nLength of sentence =', len(sentence), 'sentence =', sentence)
            finalList.append(sentenceList[i])

        i+=1
    #s = 0
    #for sentence in finalList:
    #    s +=1
    #    print('\nS=', s, ' Lenght of sentence=', len(sentence), 'sentence=', sentence)

    return(finalList)
#--- end of commaSplit

#--- start final split
def finalSplit(sentenceList):            #--- function is called with a list of sentences to split sentences based on threshold
    import re
    finalList = []
    print('\nStart Final Split - Max character per line:', MAX_CHARACTER_LENGTH_PER_LINE )
    for sentence in sentenceList:
        if len(sentence) >= MAX_CHARACTER_LENGTH_PER_LINE:       #--- long sentence which will be split by max length
            #print('\nlong sentence found=', sentence)
            sentenceSplit = sentence.split()       #--- split string into a list where each word is a list item
            
            sentence = ''
            for word in sentenceSplit:
                #print('\nword=', word)
                if len(sentence) + len(word) > MAX_CHARACTER_LENGTH_PER_SPLIT_LINE:  #-- check if the next word would exceed the permitted length
                    #print('n\Word break - sentence=', sentence)
                    sentence = sentence.strip()
                    finalList.append(sentence)
                    sentence = word + ' '
                    #print('\nSentence after word break:', sentence)
                else:
                    sentence = sentence + word + ' '
                    #print('\nsentence=', sentence)
            sentence = sentence.strip()
            finalList.append(sentence)
        else:
            sentence = sentence.strip()
            finalList.append(sentence)

    print('\nAfter Final 
    Split')
    s = 0
    for sentence in finalList:
        s +=1
        print('\nS=', s, ' Lenght of sentence=', len(sentence), 'sentence=', sentence)
    
    return(finalList)
#--- end final split

#--- start reJoin -  see if short sentences can be combined
def reJoin(sentenceList):            #--- function is called with a list of sentences to rejoin short sentences if possible
    print('\nRejoin')
    finalList = []
    phrase = ''

    for i in range(0, len(sentenceList)):
        sentence = sentenceList[i]
        for j in range(i, len(sentenceList)):
            print('\nlength of sentence=',len(sentence), 'sentence=', sentence)
            nextSentence = sentenceList[i+1]
            if sentence[-1] == '.' and len(sentence) + len(nextSentence) < MAX_CHARACTER_LENGTH_PER_LINE:
                sentence = sentence + ' ' + nextSentence
            else:
                finalList.append(sentence)
                print('\ni=', i, sentence, 'j=', j)
                break
            j += 1
        
        finalList.append(sentence)
        i +=j
    

    s = 0
    for sentence in finalList:
        s +=1
        print('\nS=', s, ' Lenght of sentence=', len(sentence), 'sentence=', sentence)
        
#--- end reJoin function

    wordString = wordSplit(TEST_STRING2)
    wordCount = 0
    for word in wordString:
        print ('\nWordCount=', wordCount, ' -Word=', word)
        wordCount +=1

    sys.exit(0)


    formattedString = stringSplit(TEST_STRING,
                              MAX_CHARACTER_LENGTH_PER_LINE)

# Print list and show characters for each element.

    for line in formattedString:
        print (line, '\n> Number of characters:', len(line), '\n')

			