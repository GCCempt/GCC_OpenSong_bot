# --- https://api.esv.org/docs/samples/
# !/usr/bin/env python

import sys
import requests
import os
import utils
import stringsplit

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

#--- funtion to convert scripture references to full scripture text
def build_scripture_text(input_scripture):
    scripture_refs = utils.parse_passages(input_scripture)   #--- returns a list of scripture refs
    #print('\nScripture Refs=', scripture_refs)
    scripture = ''          #--- stores the raw scripture text from the ESV API
    final_scripture_list =[]    #--- holds the separated verses

    #--- lookup each individual passage
    for p in scripture_refs:         #--- look up each passage
        numbers = ('-' in p)
        passage = get_esv_text(p, numbers).replace('[', '').replace(']', '').replace('–', '-').replace('\n\n  ', ':  ')
        passage = p + '\n' + passage + '\n'
        scripture = '\n' + scripture + passage + '\n'
        
        dash_split_verses = stringsplit.split_on_dash(scripture)    #--- returns a list

        #--- convert array to string
        new_scripture = stringsplit.convertListToString(dash_split_verses)  #--- returns a string

        #print('\nreturn from convertListToString:\n', new_scripture)

        number_split_verses = stringsplit.split_on_number(new_scripture)    # returns a list
        final_scripture_list = final_scripture_list + number_split_verses
        scripture = ''      #--- reset the string for holding the ESV passage lookup
    
    return(final_scripture_list)