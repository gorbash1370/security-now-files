############## SECURITY NOW PODCAST FILES: UTILITY FUNCTIONS ##############
from datetime import datetime as dt
import re
import requests
import os
import sys
import time

from sn_files_user_variables import use_log_file

######################### GLOBAL VARIABLE #########################

log_path = "" # this is returned by the log_file_setup function. If use_log_file is set to True in sn_files_user_variables.py, log_path will be required by all functions that write to the log file. Thus, easier to provide global access.


######################### SETUP OUTPUT DIRECTORY #########################

def output_directory_check(output_directory):
    """ Create a directory to gather all the API output files, if required"""
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)


######################### SETUP LOG FILE ######################### 
        
def log_file_setup(use_log_file, path_to_logs):
    """
    Instanciates .txt log file, if use_log_file is set to True in user_variables.py  Creates the specified directory for the log file if it doesn't already exist.

    Args:
        use_log_file (bool): Flag. If True, a log file will be created. If False, no log file will be created. Specified in sn_files_user_variables.py.
        path_to_logs (str): Path to the directory where the log file will be created. Specified in sn_files_user_variables.py.
    
    Raises:
        TypeError: If value of use_log_file is not a boolean or if log_path is not a string.
        OSError: If there is a system-related error, such as a file not found.
        UnicodeEncodeError: If there are issues with the encoding of the file.

    Returns:
        bool: True if log file is set up successfully, False if log file is not set up.

    Exits:
        sys.exit(): Program will exit if the value of use_log_file was not a boolean value, or if the log file was set to compulsory (True) but could not be instantiated.
    """

    try:
        if not isinstance(use_log_file, bool):
            raise TypeError

    except TypeError:
        formatted_timestamp = dt.now().strftime("%Y-%m-%d_%H-%M-%S")
        msg_error = f"{formatted_timestamp} - Error, use_log_file must be a boolean value: True or False. Check that you haven't entered a string. Exiting program.\n"
        print(msg_error)
        sys.exit(1)

    if use_log_file == False:
        return False
    
    global log_path 
    logfilename = f"log_security_now_files_grab.txt"
    log_path = os.path.join(path_to_logs, logfilename)

    try:
        if not log_path:
            raise TypeError
    except TypeError:
            formatted_timestamp = dt.now().strftime("%Y-%m-%d_%H-%M-%S")
            msg_error = f"{formatted_timestamp} - Error, log_file_path must be either "" for root directory or 'directory_name'. Check that you haven't entered None. Exiting program.\n"
            print(msg_error)
            sys.exit(1)
    try:    
        if os.path.exists(log_path):
            return True
        if not os.path.exists(log_path):
            os.makedirs(path_to_logs, exist_ok=True)
            with open(log_path, 'a'):
                pass
            msg_success = ("Log File Setup - Successful.\n")
            log_file_write(msg_success, log_path)
            return True
        
    except (OSError, UnicodeEncodeError) as e:
            formatted_timestamp = dt.now().strftime("%Y-%m-%d_%H-%M-%S")
            msg_error = f"{formatted_timestamp} - Error, unable to instantiate log file with name {logfilename} in {path_to_logs}. The following error occurred: {e}\n"
            print(msg_error)
            print("Log file is set to compulsory. Exiting program.\n")
            sys.exit(1)


######################### HELPER FUNCTIONS #########################

def log_file_write(msg, log_path):
    """
    Supplied message is printed to screen and written to the log file, prepended with a timestamp. If use_log_file is set to False, the message is only printed to screen.

    Args:
        msg (str): Message to be written to log file.
        log_path (str): Full path of log file to which status messages are written.
    
    Note:
        'use_log_file' (bool): set in sn_files_user_variables.py, should be a True or False to control whether logging to file is enabled.
    
    Returns: None
    """
    print(msg)
    if use_log_file == False:
        return
    else:
        formatted_timestamp = dt.now().strftime("%Y-%m-%d_%H-%M-%S")
        msg_timestamped = f"{formatted_timestamp} - " + msg
        with open(log_path, "a") as log_file:
            log_file.write(msg_timestamped)


