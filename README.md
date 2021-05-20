[![CodeQL](https://github.com/GCCempt/GCC_OpenSong_bot/actions/workflows/codeql-analysis.yml/badge.svg?branch=main)](https://github.com/GCCempt/GCC_OpenSong_bot/actions/workflows/codeql-analysis.yml)
# GCCOpenSongBot
## Automate OpenSong processing

#### Design goals:
* Replace manual and tedious, error-prone procedure
*	Integrate all the elements for the OpenSong Projection set (bulletin, various Discord announcements)
*	Create a base OpenSong set with all the necessary elements
*	The set can then be audited / reviewed and completed for use during Sunday Worship

#### Inputs:
*	Messages / Commands from Discord
*	PDF Bulletin downloaded from the website when the above notification is received
*	Template XML OpenSong set

#### Process:
*	Verify all the necessary inputs have been received (monitor files)
*	Download and convert the PDF bulletin to a text file for processing
*	Parse the bulletin:
*	Determine which type (template) OpenSong set will be used
*	Extract the relevant content and write to processing files
*	Read the selected template XML OpenSong set
*	Insert the current information from the processing files created from the bulletin content above
*	Write a new XML OpenSong Set

#### Outputs:
*	Message posts to Discord #opensong channel with status updates
*	XML OpenSong Set based on the current bulletin

#### Docker Environment Variables:
| ENV                  | Description                                                                                           |
|----------------------|-------------------------------------------------------------------------------------------------------|
| DISCORD_TOKEN        | Discord Bot Token                                                                                     |
| READCHANNELID        | The channel ID for the discord channel where announcements are posted                                 |
| POSTCHANNELID        | The Channel ID for the discord channel where commands can be run and output from the bot is displayed |
| DROPBOX_ACCESS_TOKEN | The API key for dropbox                                                                               |
| FTP_HOSTNAME         | Hostname for FTP server                                                                               |
| FTP_USERNAME         | Username for sFTP Access                                                                              |
| FTP_PASSWORD         | Password for sFTP Access                                                                              |
| ESV_API_KEY          | API key to https://api.esv.org                                                                        |
| ENVIRON              | PROD or DEV                                                                                           |
| COMPUTERNAME         | For use in Dev environements for creation of the set

#### File Descriptions
| Python   File Name     | Description                                                                                                                                                                |
|------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| downloadbulletin.py    | Download the latest bulletin from the GCC website; call the readbulletin.py function to process it                                                                         |
| dropbox_api_call.py    | Use the DropBox API to write files to Dropbox                                                                                                                              |
| extractpdftext.py      | Read the downloaded pdf bulletin file, extract the text, and write to a file for additional processing                                                                     |
| filelist.py            | Contains static definitions of all the files used in the processing                                                                                                        |
| getdatetime.py         | Used for date manipulation, conversion, etc.                                                                                                                               |
| ~~insertxml.py~~           | Intended to be a general purpose routine to insert elements in an XML doctree, but not currently used                                                                      |
| maintainsong.py        | Utility function for manipulating  song items to be added to Dropbox and for various song lookup functions                                                                 |
| monitorfiles.py        | Routine to check the current status of the process and determine whether all the prerequisites are met to build the Opensong set                                           |
| mydiscord.py           | Main Discord bot for processing and responding to Discord Post messages and / or # commands                                                                                |
| myroutine.py           | Used to unit test various scripts as needed                                                                                                                                |
| opensong.py            | Main routine to build the elements of the set when all the prerequisite conditions are met                                                                                 |
| passagelookup.py       | Routine to call the ESV API to lookup scripture passages.                                                                                                                  |
| readbulletin.py        | Read the extracted text file from the bulletin, extract various content to discreet files for later processing.                                                            |
| readworshipschedule.py | Read the file extracted from the Discord Worship Schedule post; extract the songs and write them to a file for additional processing                                       |
| rundiscord.py          | Main routine to launch the Discord Bot                                                                                                                                     |
| sftp_files.py          | Use pysftp to push files to and pull files from the website                                                                                                                |
| stringManip.py         | Break a paragraph of text into blocks of max n characters to fit into a single Opensong slide                                                                              |
| stringsplit.py         | Split a string by a number followed by a space; split a string based on newline                                                                                            |
| test_script.py         | Test and validation script used to test full functionality of the process when the Bot starts                                                                              |
| getdatetime.py         | General utility function which can be reused                                                                                                                               |
| writehtml.py           | Creates html files which are stored on the website and then pulled into iframes on the livestream page. The files are a summary of the bulletin, and the scripture reading |
