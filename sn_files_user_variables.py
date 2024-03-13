############## SECURITY NOW PODCAST FILES: SET USER VARIABLES ##############

""" 
Choose where downloaded Security Now files should be saved.
- Specify a directory path (relative or absolute)
- Supply "." to use the program directory, or a relative directory path i.e. "output/" to create or use a folder called "output" in the program directory.
- Path cannot be None or an empty string.
- Directory will be created if it doesn't exist.
"""

output_directory = r"sn_podcast_files/" # e.g. r"output/"or r"C:\Users\User\Documents\sn_podcast_files\"


""" 
Choose if the program should run with (True) or without (False) a log file.
- Set to False to run this script without a log file.
- True will require log file instanciation for the program to proceed (if an error prevents log_file_setup() from completing, the program will exit).
"""

use_log_file = True # True or False only


""" 
Choose where log files should be saved, if use_log_file = True.
- Specify a directory path (relative or absolute)
- Supply "." to use the program directory, or a relative directory path i.e. "output/" will create or use a folder called "output" in the program directory.
- Path cannot be None or an empty string.
- Directory will be created if it doesn't exist.
"""

path_to_logs = r"." # specify a directory path. Supply "." for program directory, or "/" for root directory. Can be set to output_directory. Do not use None.