def request_time_est(ep_start, ep_stop):
    """Calculates and prints/logs the expected time to run based on a 0.5 second pause between requests."""
    seconds = (((int(ep_stop)+1)-int(ep_start))*0.5)
    minutes = round(seconds/60, 2)
    msg_time = f"It is expected that this function will take at least {seconds} seconds to run ({minutes} minutes) to run based on a 0.5 second courtesy pause between requests, if all files in the range are available.\n"
    log_file_write(msg_time, log_path)


################ DETERMINE LATEST AVAILABLE EPISODE NUMBER ################

def latest_episode_number():
    """Determines the latest episode number by scraping the Security Now podcast webpage at grc.com.
    
    Returns:
        int: The latest episode number, if found.

    Raises:
        requests.RequestException or ValueError: If the request to the webpage fails.
        Exception: If the webpage parse is unsuccessful.

    """
    base_url = "https://www.grc.com/securitynow.htm"
    try: 
        response = requests.get(base_url)
        if response.status_code == 200:
            html_content = response.text
            # Remove this after tested
            # with open("security_now_webpage.txt", "w") as sn_html_file:
            #     sn_html_file.write(html_content)
            msg_success = f"Successfully requested {base_url}.\n"
            log_file_write(msg_success, log_path)
        else:
            raise ValueError(f"Unexpected status code: {response.status_code}") 
    except requests.RequestException as e:
        msg_error = f"Error, request failed for {base_url} - {e}\n"
        log_file_write(msg_error, log_path)
    except Exception as e:
        msg_error = f"Error, request failed for {base_url} - {e}\n"
        log_file_write(msg_error, log_path)
         
    # Regex to find the latest 'Episode #___', formatted in html
    episode_pattern = re.compile(r"Episode&nbsp;#(\d+)")
    
    try: 
        # Method 1: Find first instance of the pattern (in current webpage format this will be the latest episode)
        first_episode_match = episode_pattern.search(html_content)
        if first_episode_match:
            global latest_episode
            latest_episode = int(first_episode_match.group(1))
            msg_success = f"The most recent Security Now episode to be published at grc.com is: Episode #{latest_episode}.\n"
            log_file_write(msg_success, log_path)
            return latest_episode

        else:
            msg_error = f"Error, could not find latest episode number on Security Now webpage using Method 1. URL queried: {base_url}.\n"
            log_file_write(msg_error, log_path)
            # should go on to try the other method

            try:       
                # Method 2: find all instances and extract the highest number. This will only be attempted if Method 1 fails.
                all_episode_matches = episode_pattern.findall(html_content)
                if all_episode_matches:
                    highest_episode_number = max(map(int, all_episode_matches))
                    msg_success = f"Latest episode number found: Episode #{highest_episode_number}.\n"
                    log_file_write(msg_success, log_path)
                    return highest_episode_number
                else:
                    msg_error = f"Error, could not find latest episode number on Security Now webpag using Method 2. URL queried: {base_url}.\n"
                    log_file_write(msg_error, log_path)
                    raise Exception("Webpage requested but parse of content unsuccessful.")
            except Exception as e:
                raise Exception   

    except Exception as e:
        msg_error = f"Error, could not find latest episode number on Security Now webpage. URL queried: {base_url}. Error: {e}.\n"
        log_file_write(msg_error, log_path)



################### DETERMINE LAST DOWNLOADED EPISODE ####################
        
