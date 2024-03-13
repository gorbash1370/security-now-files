# Security Now Podcast Files - Transcripts & Shownotes


# Intro
A simple program coded in 'novice Python' to automate downloading the Security Now podcast transcripts and shownotes as generously published by Steve Gibson on [grc.com](https://www.grc.com/securitynow.htm). 

Being a career-switcher, I've missed many years of great content before I found out about the show. I wrote this program as a quick way to download the back-catalogue of transcripts so that I could find out what "three dumb routers" meant, see if Steve had recommended any hard-drive brands in the past, search for all his & Leo's past Sci-Fi recommendations, search back to re-read that deep-dive I couldn't understand from last year..., etc etc.

(Please note, this code was developed when the full search facility on [grc.com](https://www.grc.com/securitynow.htm) wasn't working - as of SN#964 Steve fixed this so it may be best for those who aren't compulsive DataHoarders like me to just search grc.com directly for specific topics!)

Whilst I can't deny that if my ML skills were good enough I'd have tried developing a 'Steve-bot' to answer all my networking and security queries, for now, this tool serves as a bridge to that wealth of information.

# Options
1) **Grab Latest**: Grab the single very latest episode published on [grc.com](https://www.grc.com/securitynow.htm) (options for shownotes, transcript pdf and transcript txt). Yes, this is just a lazy replacement for going to grc.com and right-clicking 'download'!
2) **Grab Missing**: Grab only the most recent episodes missing from your current download folder. For example, if you only collect the shownotes, and your last download was "sn-950-notes.pdf" with the latest episode being SN#970, the function call `grab_sn_shownotes_pdfs`, when pointed to the directory containing "sn-950-notes.pdf" will download all shownotes between SN#950 and SN#970. Options for shownotes (pdf), transcript (pdf) and transcript (txt). Your files must have been left with their original naming convention for these functions to work.
3) **Grab Back-Catalogue**: Grab the back catalogue of Security Now goodies. Set `ep_start` to 1 for all episodes, or specify your own episode start number.  Options for transcript (pdf), transcript (txt), shownotes (pdf) and the historically published shownotes in htm.


# Note: Usage
* Users will need to know how to uncomment lines of code (individual function calls in `sn_files_main.py`), in order to select them for execution. The comments and straighforward function names indicate what each one does. You'll also need to enter an integer value for `ep_start` and `ep_stop` immediately preceeding the function you wish to run.
* Users will need to fill in the `output_directory` path in `sn_files_user_variables.py`
* For the best functionality, leave downloaded files with their original filenames.
* Similarly, your `output_directory` will be set to the same place where you store any previously downloaded sn-files.
* Please be polite to servers and respect the short pre-set time delay programmed between requests. Even if you want to grab the entire back catalogue, it doesn't take long.


# Dependencies
`pip install requests` - one external Python library.
Otherwise, no external dependencies (just standard Python library imports)

# Program Structure  # if there are multiple files
[`sn_files_user_variables.py`]() - set the `output_directory` for where the downloaded files should be saved, set whether you want to use the logging functionality (and if so, where to save the log.txt files)  
[`sn_files_utils.py`]() - program functionality  
[`sn_files_main.py`]() - executes the program. The function calls in the "Pre-Processing Functions' Section will need to run before any utility function call. NB: The function calls which make external requests are deliberately left commented out by default to prevent accidental / mass execution. Uncomment the specific lines you want to run.


# Other files 
[`README.md`]() - voila!  
[`requirements.txt`]() - lists the packages installed by running `pip install requests`  
[`LICENCE.md`]() - lgpl-3.0 licence  


# Notes: Installation & Testing
* Code was developed with Python 3.12 and on a Windows (10) machine. It should work on other OSs but _I have not tested this_.
* I built the code as robustly as I could, but **I have not had chance to do extensive testing**. Please do let me know what errors you find and I'll do my best to fix them.


# Start / User Setup
* Install [dependencies](#dependencies) as mentioned above
* Make sure you've read the [#Options](#options), [#Notes: Usage](#notes-usage) and [#Program Operation](#program-operation) sections carefully so you understand the program capacity.
* `sn_files_user_variables.py` - complete the variable values following the instructions in the comments
* Select which functions you want to run within `sn_files_main.py`, by uncommenting the function call. Set your `ep_start` and `ep_stop` numbers. Make sure the function calls in the "Pre-Processing Functions" section are uncommented (they are provided as such). And off you go!


# Program Operation
* **File Checks and Setup**: Initially, the program checks your specified output directory is valid, sets up the log file (if selected) and queries grc.com to determine the latest published episode number. 

* **Downloading Episodes**: Depending upon which of the [Options 1-3](#options) function calls you uncommented and your specified `ep_start` & `ep_stop` episode ranges, the program proceeds to download the specified range of episodes in the desired formats. This process involves accessing [grc.com](https://www.grc.com/securitynow.htm), fetching the relevant files, and saving them in the designated output directory.

  * Option 2 **Grab Missing** additonally runs `last_downloade_episode()` on your `output_directory` to determine previously downloaded files (only works on standard filenames) and therefore deduce the residual the range of episodes to be fetched.
  
* **Workhorse Functions**: These are `grab_sn_shownotes_pdf()`, `grab_sn_transcripts_pdfs()`, `grab_sn_transcripts_txts()` (plus `grab_sn_shownotes_htm()`). All these have extensive docstrings and commentary, plus are all coded in very straightforward Python, so please see the code to understand the steps they go through. 

* **Logging and Time Estimation**: Throughout the process, the program maintains a log file (if enabled), recording actions and any issues encountered. It also estimates the time required for the entire download process, based on the number of episodes and a courtesy pause implemented between requests to avoid over-pestering the server.

* **Duplication Avoidance**: To prevent redundant downloads, the program checks for existing files in the output directory and skips any episodes already downloaded.


# gorbash1370 Disclaimer
This is an amateur project built mainly for coding practice, therefore...
* Commentary may appear excessive (learning 'notes')
* Some code is expanded (rather than shortened & simplified) for learning clarity.
* Please always inspect code before running. Use at your own risk!


# Licences
[Licence]()  


# If you enjoy this project...
- If you find any bugs or errors, please do let me know.
- Please consider sending me some project feedback or any suggestions for improvement!
- [BuyMeACawfee](https://www.buymeacoffee.com/gorbash1370)

_Last code update 2024-03-13_