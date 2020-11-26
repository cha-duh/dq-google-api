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
AUTH = '&key=' + SECRET

_SEARCH_ARGVAR = 'search_term'
MAX_RESULTS = 40

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

def format_query(q_args):
    '''compiles a request from a few simple components'''
    query = API_URL
    for key in q_args:
        if q_args[key]:
            query += key + str(q_args[key])
    query += AUTH
    return query

def main(argv):
    args = _parse_args(map(str, argv))
    err = _validate_args(args)
    if err is not None:
        return err

    print(args)

    # establish a starting point
    startIndex = 0

    # pull arg vals out of args
    query_args = {
            '?q=' : args[_SEARCH_ARGVAR],
            '+intitle:' : args['intitle'],
            '+inauthor:': args['inauthor'],
            '+inpublisher:' : args['inpublisher'],
            '+subject:' : args['subject'],
            '&startIndex=': startIndex,
            '&maxResults=': MAX_RESULTS
            }


    # results = {}
    q = format_query(query_args)
    r = requests.get(q)
    content = {}
    try :
        content = r.json()
    except :
        _print_error('unable to get json from the api response')
    
    print(content)
    return 0
 
if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
