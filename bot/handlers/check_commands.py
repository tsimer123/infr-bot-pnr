import re

def split_message(message_text: str) -> str:

    split_message = re.split(r"\s", message_text)    
        
    return split_message

def check_len_command(in_list_command):

    result = False
    list_command = split_message(in_list_command)

    if len(list_command) > 1:
        result = True

    return result

