import os
import inspect

caller_frame = inspect.stack()[0]
caller_file_path_full = os.path.abspath(caller_frame.filename)
caller_file_path_short = caller_file_path_full[:-3]
extension = '.csv'
filename = (f'{caller_file_path_short}+{extension}')

print(caller_file_path_full)
print(caller_file_path_short)
print(filename)