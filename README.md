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