def last_downloaded_episode(output_directory):
    """Determines the latest episode number downloaded by checking the output directory for the highest episode number file across the three current formats of transcript / shownotes. 
    
    Dependency: 
        Relies upon the previously downloaded files being named in the original format "sn-xxx.pdf" or "sn-xxxx.txt" for transcripts or "sn-xxx-notes.pdf" for shownotes. If the files are named differently, the function will assess that no Security Now files are present in the folder and abandon any download attempts.
    
    Returns:
        int: The highest downloaded episode number for each of the three formats (pdf transcript, txt transcript, pdf shownotes), if the specified directory contains filenames in the correct format.

        "skip" (str): If no relevant files are found in the specified directory, the function will return "skip" to prevent mass downloading of the entire back catalogue.
    
    """
    # Get a list of all files in the output directory
    all_files = os.listdir(output_directory)
    
    # Filter the list to only include files that are a matching filename format and type

    # For transcripts in pdf format
    pdf_transcripts = [file for file in all_files if re.match(r'sn-\d+\.pdf$', file)]
    if pdf_transcripts:
        pdf_transcript_numbers = [int(file.split("-")[1].split(".")[0]) for file in pdf_transcripts]
        last_downloaded_pdf_transcript = max(pdf_transcript_numbers)
        msg = f"The most recent downloaded pdf transcript in your download folder is Episode: #{last_downloaded_pdf_transcript}.\nRun grab_sn_transcripts_pdfs to download episodes between this and the latest published episode.\n"
        log_file_write(msg, log_path)

    else:
        msg = "No matching sn_xxx.pdf transcripts files found in the output directory. Function will skip this format.\n"
        log_file_write(msg, log_path)
        last_downloaded_pdf_transcript = "skip"

    txt_transcripts = [file for file in all_files if re.match(r'sn-\d+\.txt$', file)]

    # For transcripts in txt format
    if txt_transcripts:
        txt_transcript_numbers = [int(file.split("-")[1].split(".")[0]) for file in txt_transcripts]
        last_downloaded_txt_transcript = max(txt_transcript_numbers)
        msg = f"The most recent downloaded pdf transcript in your download folder is Episode: #{last_downloaded_txt_transcript}.\nRun grab_sn_transcripts_txts to download episodes between this and the latest published episode.\n"
        log_file_write(msg, log_path)

    else:
        msg = "No matching sn_xxx.txt transcripts files found in the output directory. Function will skip this format.\n"
        log_file_write(msg, log_path)
        last_downloaded_txt_transcript = "skip"

    # For shownotes in pdf format
    pdf_shownotes = [file for file in all_files if re.match(r'sn-\d+-notes\.pdf$', file)]
    if pdf_shownotes:
        pdf_shownotes_numbers = [int(file.split("-")[1].split(".")[0]) for file in pdf_shownotes]
        last_downloaded_pdf_shownotes = max(pdf_shownotes_numbers)
        msg = f"The most recent downloaded pdf transcript in your download folder is Episode: #{last_downloaded_pdf_shownotes}.\nRun grab_sn_shownotes_pdfs to download episodes between this and the latest published episode.\n"
        log_file_write(msg, log_path)

    else:
        msg = "No matching sn_xxx-notes.pdf shownotes files found in the output directory. Function will skip this format.\n"
        log_file_write(msg, log_path)
        last_downloaded_pdf_shownotes = "skip"

    # If there are no matching filenames for any of the file formats, the program assumes an incorrect directory path has been supplied or that the back-catalogue function(s) would be more appropriate - so exits. 
    if not pdf_transcripts and not txt_transcripts and not pdf_shownotes: 
        msg_error = "No matching .txt or .pdf files found in the output directory. Either no episodes have been downloaded (in which case, use the back-catalogue functions), or an incorrect output_directory has been selected. Exiting program.\n"
        log_file_write(msg_error, log_path)
        sys.exit

    return last_downloaded_pdf_transcript, last_downloaded_txt_transcript, last_downloaded_pdf_shownotes               


########################## FILE GRAB FUNCTIONS ############################

