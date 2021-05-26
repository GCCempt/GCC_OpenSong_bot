# -------- Read bulletin file -------------------------------
# ! python3
import logging
import os
import sys

import extractpdftext  # --- my module to convert PDF bulletin to .txt file
import filelist  # --- definition of list of files and directories used in the proces

set_path = 'sets/'
bulletin_path = 'bulletin/'


# ------------ Read bulletin text file function -
def selectset():
    # --- read and parse the text bulletin file to select a template set for processing
    file1 = open(bulletin_path + filelist.TextBulletinFilename, 'r', encoding='utf-8', errors='ignore')
    Lines = file1.readlines()
    file1.close()

    # ----- scan bulletin lines to determine which template set to use
    inputset_name = 'SampleSet'  # --- set the default value
    line_count = 0
    for line in Lines:
        # print(i, end = '')
        line_count += 1

        if 'songofassurance' in line.replace(" ", '').replace('\t', '').lower():
            inputset_name = 'SampleSet-NoGloriaPatri'  # -- use the "no Gloria Patri set"
            # --- check if Lord's Supper is included
            for j in range(line_count, len(Lines)):
                if 'Sacrament' in Lines[j]:
                    inputset_name = 'SampleSet-NoGloriaPatriWCommunion'  # --- use the communion set
            break

        elif "thegloriapatri" in line.replace(" ", '').replace('\t', '').lower():
            inputset_name = 'SampleSet'  # --- use the standard set
        elif 'Sacrament' in line:
            inputset_name = 'SampleSet-Communion'  # --- use the communion set
        elif 'on the Lords Day ' in line:
            bulletin_date = Lines[line_count]
            print('\nReadBulletin.readtxt - inputset_name=', inputset_name, ' for bulletin date:', bulletin_date)

    # --- write the selected set name to a file for later processing
    textFile = open(bulletin_path + filelist.SetFilename, 'w', encoding='utf-8', errors='ignore')
    textFile.write(str(inputset_name))
    textFile.close()

    return ()


# ------------ End of readtxt function definition

# --------------- Start of main program ---------------------------
def getfiles():
    # ------------------------ Read component files -----------
    print(
        '\nReadBulletin.getfiles - Welcome to OpenSong Create Set Script to parse the bulletin and create an OpenSong Set!')

    # ---------------- Verify the bulletin file exists ------------
    print('\nInput Bulletin: ', bulletin_path + filelist.PDFBulletinFilename, '\n')
    if not os.path.exists(bulletin_path + filelist.PDFBulletinFilename):
        print("File path {} does not exist. Exiting...".format(bulletin_path + filelist.PDFBulletinFilename))
        sys.exit()

    extractpdftext.fitz_extract_text(bulletin_path + filelist.PDFBulletinFilename,
                                     bulletin_path + filelist.TextPDFBulletinFilename)  # --- read the pdf bulletin and convert to text file

    selectset()  # --- Read the text bulletin and determine which set template to us

    # print(lines)
    parsebulletin()  # --- extract relevant sections of the bulletin as separate text files
    return ()


