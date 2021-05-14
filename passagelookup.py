# --- https://api.esv.org/docs/samples/
# !/usr/bin/env python

import sys
import requests
import os

ESV_API_KEY = os.environ['ESV_API_KEY']
ESV_API_URL = 'https://api.esv.org/v3/passage/text/'

def get_esv_text(passage, numbers):
    params = {
        'q': passage,
        'include-headings': False,
        'include-footnotes': False,
        'include-verse-numbers': True,
        'include-short-copyright': False,
        'include-passage-references': False
    }

    headers = {
        'Authorization': 'Token %s' % ESV_API_KEY
    }

    response = requests.get(ESV_API_URL, params=params, headers=headers)

    passages = response.json()['passages']

    return passages[0].strip() if passages else 'Error: Passage not found'


# --- end of GetESVText function

def old_parse_passages(passages):
    scripture = ''
    book_chapter = ''
    passages = passages.replace(',', ';')
    for p in passages.strip().split(';'):  # split into multiple passages
        if ':' in p:
            book_chapter, verse = p.split(':', 1)
        else:
            ref = book_chapter.rstrip()
            p = ref + ':' + p

        numbers = ('-' in p)
        passage = get_esv_text(p, numbers).replace('[', '').replace(']', '').replace('–', '-').replace('\n\n  ', ':  ')
        passage = p + '\n' + passage + '\n'
        scripture = scripture + passage + '\n'
    # print('\nparse passage: \n')
    # print(scripture)
    return (scripture)  # --- return scripture as a string with newline characters

#--- ensure proper formatting of scripture references
def parse_passages(input_passages):			#--- input is a string
    full_ref_passages = []						#--- list to hold the complete scripture references

    passages = input_passages.replace(',', ';')		#--- standarize ';' as scripture separator
    passages = passages.strip().split(';')	#--- split the string into an array

    #--- get book, chapter, verse
    hold_book_chapter = ''			#-- save the book and chapter reference
    book = ''
    chapter = ''
    scripture = ''
    for p in passages:
        p = p.strip()
        if ' ' in p:				#--- indicates a references includes book; e.g. 'john '
            if ':' in p:				#--- indicates a complete references includes book; e.g. 'john 3:'
                book_chapter, verse = p.split(':', 1)
                book, chapter = book_chapter.split(' ', 1)
                hold_book_chapter = book_chapter.strip()	#--- remove leading and trailing spaces
                passage_ref = hold_book_chapter + ':' + verse
                full_ref_passages.append(passage_ref)
            else:
                passage_ref = hold_book_chapter + ':' + verse   
                full_ref_passages.append(passage_ref)
                book, chapter = hold_book_chapter.split(' ', 1)
        else:
            if ':' in p:    #--- no book; just chapter and verse(s), e.g. 5:1-3
                passage_ref = book + ' ' + p
                full_ref_passages.append(passage_ref)
                book_chapter, ref = passage_ref.split(':', 1)
                hold_book_chapter = str(book_chapter) + ':'

            else:
                verse = p
                passage_ref = hold_book_chapter + ':' + verse
                full_ref_passages.append(passage_ref)       
                book_chapter, ref = passage_ref.split(':', 1)
                #hold_book_chapter = str(book_chapter) + ':'

    #print('\nInput passage=', input_passages, '\n')
    for p in full_ref_passages:         #--- look up each passage
        numbers = ('-' in p)
        passage = get_esv_text(p, numbers).replace('[', '').replace(']', '').replace('–', '-').replace('\n\n  ', ':  ')
        passage = p + '\n' + passage + '\n'
        scripture = '\n' + scripture + passage + '\n'
        
        #print(p)
    
    #print('\nComplete passage lookup:\n')
    #print(scripture)
    return(scripture)       #--- returns a string variable