def grab_sn_shownotes_htm(output_directory, ep_start=1, ep_stop=177):
    """
    Downloads original htm shownotes, for given episode range.
    Htm shownotes were only produced for episodes 001 - 177.
    No shownotes at all 2011, '12, half '13, then pdf from 432.
    Shows missing htm notes: 138, 139, 140, 146, 148-152, 154, 156, 158-163, 165-168, 169-175, these will simply be passed over.

    Args:
        ep_start: episode number to start range, defaults to 1.
        ep_stop: episode number to end range, defaults to 177. 
        
    Available range: 001 - 177.
        
    Syntax examples:
        https://www.grc.com/sn/notes-001.htm
        https://www.grc.com/sn/notes-177.htm
    
    Returns:
        False: if last_downloaded_episode function found no existing files of the sn-xxx or sn-xxx-notes format in the specified directory, it will have returned "skip" to prevent mass downloading via this function.

    """
    if ep_start == "skip": # This string is returned by the last_downloaded_episode function if it finds no existing files of the sn-xxx or sn-xxx-notes format in the specified directory. This is to prevent mass downloading of entire back catalogue via that function, or by accident.
        return False

    # Sanitise episode range values
    if ep_start < 1 or ep_start > 177:
        ep_start = 1
        msg_error = "invalid episode start value entered, 001 used"
        log_file_write(msg_error, log_path)
        
    if ep_stop > 177:
        ep_stop = 177
        msg_error = "invalid episode stop value entered, 177 used"
        log_file_write(msg_error, log_path)
        

    request_time_est(ep_start, ep_stop) # prints & logs expected time to run based on 0.5 second pause between requests

    episodes_to_grab = range(ep_start, ep_stop+1)
    for episode in episodes_to_grab:
        # Format episode number with leading zeros to make it three digits long
        formatted_episode = f"{episode:03}"   
        url_shownotes_htm = f"https://www.grc.com/sn/notes-{formatted_episode}.htm"
        if formatted_episode == "003":
            url_shownotes_htm = "https://www.grc.com/nat/nat.htm"        
        if formatted_episode == "023":
            url_shownotes_htm = "https://www.grc.com/wmf/wmf.htm"
        
        filename_shownotes_htm = f"sn-{formatted_episode}-notes.htm"

        # Duplicate file check
        if os.path.exists(os.path.join(output_directory, filename_shownotes_htm)):
            msg_dupe = f"File {filename_shownotes_htm} already exists. Skipping.\n"
            log_file_write(msg_dupe, log_path)
            continue  # Skip to next iteration if identical filename exists
        
        try:
            response = requests.get(url_shownotes_htm)
            if response.status_code == 200:
                with open(os.path.join(output_directory, filename_shownotes_htm), 'wb') as file: # renders better as 'w' and response.text vs 'wb' and response.content
                    file.write(response.content)
                
                success_msg =f"Successfully downloaded htm shownotes {filename_shownotes_htm}.\n"
                log_file_write(success_msg, log_path)
                time.sleep(0.5)

            else:
                msg_error = f"Failed to download htm shownotes {filename_shownotes_htm}. Status code: {response.status_code}"
                log_file_write(msg_error, log_path)

        except requests.RequestException as e:
            msg_exception = f"Error, request failed for {formatted_episode} htm shownotes - {e}\n"
            log_file_write(msg_exception, log_path)


