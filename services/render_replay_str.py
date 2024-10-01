import sys
from datetime import datetime

def print_format_log_cmd(list_param, type, message):
    
    print(str(datetime.now()) + ", " +
            str(list_param[0]) + ", " +
            type + " " +
            str(list_param[1]) + ", " +
            str(list_param[2]) + ", " +
            str(list_param[3]) + ", " +
            str(list_param[4]) + ", " +
            str(message), file=sys.stdout)
    