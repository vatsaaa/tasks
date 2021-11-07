from sys import exit
import getopt
from json import loads
import enum

## Project imports
from appexception import AppException


class SecretsStoreType(enum.Enum):
    file = "file"

def usage():
    print("Usage: python3 app.py -c <config_file>")
    print("Usage: python3 app.py -h: Prints this message")

def get_app_config(secrets_store: str, secrets_store_type: str=SecretsStoreType.file) -> dict:
    if secrets_store_type == SecretsStoreType.file:
        with open(secrets_store, "r") as f:
            config = loads(f.read())
    ## TODO: Add code to read config from other types of secrets store      
    else:
        raise AppException("Invalid secrets store type")

    return config

def process_args(args) -> dict:
    try:
        ## Short args are in alphabetical order, long args are in order of appearance of short args
        ## Broker and Celery are separate processes, but their ports & hosts are required for app to run
        opts, args = getopt.getopt(args, "c:h",
                                   [
                                       "config=",
                                       "help"
                                   ])
    except getopt.GetoptError as err:
        ## TODO: Log err to the log file
        print("Fatal Error: Invalid arguments given. For help use python3 app.py --help")
        print(err)
    
    for o, a in opts:
        if o in ("-c", "--config"):
            config = get_app_config(a)
        elif o in ("-h", "--help"):
            usage()
            exit(-1)
        else:
            usage()
            exit(-2)


    return config