def grab_sn_shownotes_pdfs(output_directory, latest_episode, ep_start=432, ep_stop=None):
    """Downloads PDF shownotes for given episode range.
    First availble PDF shownote is for episode 432: https://www.grc.com/sn/sn-432-notes.pdf
    
    Args:
        ep_start: episode number to start range, substitutes 432 if None or lower than 432. 
        ep_stop:  episode number to end range, defaults just the start episode if non-sensical stop episode is provided meaning just a single request is made.

    Available range:
        432 to latest_episode. None for #592, #643, #747, #851, #954.
        
    Syntax examples:
        https://www.grc.com/sn/sn-432-notes.pdf

    Returns:
        False: if last_downloaded_episode function found no existing files of the sn-xxx or sn-xxx-notes format in the specified directory, it will have returned "skip" to prevent mass downloading via this function.
    """
    
    if ep_start == "skip": # This string is returned by the last_downloaded_episode function if it finds no existing files of the sn-xxx or sn-xxx-notes format in the specified directory. This is to prevent mass downloading of entire back catalogue via that function, or by accident.
            return False

    # Santize the episode range values
    if ep_start < 432 or ep_start == None:
        msg = "Invalid episode start value entered, 432 used.\n"
        ep_start = 432
        log_file_write(msg, log_path)
    
    if ep_stop is None:
        ep_stop = ep_start + 1  # Default to just the start episode if no stop is provided, to prevent accidental mass-downloading
        msg = "Invalid episode stop value entered, grabbing just one episode.\n"
    
    if ep_stop > latest_episode:
        ep_stop = latest_episode
        msg = "Invalid episode stop value entered, grabbing through to latest episode.\n"
        log_file_write(msg, log_path)


    request_time_est(ep_start, ep_stop) # prints & logs expected time to run based on 0.5 second pause between requests

    episodes_to_grab = range(ep_start, ep_stop+1, 1)
    for episode in episodes_to_grab:
        # Don't need to format episode number with leading zeros as it's already minimum three digits long. Will accommodate 999 & beyond :-)
        url_shownotes = f"https://www.grc.com/sn/sn-{episode}-notes.pdf"
        filename_shownotes = f"sn-{episode}-notes.pdf"

        # Duplicate file check
        if os.path.exists(os.path.join(output_directory, filename_shownotes)):
            dupe_msg = f"File {filename_shownotes} already exists. Skipping.\n"
            log_file_write(dupe_msg, log_path)
            continue  # Skip to next iteration if identical filename exists

        try:
            response = requests.get(url_shownotes)
            if response.status_code == 200:
                with open(os.path.join(output_directory, filename_shownotes), 'wb') as file:
                    file.write(response.content)
                
                success_msg =f"Successfully downloaded PDF shownotes {filename_shownotes}.\n"
                log_file_write(success_msg, log_path)
                time.sleep(0.5)

            else:
                msg_error = f"Failed to download PDF shownotes {filename_shownotes}. Status code: {response.status_code}\n"
                log_file_write(msg_error, log_path)
        
        except requests.RequestException as e:
            msg_exception = f"Request failed for PDF shownotes {filename_shownotes} - {e}\n"
            log_file_write(msg_exception, log_path)


def grab_sn_transcripts_pdfs(output_directory, latest_episode, ep_start, ep_stop):
    """Downloads PDF transcript for given episode range.

    Args:
        ep_start: episode number to start range, defaults to 1
        ep_stop: episode number to end range, defaults just the start episode if non-sensical stop episode is provided.

    Available range: 
        001 to latest_episode.
        
    Syntax examples:
        https://www.grc.com/sn/sn-001.pdf, https://www.grc.com/sn/sn-953.pdf

    Returns:
        False: if last_downloaded_episode function found no existing files of the sn-xxx or sn-xxx-notes format in the specified directory, it will have returned "skip" to prevent mass downloading via this function.
           
    """
    if ep_start == "skip": # This string is returned by the last_downloaded_episode function if it finds no existing files of the sn-xxx or sn-xxx-notes format in the specified directory. This is to prevent mass downloading of entire back catalogue via that function, or by accident.
        return False

    # Sanitise episode range values
    if ep_start < 1 or ep_start > ep_stop:
        ep_start = 1
        msg = "Invalid episode start value entered, 001 used.\n"
        log_file_write(msg, log_path)
    
    if ep_stop < ep_start:
        ep_stop = ep_start + 1  # Default to just the start episode if non-sensical stop episode is provided
        msg = "Invalid episode stop value entered, grabbing just one episode.\n"
        log_file_write(msg, log_path)

    if ep_stop > latest_episode:
        ep_stop = latest_episode
        msg = "Invalid episode stop value entered, grabbing through to latest episode.\n"
        log_file_write(msg, log_path)    


    request_time_est(ep_start, ep_stop) # prints & logs expected time to run based on 0.5 second pause between requests

    episodes_to_grab = range(ep_start, ep_stop+1, 1)
    for episode in episodes_to_grab:
        # Format each episode number with leading zeros to make it three digits long if it's less than 100
        formatted_episode = f"{episode:03}" if episode < 100 else str(episode)
        
        url_transcript_pdf = f"https://www.grc.com/sn/sn-{formatted_episode}.pdf"
        filename_transcript_pdf = f"sn-{formatted_episode}.pdf"

        # Duplicate file check
        if os.path.exists(os.path.join(output_directory, filename_transcript_pdf)):
            msg_dupe = f"File {filename_transcript_pdf} already exists. Skipping.\n"
            log_file_write(msg_dupe, log_path)
            continue  # Skip to the next iteration if identical filename exists
        
        try:
            response = requests.get(url_transcript_pdf)
            if response.status_code == 200:
                with open(os.path.join(output_directory,filename_transcript_pdf), 'wb') as file:
                    file.write(response.content)
                
                msg_success =f"Successfully downloaded PDF transcript for {filename_transcript_pdf}.\n"
                log_file_write(msg_success, log_path)
                time.sleep(0.5)
            else:
                msg_error = f"Failed to download PDF transcript for episode {filename_transcript_pdf}. Status code: {response.status_code}.\n"
                log_file_write(msg_error, log_path)

        except requests.RequestException as e:
            msg_exception = f"Request failed for {filename_transcript_pdf} - {e}\n"
            log_file_write(msg_exception, log_path)


