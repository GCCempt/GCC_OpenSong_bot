# --- Split a string by a number followed by a space
def split_on_number(text):
    first_verse = True  # --- flag to identify the first verse number
    final = [text.split()[0]]  # Autoload the first item

    for i in text.split()[1:]:  # Ignore the first item (item 0)

        try:
            # Try to convert it to a float
            float(i)

        except ValueError:
            # if there's an issue, append to last item
            final[-1] = " ".join([final[-1], i])

        else:
            # if you can convert to a float, then it is possibly a verse number
            if first_verse:
                final.append(i)
                prev_verse = int(i)  # --- get the initial verse number
                first_verse = False
            else:
                # --- validity check to ensure this verse is an increment of the previous
                int_i = int(i)
                # --- check if the new "verse" i 1 greater than the previous or if reset to 1 (indicates a chapter change)
                if int_i == prev_verse + 1 or int_i == 1:
                    final.append(i)
                    # print(final)
                    prev_verse = int(i)  # --- save the current verse number
                else:
                    final[-1] = " ".join([final[-1], i])  # --- continue normal processing

    return (final)  # --- return a list of verses


# --- end split_on_number -Split a string by a number followed by a space

# --- Start split a string by a newline character '\n'
# --- https://pythonexamples.org/python-split-string-by-new-line/
def split_on_newline(text):
    # text = 'Welcome\nto\nPythonExamples.org'
    final = text.split('\n')  # split string based on newline character

    for i in range(0, len(final)):
        print('\n i=', i, 'text=', final[i])
    return (final)


# --- Start convert a list into a string
# --- https://www.kite.com/python/answers/how-to-join-a-list-together-with-a-newline-character-in-python
def convertListToString(Element_List=['The', 'Quick', 'Brown',
                                      'Fox']):  # --- default list provided, but can overriden on the function call
    # text = 'Welcome\nto\nPythonExamples.org'
    joined_string = ''.join(Element_List)

    # print('\n Joined String=', joined_string)
    return (joined_string)  # --- return String

def convertListToStringWithNewLine(Element_List=['The', 'Quick', 'Brown',
                                      'Fox']):  # --- default list provided, but can overriden on the function call
    # text = 'Welcome\nto\nPythonExamples.org'
    joined_string = '\n'.join(Element_List)

    # print('\n Joined String=', joined_string)
    return (joined_string)  # --- return String

# --- Start parse string - split by '-'
def split_on_dash(input_string):
    string_split = input_string.split('—')

    matched = []

    i = 0
    for match in string_split:
        i += 1
        if i < len(string_split):
            new_match = match + ' — '  # --- add back the split character
            matched.append(new_match)

        else:
            matched.append(match)

    return (matched)  # --- return a list of verses

    # --- Inpute String "13Cursed is everyone who is hanged on a tree”—14 so that in Christ Jesus"
    # --- Output: ['13Cursed is everyone who is hanged on a tree'-, '14 so that in Christ Jesus']
