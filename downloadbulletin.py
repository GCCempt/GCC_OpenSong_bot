# ---- https://www.geeksforgeeks.org/downloading-files-web-using-python/
import json
import urllib.request
from urllib.request import Request, urlopen

import filelist  # --- definition of list of files and directories used in the process
import monitorfiles
import readbulletin

set_path = 'sets/'
bulletin_path = 'bulletin/'

# --- WordPress REST API endpoint for media discovery.
# --- The church site moved to Hostinger and the Apache directory autoindex now
# --- returns HTTP 403, so the old "scrape /wp-content/uploads/YYYY/MM/" approach
# --- no longer works.  The WP REST media endpoint replaces it.
WP_MEDIA_API_URL = (
    'https://graceem.gccvapca.org/wp-json/wp/v2/media'
    '?search=EM_Bulletin&orderby=date&order=desc&per_page=10'
)

USER_AGENT = (
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:78.0) '
    'Gecko/20100101 Firefox/78.0'
)

# --- network timeouts (seconds).  Tunable in one place so a slow/hung
# --- Hostinger response can't block the async Discord handler indefinitely.
API_TIMEOUT = 30  # JSON REST API call
DOWNLOAD_TIMEOUT = 60  # PDF download (larger payload)


# --- using urllib2
def get_bulletin():  # --- function to download bulletin
    bulletins = get_current_bulletin()  # --- find the URL of the current bulletin

    if not bulletins:  # --- no EM_Bulletin entries returned by the WP REST API
        raise RuntimeError(
            'No EM_Bulletin entries were returned by the WordPress REST API at '
            '{}.  Either the search term changed or the site is unreachable.'
            .format(WP_MEDIA_API_URL)
        )

    current_bulletin = bulletins[0]  # --- newest entry (API returns desc by date)
    current_bulletin_url = current_bulletin['url']

    # --- retrieve the current bulletin and write to local file
    # Download the current bulletin file from `url` and save it locally under `file_name`:
    req = urllib.request.Request(current_bulletin_url)
    req.add_header('User-Agent', USER_AGENT)
    req.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8')

    file_name = bulletin_path + filelist.PDFBulletinFilename
    with urllib.request.urlopen(req, timeout=DOWNLOAD_TIMEOUT) as response, open(file_name, 'wb') as out_file:
        data = response.read()  # a `bytes` object
        out_file.write(data)

    readbulletin.getfiles()  # --- process the downloaded bulletin file
    status_message = monitorfiles.filechecker()  # --- check if all files are ready to be processed

    return status_message


# --- end of get_bulltine function


def get_current_bulletin():  # --- function to find the most recent bulletin via WP REST API
    """Query the WordPress REST API for EM_Bulletin media entries.

    Returns a list of dicts, newest first, where each dict has at minimum:
        url  - the PDF URL (from `guid.rendered`)
        date - the upload timestamp (ISO-8601 string from `date`)
        slug - the WordPress slug (e.g. 'em_bulletin_260517')
    """
    print('\nDownloadBulletin.get_current_bulletin - WP REST API:', WP_MEDIA_API_URL)

    req = Request(WP_MEDIA_API_URL)
    # ---- fix issue #167 HTTP Error 406
    req.add_header('User-Agent', USER_AGENT)
    req.add_header('Accept', 'application/json')

    raw = urlopen(req, timeout=API_TIMEOUT).read()
    entries = json.loads(raw)

    bulletins = []
    for entry in entries:
        guid = entry.get('guid') or {}
        url = guid.get('rendered', '')
        # --- defensive: only keep entries that actually look like bulletin PDFs
        if '.pdf' not in url.lower():
            continue
        if 'em_bulletin' not in url.lower() and 'em_bulletin' not in entry.get('slug', '').lower():
            continue
        bulletins.append({
            'url': url,
            'date': entry.get('date', ''),
            'slug': entry.get('slug', ''),
        })

    return bulletins


if __name__ == "__main__":
    results = get_current_bulletin()
    print('Found {} EM_Bulletin entries.  Top 3:'.format(len(results)))
    for entry in results[:3]:
        print('  ', entry['date'], entry['url'])