def grab_sn_transcripts_txts(output_directory, latest_episode, ep_start, ep_stop):
    """Downloads txt transcript for given episode range.
    
    Args:
        ep_start: episode number to start range, defaults to 1.
        ep_stop: episode number to end range, defaults just the start episode if non-sensical stop episode is provided.
    
    Available range:
        001 to latest_episode.
    
    Syntax examples:
        https://www.grc.com/sn/sn-001.txt, https://www.grc.com/sn/sn-953.txt

    Returns:
        False: if last_downloaded_episode function found no existing files of the sn-xxx or sn-xxx-notes format in the specified directory, it will have returned "skip" to prevent mass downloading via this function.

    """
    if ep_start == "skip": # This string is returned by the last_downloaded_episode function if it finds no existing files of the sn-xxx or sn-xxx-notes format in the specified directory. This is to prevent mass downloading of entire back catalogue via that function, or by accident.
        return False

    # Sanitise episode range values
    if ep_start < 1 or ep_start > ep_stop:
        ep_start = 1
        msg = "Invalid episode start value entered, 001 used.\n"
        log_file_write(msg, log_path)
    
    if ep_stop < ep_start:
        ep_stop = ep_start + 1  # Default to just the start episode if non-sensical stop episode is provided
        msg = "Invalid episode stop value entered, grabbing just one episode.\n"
        log_file_write(msg, log_path)

    if ep_stop > latest_episode:
        ep_stop = latest_episode
        msg = "Invalid episode stop value entered, grabbing through to latest episode.\n"
        log_file_write(msg, log_path)  
    
    request_time_est(ep_start, ep_stop) # prints & logs expected time to run based on 0.5 second pause between requests

    episodes_to_grab = range(ep_start, ep_stop+1)
    for episode in episodes_to_grab:
        # Format each episode number with leading zeros to make it three digits long if it's less than 100
        formatted_episode = f"{episode:03}" if episode < 100 else str(episode)

        url_transcript_txt = f"https://www.grc.com/sn/sn-{formatted_episode}.txt"
        filename_transcript_txt = f"sn-{formatted_episode}.txt"

         # Duplicate file check
        if os.path.exists(os.path.join(output_directory, filename_transcript_txt)):
            msg_dupe = f"File {filename_transcript_txt} already exists. Skipping.\n"
            log_file_write(msg_dupe, log_path)
            continue  # Skip to the next iteration if identical filename exists
        
        try:
            response = requests.get(url_transcript_txt)
            if response.status_code == 200:
                with open(os.path.join(output_directory, filename_transcript_txt), 'w', encoding='utf-8') as file: # NB: not wb
                    file.write(response.text) # NB: .text not .content
                
                msg_success =f"Successfully downloaded text transcript for {filename_transcript_txt}.\n"
                log_file_write(msg_success, log_path)
                time.sleep(0.5)

            else:
                msg_error = f"Failed to download text transcript for episode {filename_transcript_txt}. Status code: {response.status_code}.\n"
                log_file_write(msg_error, log_path) 
        
        except requests.RequestException as e:
            msg_exception = f"Request failed for {filename_transcript_txt} - {e}\n"
            log_file_write(msg_exception, log_path)