# --------------- Parse the text bulletin, extract relevant text, write to individual files  ---------------------------
def parsebulletin():
    # --- read the bulletin text file Using readlines()
    file1 = open(bulletin_path + filelist.TextBulletinFilename, 'r', encoding='utf-8', errors='ignore')
    Lines = file1.readlines()
    file1.close()

    count = 0
    aof_tag = 'aof'  # --- set default value for affirmation of faith tag
    for line in Lines:
        count += 1
        # --- extract Announcements from bulletin
        if 'announcements' in Lines[count].lower():
            # print('\nAnnouncements  - found; count =', count, ' bulletin line=', Lines[count])
            if 'Doxology' in Lines[count + 1]:
                # print('\n    ReadBulletinParseBulletin - Doxology line follows Announcements bulletin line=', Lines[count+1])
                continue
            else:
                announcement_tag = ['1.', '2.', '3.', '4.', '5.', '6.', '7.', '8.', '9.', '10.', '11.', '12.']

                body_text = 'Announcements\n'
                # print('\nLine Count=', count, ' line=', Lines[count].encode('utf-8'))

                count += 1  # --- advance one line to skip the worship leader name
                for count in range(count, len(Lines) - 1):
                    if 'presbyterianchurch' in Lines[count].replace(" ", '').replace('\t', '').lower():
                        break
                    else:
                        try:
                            prefix, text = Lines[count].split(' ', 1)
                            # --- split the line at the first space to remove the #'s
                            result = any(([True if subStr in prefix else False for subStr in announcement_tag]))
                            if result:
                                body_text = body_text + text
                            else:
                                body_text = body_text + prefix + ' ' + text
                        except Exception as e:
                            logger.WARNING(e)
                            body_text = Lines[count]
                    count += 1

                # print('    ReadBulletin.ParseBulletin - end of Announcements.')
                # --- write the corporate confession to text file
                textFile = open(bulletin_path + filelist.AnnouncementFileName, 'w', encoding='utf-8',
                                errors='ignore')  # --- output announcement text file
                textFile.write(str(body_text))
                textFile.close()
                continue

                # --- extract Call To Worship from bulletin
        if 'calltoworship' in line.replace(" ", '').replace('\t', '').lower():
            # print('\nCall To Worship  - found; count =', count, ' bulletin line=', Lines[count])
            body_text = 'Call To Worship\n'
            for count in range(count, len(Lines) - 1):
                body_text = body_text + Lines[count]

                if 'songofapproach' in Lines[count + 1].replace(" ", '').replace('\t', '').lower():
                    # print('\n    End of Call To Worship  - found Song of Approach in suceeding line; count=', count, ' line=', Lines[count+1])
                    # --- write the Call to Worship of Faith to text file
                    textFile = open(bulletin_path + filelist.CallToWorshipFileName, 'w', encoding='utf-8',
                                    errors='ignore')  # --- output call to worship text file
                    textFile.write(str(body_text))
                    textFile.close()
                    break
                else:
                    continue

        # --- extract Scripture Reading from bulletin
        if 'scripturereading' in Lines[count].replace(" ", '').replace('\t', '').lower():
            # print('\nScripture Reading  - found; count =', count, ' bulletin line=', Lines[count])
            body_text = 'Scripture Reading\n'
            count += 1  # --- increment the count to get the next line with the scripture text
            body_text = body_text + Lines[count]

            # --- write the Scripture Reading to text file
            textFile = open(bulletin_path + filelist.ScriptureFileName, 'w', encoding='utf-8',
                            errors='ignore')  # --- output call to worship text file
            textFile.write(str(body_text))
            textFile.close()

            continue

        # --- extract sermon information from bulletin
        if 'sermon' in Lines[count].replace(" ", '').replace('\t', '').lower():
            # print('\nSermon Info  - found; count =', count, ' bulletin line=', Lines[count])
            body_text = 'Sermon    '
            count += 1
            body_text = body_text + Lines[count]
            count += 1
            body_text = body_text + Lines[count]
            # --- write the Bulletin Sermon info to text file
            textFile = open(bulletin_path + filelist.BulletinSermonFilename, 'w', encoding='utf-8',
                            errors='ignore')  # --- output call to worship text file
            textFile.write(str(body_text))
            textFile.close()

            continue

        # --- extract Affirmation of Faith "tag" from bulletin
        if 'affirmationoffaith' in Lines[count].replace(" ", '').replace('\t', '').lower():
            # print('\nReadbulletin.parsebulletin Affirmation of Faith header - found;
            # count =', count, ' bulletin line=', Lines[count])
            count += 1  # ---get the actual Confession title which is stored in the suceeding line
            aof_tag = Lines[count].replace(" ", '').replace('\t', '').lower()
            # print('\nAffirmation of Faith tag added; count =', count, ' bulletin line=', aof_tag)
            aofextract(aof_tag, count,
                       Lines)  # --- Call the aofextract routine to write the affirmation of faith to file
            continue

        # --- extract the Bulletin Date from bulletin
        if 'orderforpublicworship' in Lines[count].replace(" ", '').replace('\t', '').lower():
            bulletin_date = Lines[count + 3]
            # print('\nBulletin Date found; count =', count, ' bulletin line=', Lines[count])

            # --- write the bulletin date to text file
            textFile = open(bulletin_path + filelist.BulletinDateFilename, 'w', encoding='utf-8', errors='ignore')
            textFile.write(str(bulletin_date))
            textFile.close()
            break
        else:
            continue

        continue

    return ()


# --------------- End of Parse the text bulletin

# --------------- Extract the Affirmation of Faith from the bulletin  ---------------------------
def aofextract(aof_tag, count, Lines):
    # --- extract the Affirmation of Faith text from bulletin
    aof_tag = aof_tag.replace(" ", '').replace('\t', '').replace(",", "").replace(".", "").lower()
    aof_tag = aof_tag.strip()
    # print('\nAOFExtract - aof_tag=', aof_tag)

    # --- scan the bulletin content to match the Affirmation of Fatih
    body_text = 'Affirmation of Faith' + '\n'
    end_index = len(Lines) - 1
    for i in range(count, end_index):
        i += 1
        temp_line = Lines[i].replace(" ", '').replace('\t', '').replace(",", "").replace(".", "").lower()
        temp_line = temp_line.strip()
        # print('\nAOFExtract - aof_tag=', aof_tag, ' - i =', i, ' temp line=', temp_line)

        if aof_tag in temp_line:
            # if aof_tag in Lines[i].replace(" ", '').replace('\t', '').replace(",", "").replace(".", "").lower():
            for j in range(i, end_index):
                body_text = body_text + Lines[j]
                if 'gracechristianchurch' in Lines[j + 1].replace(" ", '').replace('\t', '').lower():
                    # print('\nReadBulletin.aofextrct - Write the Affirmation of Faith to text file')
                    # print('\nAffirmation of Faith body text=', body_text)
                    textFile = open(bulletin_path + filelist.AffirmationFileName, 'w', encoding='utf-8',
                                    errors='ignore')
                    textFile.write(str(body_text))
                    textFile.close()
                    return ()
        else:
            continue
    # --------------- end of Extract the Affirmation of Faith from the bulletin  ---------------------------
