############## SECURITY NOW PODCAST FILES: RUN PROGRAM ##############

from sn_files_user_variables import use_log_file, path_to_logs, output_directory

from sn_files_utils import output_directory_check, log_file_setup, latest_episode_number, last_downloaded_episode, grab_sn_transcripts_pdfs, grab_sn_transcripts_txts, grab_sn_shownotes_pdfs, grab_sn_shownotes_htm

############################ NOTES ############################
""" Security Now podcast goodies come in the following file formats:

* Shownotes: currently published in pdf format. Historically, from Episode#1 to #177, they were published in htm format.

* Transcripts: published in pdf and txt format, both currently and historically.

---
Any function calls which can potentially trigger a large number of requests / downloads have been left commented out with a single (#) to prevent accidental execution / spamming grc's servers. Uncomment the function calls (delete the '# ') to run them. 

---
All you need to do is supply your required ep_start & ep_stop integers (as int, not str) and uncomment whichever function call(s) you wish to run. No other code editing is required.

"""


############ REQUIRED: PRE-PROCESSING FUNCTIONS ############
"""Sets up logfile & grabs latest episode number from grc.com. Fill in your preferences in sn_files_user_variables.py first. These three function calls must be run before any of the other utility functions"""

output_directory_check(output_directory)
log_file_setup(use_log_file, path_to_logs)
latest_episode = latest_episode_number() # determines latest episode number as published on grc.com


############ GRAB THE SINGLE VERY LATEST EPISODE ############
"""Grabs the files, in the specified format for the very latest published episode on grc.com. Comment out any of the below lines to skip grabbing that file type for the latest episode."""

ep_start = latest_episode-1
ep_stop = latest_episode
# grab_sn_shownotes_pdfs(output_directory, latest_episode, ep_start, ep_stop)
# grab_sn_transcripts_txts(output_directory, latest_episode, ep_start, ep_stop)
# grab_sn_transcripts_pdfs(output_directory, latest_episode, ep_start, ep_stop)


#### GRAB ONLY MOST RECENCT EPISODES MISSING FROM DOWNLOAD FOLDER #####
"""Dynamically determines difference between latest_episode published on grc.com and the most recent episode's files in the output_directory folder. 

NB: Point output_directory towards the location where your goldmine of Security Now files is currently saved. 

NB: The script only works if your existing files are named in the original format "sn-xxx.pdf" or "sn-xxxx.txt" for transcripts or "sn-xxx-notes.pdf" for shownotes. If the files are named differently, the script will not work as intended and will regard the latest episo.

BEWARE: If the folder detects no filenames in the sn-xxx or sn-xxx-notes format, it will exit the program. This is to prevent accidental mass downloads of the entire back catalogue.

The first function call (left uncommented) will look into your output_directory and determine most recent episode number you already have, for each of the three file types (pdf transcript, txt transcript, pdf shownotes).

"""

last_downloaded_pdf_transcript, last_downloaded_txt_transcript, last_downloaded_pdf_shownotes = last_downloaded_episode(output_directory)

# grab_sn_transcripts_pdfs(output_directory, latest_episode, last_downloaded_pdf_transcript, latest_episode)

# grab_sn_transcripts_txts(output_directory, latest_episode, last_downloaded_txt_transcript, latest_episode)

# grab_sn_shownotes_pdfs(output_directory, latest_episode, last_downloaded_pdf_shownotes, latest_episode)


############ GRAB BACK CATALOGUE, MANUAL SPECIFICATION ############

"""Grab the back-catalogue of transcripts in pdf format.
Available range: 001 to latest_episode.
TEST ME"""
ep_start = 1
ep_stop = latest_episode
# grab_sn_transcripts_pdfs(output_directory, latest_episode, ep_start, ep_stop)

"""Grab the back-catalogue of transcripts in txt format.
Available range: 001 to latest_episode.
TEST ME"""
ep_start = 1
ep_stop = latest_episode
# grab_sn_transcripts_txts(output_directory, latest_episode, ep_start, ep_stop)

"""Grab the back-catalogue of shownotes in pdf format.
Available range: 432 to latest_episode.
TEST ME"""
ep_start = 432 # must be 432 or later
ep_stop = latest_episode
# grab_sn_shownotes_pdfs(output_directory, latest_episode, ep_start, ep_stop)

"""Grab the back-catalogue (finite) of shownotes in htm format (historical).
Available range: 001 - 177.
Shows missing htm notes: 138, 139, 140, 146, 148-152, 154, 156, 158-163, 165-168, 169-175; these will simply be passed over.
TEST ME"""
# grab_sn_shownotes_htm(output_directory, ep_start=1, ep_stop=177)













