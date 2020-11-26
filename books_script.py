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
SECRET  = 'AIzaSyBKFOVhps_PAJaA5mq9n440F_ILdj8BCMM'
_SEARCH_ARGVAR = 'search_term'

# result vars
results = {}
responseTime = 0
maxDate = None
minDate = None
mostProlific = ''

 
def _parse_args(argv):
    ''' Parses args into a dict of ARGVAR=value, or None if the argument wasn't supplied '''
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(_SEARCH_ARGVAR, metavar="<search>", help="Your search term(s)")
    parser.add_argument('-t', '--intitle', help="filter books by keywords contained in the title")
    parser.add_argument('-a', '--inauthor', help="filter books by keywords contained in the author")
    parser.add_argument('-p', '--inpublisher', help="filter books by keywords contained in the publisher")
    parser.add_argument('-s', '--subject', help="filter books by keywords in theb book subject or category list")
    return vars(parser.parse_args(argv))
 
def _print_error(msg):
    sys.stderr.write('Error: ' + msg + '\n')
 
def _validate_args(args):
    ''' Performs validation on the given args dict, returning a non-zero exit code if errors were found or None if all is well '''
    if args[_SEARCH_ARGVAR] is None:
        return "You must supply a search term."
    return None

def format_request(query, start, maxRes):
    '''compiles a request from a few simple components'''
    
    
 
def main(argv):
    args = _parse_args(map(str, argv))
    err = _validate_args(args)
    if err is not None:
        return err
 
    # pull arg vals out of args
    search_term = args[_SEARCH_ARGVAR]
    intitle = args.intitle
    inauthor = args.inauthor
    inpublisher = args.inpublisher
    subject = args.subject
    query_args = [search_term, intitle, inauthor, inpublisher, subject]

    # establish a starting point
    startIndex = 0
    maxResults = 40



    

    return 0
 
if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
