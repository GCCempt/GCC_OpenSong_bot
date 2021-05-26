# -------- Read pdf bulletin file and convert to text-------------------------------
# ! python3
# ---- using pyMuPDF; https://stackoverflow.com/questions/55767511/how-to-extract-text-from-pdf-in-python-3-7
def fitz_extract_text(bulletin_path, OutputtextFilename):
    import fitz  # pymupdf package
    import filelist
    set_path = 'sets/'
    bulletin_dir = 'bulletin/'

    with fitz.open(bulletin_path) as doc:
        text = ""
        count = 0
        for page in doc:
            # line = page.getText().strip().encode('utf-8')
            # line = line.encode('utf-8')
            # print('\nCount=',count, 'line=', line))
            count += 1
            text += page.getText().strip()
    # print(text)

    # --- write the PDF text to a temporary text file
    textFile = open(bulletin_dir + filelist.TextPDFBulletinFilename, 'w', encoding='utf-8', errors='ignore')
    textFile.write(text)
    textFile.close()

    # --- read the temporary text file into an array of Lines
    # print('\nExtractPDFText.extract_text - Read Converted PDF file:', PDF_text_fileName)

    # --- Using readlines()
    file1 = open(bulletin_dir + filelist.TextPDFBulletinFilename, 'r', encoding='utf-8', errors='ignore')
    Lines = file1.readlines()

    count = 0
    text = ''
    # --- read the file and print line by line
    for line in Lines:
        count += 1
        #    print("Line{}: {}".format(count, line))
        #    print('count=', count, 'line length=', len(line), 'line=', line)

        if len(line) > 2:  # --- skip blank lines
            text = text + line  # --- add non-empty lines to a new string

    # --- write the text string to a new text file
    textFile = open(bulletin_dir + filelist.TextBulletinFilename, 'w', encoding='utf-8', errors='ignore')
    # textFile.write(str(text, 'utf-8'))
    textFile.write(str(text))

    textFile.close()

    # print('\nExtractPDFText.extract_text - Write converted PDF file to text file:', OutputtextFilename)

    # --- read the final text file into an array of Lines
    # print('\nExtractPDFText.extract_text - Read final text file:', OutputtextFilename)

    # --- Using readlines()
    file1 = open(bulletin_dir + filelist.TextBulletinFilename, 'r', encoding='utf-8', errors='ignore')
    Lines = file1.readlines()
    file1.close()

    count = 0
    for line in Lines:
        count += 1
        # print("Line{}: {}".format(count, line))
        # print('count=', count, 'line length=', len(line), 'line=', (line)
    # print('number of lines=', count)

    return ()
