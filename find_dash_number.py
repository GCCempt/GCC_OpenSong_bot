import re
import passagelookup
import stringsplit
import sys
import utils

#--- find pattern of dash followed by number in a string
def parse_string(input_string):
    print('\nInput String:', input_string)

    #match = re.findall( r"([2-3]-)(9|(1(?:0|1)))", string )
    #matches = re.split( r"(\-?[0-9])", input_string )
    #matches = input_string.split('—')
    matches = input_string.split('—')
    print('\nmatches=', matches)
    matched = []
    
    i = 0
    for match in matches:
        i += 1
        if i < len(matches):
            new_match = match + '—'         #--- add back the split character
            matched.append(new_match)
            print('\nmatch=', new_match)

        else:
            matched.append(match)
            print('\nmatch=', match)

    print(matched)
        
    #--- Inpute String "13Cursed is everyone who is hanged on a tree”—14 so that in Christ Jesus" 
    #--- Output: ['13Cursed is everyone who is hanged on a tree', '14 so that in Christ Jesus']
    # ============ DO NOT DELETE BELOW THIS LINE - MAIN FUNCTION CALL =======================
#
if __name__ == "__main__":
    input_passage = 'galatians 3:13-18; 28-29; John 3:16-17; 21-23'
    print('\nInput Passage=', input_passage)
    scripture_verses = passagelookup.build_scripture_text(input_passage)   #--- returns a list of scripture refs

    for verse in scripture_verses:
        print(verse)
        
#
# ======================================================================================