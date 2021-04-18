#------ Insert XML element
import xml.etree.ElementTree as ET

def insertxmlelement(slide_group_name):

#---------------- Variables for filtering message by date / time
    setfilepath = 'C:\\Dropbox\\OpenSongV2\\OpenSong Data\\Sets\\TemplateSet'
    print('\nInput Template Set:', setfilepath)
    print('\nInsertXMLElement Start - Slide Group Name: ', slide_group_name)

    #-------------- Open the Template Set and load into XML document tree -----------------------------
    datasource = open(setfilepath, 'rb')
	 
    doctree = ET.parse(datasource)
    root = doctree.getroot()
    
    #print('\n',[elem.tag for elem in root.iter()])
        
    print(root.find('./slide_groups/slide_group[@name="{value}"]'.format(value=slide_group_name)))
    

    for slide_group in root.iter('slide_group'):
        print(slide_group.tag, slide_group.attrib)
        
        try:
            myslidegroup = slide_group.find('./slide_groups/slide_group[@name="{value}"]'.format(value=slide_group_name))
            #print('\n    InsertXMLElement found slide_group_name: ', myslidegroup)

        except:
            print('\n    InsertXMLElement slide_group_name not found: ', myslidegroup)

   
    #tree = root.find('./slide_groups/slide_group[@name="{value}"]'.format(value=slide_group_name))
    #print(child.tag, child.attrib)
    #print(tree.type)
    #for child in tree:
    #    print(child.tag, child.attrib)

    #for child in tree.iter('slide_group'):
    #    print(child.tag, child.attrib)

    outputset =r'C:\\Dropbox\\OpenSongV2\\OpenSong Data\\Sets\\OutputSet'
    print('\nOutput Set:' + outputset)

    doctree.write(outputset)
