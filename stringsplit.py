#--- Split a string by a number followed by a space
def split_on_number(text):

    final = [text.split()[0]]  # Autoload the first item
    for i in text.split()[1:]: # Ignore the first item

        try:
            #Try to convert it to a float
            float(i)           

        except ValueError: 
            # if there's an issue, append to last item
            final[-1] = " ".join([final[-1], i]) 

        else:
            # if you can convert to a float, then append it
            final.append(i)    
    #print(final)
    return(final)
#--- end split_on_number -Split a string by a number followed by a space

#--- Start split a string by a newline character '\n'
#--- https://pythonexamples.org/python-split-string-by-new-line/
def split_on_newline(text):
    #text = 'Welcome\nto\nPythonExamples.org'
    final = text.split('\n')  # split string based on newline character

    for i in range(0, len(final)):
        print('\n i=', i, 'text=', final[i])
    return(final)

#--- Start convert a list into a string
#--- https://www.kite.com/python/answers/how-to-join-a-list-together-with-a-newline-character-in-python
def convertListToString(Element_List=['The', 'Quick', 'Brown', 'Fox']):  #--- default list provided, but can overriden on the function call
    #text = 'Welcome\nto\nPythonExamples.org'
    joined_string = ''.join(Element_List)

    #print('\n Joined String=', joined_string)
    return(joined_string)           #--- return String