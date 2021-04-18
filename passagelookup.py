#--- https://api.esv.org/docs/samples/
#!/usr/bin/env python

import sys
import requests

API_KEY = 'ad0e0de3fd9289f49425ba1c4ff7cb224d11f7a5'
API_URL = 'https://api.esv.org/v3/passage/text/'

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
        'Authorization': 'Token %s' % API_KEY
    }

    response = requests.get(API_URL, params=params, headers=headers)

    passages = response.json()['passages']

    return passages[0].strip() if passages else 'Error: Passage not found'

#--- end of GetESVText function

def parse_passages(passages):
    scripture = ''
    book_chapter = ''
    passages = passages.replace(',', ';')
    for p in passages.strip().split(';'):       #split into multiple passages
        if ':' in p:
            book_chapter, verse = p.split(':', 1)
        else:
            ref = book_chapter.rstrip()
            p =  ref + ':'  + p

        numbers = ('-' in p)
        passage = get_esv_text(p, numbers).replace('[', '').replace(']', '').replace('–', '-').replace('\n\n  ', ':  ')
        passage = p + '\n' + passage + '\n'
        scripture = scripture + passage + '\n'
    #print('\nparse passage: \n')
    #print(scripture)
    return(scripture)       #--- return scripture as a string with newline characters
