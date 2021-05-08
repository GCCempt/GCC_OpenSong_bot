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
