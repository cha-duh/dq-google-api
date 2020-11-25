'''
books_script.py will hit the google books API to collate the data necessary
to build some basic metrics about various searches
author: jowens
'''
 
import sys
import requests
import argparse

# CONSTANTS
API_URL = 'https://www.googleapis.com/books/v1/volumes'

# vars
parameters = dict(q='')
startIndex = 0
search = ''  
results = '' 
responseTime = 0
maxDate = None
minDate = None
mostProlific = ''

_STERM_ARGVAR = 'search_term'
 
def _parse_args(argv):
    ''' Parses args into a dict of ARGVAR=value, or None if the argument wasn't supplied '''
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    # TODO Add arguments here, e.g.:
    # parser.add_argument(_SAMPLE_ARGVAR, metavar="<sample>", help="This variable is a sample variable")
    parser.add_argument(_STERM_ARGVAR, metavar="<search>", help="Your search term(s)"
    return vars(parser.parse_args(argv))
 
def _print_error(msg):
    sys.stderr.write('Error: ' + msg + '\n')
 
def _validate_args(args):
    ''' Performs validation on the given args dict, returning a non-zero exit code if errors were found or None if all is well '''
    if args[_STERM_ARGVAR] is None:
        return "You must supply a search term."
    return None
 
def main(argv):
    args = _parse_args(map(str, argv))
    err = _validate_args(args)
    if err is not None:
        return err
 
    
 
    return 0
 
if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
