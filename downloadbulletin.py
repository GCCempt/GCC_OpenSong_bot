# ---- https://www.geeksforgeeks.org/downloading-files-web-using-python/
from datetime import datetime, timedelta
from urllib.request import Request, urlopen, urlretrieve

from bs4 import BeautifulSoup

import filelist  # --- definition of list of files and directories used in the process
import monitorfiles
import readbulletin

set_path = 'sets/'
bulletin_path = 'bulletin/'


# --- using urllib2
def get_bulletin():  # --- function to download bulletin
    import urllib.request
    # bulletinurl = 'http://graceem.gccvapca.org/wp-content/uploads/'  #-- bulletin URL
    bulletinurl = build_directory_name()  # -- call my module getdate() to build the bulletin directory URL

    bulletins = get_current_bulletin(bulletinurl)  # --- find the URL of the current bulletin

    # print('\n Bulletins=', bulletins, 'number of bulletins=', len(bulletins))
    if len(bulletins) == 0:  # --- no bulletins found for current month
        bulletinurl = build_prev_month_directory_name()  # --- look in the previous month's directory
        bulletins = get_current_bulletin(bulletinurl)  # --- find the latest bulletin of the previous month

    current_bulletin = max(bulletins)  # --- get the current bulletin
    current_bulletin_url = bulletinurl + current_bulletin
    # --- retrieve the current bulletin and write to local file

    # Download the current bulletin file from `url` and save it locally under `file_name`:
    req = urllib.request.Request(current_bulletin_url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:78.0) Gecko/20100101 Firefox/78.0')
    req.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8')

    file_name = bulletin_path + filelist.PDFBulletinFilename
    with urllib.request.urlopen(req)  as response, open(file_name, 'wb') as out_file:
        data = response.read() # a `bytes` object
        out_file.write(data)

    readbulletin.getfiles()  # --- process the downloaded bulletin file
    status_message = monitorfiles.filechecker()  # --- check if all files are ready to be processed

    return status_message


# --- end of get_bulltine function

# --- https://stackoverflow.com/questions/11023530/python-to-list-http-files-and-directories/34718858
def get_current_bulletin(bulletinurl):  # --- function to find the most recent bulletin
    # bulletinurl = 'http://graceem.gccvapca.org/wp-content/uploads/2021/02/'  #-- bulletin URL
    # bulletinurl = build_directory_name()
    # -- call my module getdate() to build the bulletin directory URL

    # outputfile = 'C:\\Dropbox\\OpenSongV2\\Bulletin\\bulletin.pdf'
    # #---  path for downloaded bulletin
    #bulletinurl = 'http://graceem.gccvapca.org/wp-content/uploads/2021/07/'  #-- bulletin URL OVERRIDE FOR TESTING
    print('\nDownloadBulletin.get_current_bulletin - Bulletin file path: ', bulletinurl)

    bulletins = []
    url = bulletinurl
    req = Request(url)

    #---- fix issue #167 HTTP Error 406
    req.add_header('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:78.0) Gecko/20100101 Firefox/78.0')
    req.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8')

    a = urlopen(req).read()  # --- read the bulletin directory

    soup = BeautifulSoup(a, 'html.parser')
    x = (soup.find_all('a'))
    for i in x:
        file_name = i.extract().get_text()
        url_new = url + file_name
        url_new = url_new.replace(" ", "%20")
        if file_name[-1] == '/' and file_name[0] != '.':
            # read_url(url_new)          # call this function recursively for each subdirectory
            break
        # print(url_new)
        if '.pdf' in file_name:
            # print(file_name)
            bulletins.append(file_name)

    return bulletins


# --- https://stackoverflow.com/questions/28189442/datetime-current-year-and-month-in-python
# --- function to get the current year and month to build the correct bulletin directory URL
def build_directory_name():
    current_month = datetime.now().strftime('%m')  # ---// 02 //This is 0 padded
    current_year_full = datetime.now().strftime('%Y')  # ---// 2018

    # print('Current year:', current_year_full, ' current month:', current_month)
    bulletin_directory = 'http://graceem.gccvapca.org/wp-content/uploads/' + current_year_full + '/' + current_month + '/'
    print('Bulletin Directory:', bulletin_directory)

    return bulletin_directory


# --- https://stackoverflow.com/questions/28189442/datetime-current-year-and-month-in-python
def build_prev_month_directory_name():  # --- function to build the bulletin directory URL for previous month
    current_month = datetime.now() - timedelta(days=6)  # ---// Go back 6 days
    current_month = current_month.strftime('%m')  # ---// This is 0 padded

    current_year_full = datetime.now() - timedelta(days=6)  # ---// Go bakc 6 days
    current_year_full = current_year_full.strftime('%Y')  # ---// This is padded

    print('Current year:', current_year_full, ' current month:', current_month)
    bulletin_directory = 'http://graceem.gccvapca.org/wp-content/uploads/' + current_year_full + '/' + current_month + '/'
    print('Bulletin Directory:', bulletin_directory)

    return bulletin_directory
