# ------------Start Function to parse the affirmation of faith
def read_affirmation_of_faith():
    import filelist

    bulletin_path = 'bulletin/'
    body_text = ''
    # -------------- Read the contents of the Affirmation of Faith text file -----------------------------
    try:
        with open(bulletin_path + filelist.AffirmationFileName, 'r') as textFile:
            affirmation_of_faith = textFile.read().replace('\n', ' ')
    except:
        body_text = "Missing affirmation of faith"
        return(body_text)

    # --- determine if this is a Heidelberg Catechism
    if 'HEIDELBERG CATECHISM' in affirmation_of_faith or 'WESTMINSTER LARGER CATECHISM' in affirmation_of_faith:
        body_text = process_cathechism(affirmation_of_faith)
    else:
        body_text = process_cathechism(affirmation_of_faith)
    return(body_text)
# --- end parse affirmation of faith

#--- Process Hedelberg and Westminster athechism
def process_cathechism(aof_text):
    import re

    body_text = aof_text.replace('Q.', 'Q-').replace('A.', 'A-')   #--- temporarily protect the Q. & A. tag
 
    body_text = re.sub('Q-(\d+)\.', 'Q-\\1-', body_text)   #--- temporarily replace "Qn." with "Qn-" to prevent newline replacement below
    body_text = re.sub(r'(\.)\s', '. \n', body_text)   #--- add newline character at the end of each sentence
    body_text = body_text.replace('Q-', '\nQ.').replace('A-', '\nA.')   #--- restore the Q. & A. tag with a preceding newline break

    body_text = re.sub('Q.(\d+)-', 'Q.\\1.', body_text)   #--- temporarily replace "Qn." with "Qn-" to prevent newline replacement below
    body_text = re.sub('CONGREGATION:', '\nCONGREGATION:', body_text) #--- ensure new line preceeds congregation section
    body_text = re.sub('A \(', '\nA (', body_text) #--- ensure new line preceeds congregation section

    body_text = body_text.splitlines(True)      #--- split the string into a list based on newline

    try:
        body_text.remove(' \n')      #--- remove emty lines
    except:
        pass

    try:
        body_text.remove('\n')       #--- remove lines with just a newline character
    except:
        pass
   
    try:
        body_text.remove(' ')          #--- remove blank lines
    except:
        pass

    return(body_text)  # --- return the body_text array
# -----------End Function to process cathechisms