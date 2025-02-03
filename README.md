# iPod Classic to Online Playlist Scripting
3 Simple python scripts created with AI assitance to parse iPod Classic data files,
and create online playlists with generated Spotify & Youtube API's.
Although I have previous experience creating python scripting, this was a favor for family, and so I used an LLM
as an ease of use tool, and debugged any quirks/structure/application that result from it not having genuine reasoning.
Thought I'd publish it as it only took me less than an hour.

# Installation
- Python
- install spotipy
- install mutagen

## a. Spotify API
- Acquire a spotify api via developer program, and find all credentials & secret_auth in project profile
- Put respective data into files
## b. Youtube API
- Acquire a google api via google cloud developer program, and install Youtube Data API V3 to project
- Create OAuth 2.0 credentials for an installed application, in this case desktop
- Install the Google API client libraries
- Put JSON file within project folder, not in external iPod folder
- Put respective data into files

# Using program
- After putting respective PATH into files, run in order of:
1. ipod_read_script.py
2. create_playlists.py
3. lost_songs.py
- You'll find that google API is much more limiting in token use, so lost_songs.py should
  really be used to find those not found in spotify

The structure of generated files was formatted into both JSON and txt for ease of use, for any other uses.

Any unclear instructions should be found easily with a search, I withheld from any direct links and terminal commands
as others may have other shells, and links become depreciated. 
This can be easily made in a containerized docker program, to avoid any prequisite libraries, which I plan on making.
When done, I'll link to that here, for more security and deployability.
Enjoy!
