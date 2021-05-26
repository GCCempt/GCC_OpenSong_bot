# --- https://stackabuse.com/reading-and-writing-xml-files-in-python/
def addsong(mytree, slide_group_name, song_name, presentation_order):
    import xml.etree.ElementTree as ET

    # --- remove invalid charactes from song name which are not supported by OpenSong
    # song_name = song_name.replace("'", '').replace(',', '')
    # --- Read Template set

    # mytree = ET.parse('C:\\Dropbox\\OpenSongV2\\OpenSong Data\\Sets\\TemplateSet')
    my_root = mytree.getroot()
    my_node = mytree.find('./slide_groups')
    j = 0  # --- index used to count the slide groups

    # print('\nLength of XML document', len(myroot[0]))
    # print(ET.tostring(myroot, encoding='utf8').decode('utf8'))

    # print('Adding a song Slide Group=', slide_group_name)

    # find all "slide_group" objects and print their "name" attribute
    for elem in my_root:
        for subelem in elem.findall('slide_group'):
            j += 1  # ----- increment the index for counting the slide groups
            # print(elem.tag, elem.text, elem.attrib)

            if subelem.get('name').lower() == slide_group_name.lower():
                # print('\nSuccess - Slide Group Found', 'Name:', subelem.get('name'), ' Attrib:', subelem.attrib)

                # ----------- Build New Slide Group
                new_slide_group = ET.Element('slide_group')
                slide_attrib = {'name': song_name, 'type': 'song', 'presentation': presentation_order, 'path': ''}
                new_slide_group.attrib = slide_attrib

                # --- add the new element to the set
                my_node.insert(j, new_slide_group)  # ----------- insert the new slide_group

    return mytree


# --- end of addsong function

# --- Start of Add Scripture Function to add a Scripture node to OpenSong
def addscripture(mytree, slide_group_name, scripture_ref):
    import xml.etree.ElementTree as ET
    import passagelookup  # --- modulue to do API lookup for ESV passage from Crossway

    # --- parse the input passage(s) and create a list of the verse text -------
    verses = []

    verses = passagelookup.build_scripture_text(scripture_ref)  # --- returns a list of scripture verses

    # --- Read Template set to be updated
    myroot = mytree.getroot()
    mynode = mytree.find('./slide_groups')
    j = 0  # --- index used to count the slide groups

    # find all "slide_group" objects and print their "name" attribute
    for elem in myroot:
        for subelem in elem.findall('slide_group'):
            j += 1  # ----- increment the index for counting the slide groups
            # print(elem.tag, elem.text, elem.attrib)

            if subelem.get('name').lower() == slide_group_name.lower():
                # print('\nSuccess - Slide Group Found', 'Name:', subelem.get('name'), ' Attrib:', subelem.attrib)

                # ----------- Build Scripture Slide Group
                new_slide_group = ET.Element('slide_group')
                scripture_ref = scripture_ref + '|ESV'
                slide_attrib = {'type': 'scripture', 'name': scripture_ref, 'print': 'true'}
                new_slide_group.attrib = slide_attrib

                # --- add the new element to the set
                mynode.insert(j, new_slide_group)  # ----------- insert the new slide_group

                # ----------- Build Title SubElement
                new_title = ET.SubElement(new_slide_group, 'title')
                new_title.text = scripture_ref
                # new_slide_group.append(new_title)

                # ----------- Build Slides SubElement
                new_slides = ET.SubElement(new_slide_group, 'slides')

                # ----------- Build Slide and body text for each verse in the scripture passage
                for p in range(0, len(verses)):
                    # print(verses[p])
                    new_slide = ET.SubElement(new_slides, 'slide')
                    new_body = ET.SubElement(new_slide, 'body')
                    if scripture_ref in verses[1]:
                        continue
                    else:
                        new_body.text = verses[p]

                # ----------- Add the static "Thanks be to God" text for the Scripture Reading
                if slide_group_name == 'Scripture Reading':
                    thanks_text = 'LEADER: This is the Word of the Lord. \n CONGREGATION: Thanks be to God.'
                    new_slide = ET.SubElement(new_slides, 'slide')
                    new_body = ET.SubElement(new_slide, 'body')
                    new_body.text = thanks_text

                # ----------- Build SubTitle SubElement
                new_subtitle = ET.SubElement(new_slide_group, 'subtitle')
                new_subtitle.text = 'ESV'
                # new_slide_group.append(new_subtitle)

    return mytree


# --- end of addscripture function

# --- Start of findnode function to locate the position to insert a new XML element
def findnode(mytree, slide_group_name):
    myroot = mytree.getroot()  # --- XML document tree passed as a parameter
    # mynode = mytree.find('./slide_groups')          #--- select the starting point in the XMLTree
    j = 0  # --- index used to find the position to insert the new element

    # --- process through the "slide_group" elements to find a match on slide_group_name
    for elem in myroot:
        for subelem in elem.findall('slide_group'):
            j += 1  # ----- increment the index for counting the slide groups
            # print(elem.tag, elem.text, elem.attrib)

            if subelem.get('name').lower() == slide_group_name.lower():
                print('\nSuccess - Slide Group Found', 'Name:', subelem.get('name'), ' Attrib:', subelem.attrib)
                return j  # return the position where the new slide group content will be insterted


# --- end of findnode function

# --- Start of Add Body text Function to add body text to a slide group
def addbodytext(doctree, slide_group_name, body_text):
    root = doctree.getroot()
    # --- find the matching slide group
    try:
        tree = root.find('./slide_groups/slide_group[@name="{value}"]'.format(value=slide_group_name))
        e = tree.findall('slides/slide/body')  # find the <body> slides for the specified slide_group_name
    except:
        print('\n    SlideGroupLookup slide_group_name not found: ', slide_group_name)
        return ()

    for j in e:
        j.text = body_text  # ------ modify the body text -------
        # print('\n    SlideGroupLookup - New Slide Body Text for ', slide_group_name, ' = ', j.text,)

    return ()


# --- Start of Add slides from a "list / array" to a slide group
def addbodyslides(doctree, slide_group_name, body_text):
    import xml.etree.ElementTree as ET
    root = doctree.getroot()
    # --- find the matching slide group
    try:
        # tree = root.find('./slide_groups/slide_group[@name="{value}"]'.format(value=slide_group_name))
        tree = root.find('./slide_groups/slide_group[@name="{value}"]/slides'.format(value=slide_group_name))

        # e = tree.findall('slides/slide/body')           # find the <body> slides for the specified slide_group_name
    except:
        print('\n    SlideGroupLookup slide_group_name not found: ', slide_group_name)
        return ()

    # ----------- Build Slide and body text for each sentence in the body text
    for p in range(0, len(body_text)):
        # print('\naddnode.addbodyslides - p=', p, 'body_text=', body_text[p])
        new_slide = ET.SubElement(tree, 'slide')
        new_body = ET.SubElement(new_slide, 'body')
        new_body.text = body_text[p]

    return ()
# --- end of add confession text function
