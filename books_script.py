'''
books_script.py will hit the google books API to collate the data necessary
to build some basic metrics about various searches
author: jowens
'''
 
import sys
import requests
import argparse

from dateutil.parser import parse
from datetime import date
from terminal_table import Table
from ansi_colours import AnsiColours as Colour

# CONSTANTS
API_URL = 'https://www.googleapis.com/books/v1/volumes'
SECRET  = 'AIzaSyBKFOVhps_PAJaA5mq9n440F_ILdj8BCMM'
AUTH = '&key=' + SECRET
QUERY = '?q='
TITLE = '+intitle:'
AUTHOR = '+inauthor:'
PUB = '+inpublisher:'
SUB = '+subject:'
START = '&startIndex='
MAXRES = '&maxResults='

_SEARCH_ARGVAR = 'search_term'
MAX_RESULTS = 40

 
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

def get_results(q_args):
    '''first iteration results'''
    this_set = None
    try:
        this_set = requests.get(format_query(q_args)).json()
    except:
        _print_error('unable to get json from api response')
        return None
    return this_set if this_set['totalItems'] <= q_args[MAXRES] else get_more_results(q_args, this_set)

def get_more_results(q_args, r):
    '''paginate with google to pull all of the resutls'''
    if r is None:
        _print_error('error retrieving first set')
    if 'totalItems' in r:
        while q_args[START] < r['totalItems']:
            q_args[START] += q_args[MAXRES]
            query_url = format_query(q_args)
            result = requests.get(query_url)
            try:
                result = result.json()
            except:
                _print_error('unable to get json from api response starting from index: ' + str(q_args[START]))
            if 'items' in result:
                r['items'].extend(result['items'])
            else:
                _print_error('no items retreived from api. query url: ' + query_url)
    return r

def analyze_results(r):
    '''built top level metrics for the results from the api'''
    if 'items' in r:
        authors = {}
        analyzed = {
                'maxDate':date.min,
                'minDate':date.today(),
                'author' :None,
        }

        for item in r['items']:
            if 'publishedDate' in item['volumeInfo']:
                pubDate = parse(item['volumeInfo']['publishedDate']).date()
                if pubDate > analyzed['maxDate']:
                    analyzed['maxDate'] = pubDate
                elif pubDate < analyzed['minDate']:
                    analyzed['minDate'] = pubDate

            # if the author doesn't exist, initialize it to zero
            # add one to whatever is returned from get()
            if 'authors' in item['volumeInfo']:
                for author in item['volumeInfo']['authors']:
                    authors[author] = authors.get(author, 0) + 1
        
        top_author = max(authors, key=authors.get)
        analyzed['author'] = (top_author, authors[top_author])
        return analyzed

def display(results):
    '''loop until the user is done scoping out their books'''
    viewing = True
    items = results['items']
    index = 0
    display_num = 10

    # main loop
    while viewing:
        table_content = [] 
        end_index = len(items) if index+display_num > len(items) else index+display_num
        
        # format results for viewing 
        for i in range(index, end_index):
            authors = 'no authors provided'
            title = 'no title provided'
            if 'authors' in items[i]['volumeInfo']:
                authors = ', '.join(items[i]['volumeInfo']['authors'])
            if 'title' in items[i]['volumeInfo']:
                title = items[i]['volumeInfo']['title']
            table_content.append( (i, authors, title) )

        table = Table.create(
            table_content,
            ("ID", "Author(s)", "Title"),
            header_colour=Colour.cyan,
            column_colours=(Colour.green,)
        )
        print(table)
        holding=True

        # secondary loop for user input
        while holding:
            user_input = input(
                    "Select an index above for more information, type 'back' or 'b' for the previous ten results, or just hit <enter> for the next ten results"
                    + "\n"
                    +"To quit, type 'quit' or 'q'"
                    +"\n"
            )

            # enum schmenum, ifs for days!
            # i considered refactoring this to an await_input() method
            # this works cleanly, and is quite legible. sticking with it.
            if not user_input:
                index=index+display_num
                if index > len(items):
                    index=0
                holding=False
                break
            elif user_input is 'b' or user_input is 'back':
                index=index-display_num
                if index < 0:
                    index=len(items)-display_num
                holding=False
                break
            elif user_input is 'q' or user_input is 'quit':
                holding=False
                viewing=False
                break
            elif user_input.isdigit() and int(user_input) in range(index,index+display_num):
                selection = items[int(user_input)]['volumeInfo']
                if 'description' in selection:
                    print(selection['description'])
                else:
                    print('no description for this volume')
            else:
                print('that entry was invalid. please try again.')


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
            QUERY   : args[_SEARCH_ARGVAR],
            TITLE   : args['intitle'],
            AUTHOR  : args['inauthor'],
            PUB     : args['inpublisher'],
            SUB     : args['subject'],
            START   : startIndex,
            MAXRES  : MAX_RESULTS
            }

    # pull results out of the api
    results = get_results(query_args) 
    
    # compare expected results to actual
    num_res_expected = results['totalItems']
    num_res_actual = len(results['items'])
    print('expected ' + str(num_res_expected) + ' results')
    print('successfully retreived ' + str(num_res_actual))
    
    # quick analysis on all results
    analysis = analyze_results(results)
    print('results span from ' + analysis['minDate'].isoformat() + ' to ' + analysis['maxDate'].isoformat())
    print('in this timeframe, ' + analysis['author'][0] + ' contributed the most works: ' + str(analysis['author'][1]))

    # loop over results for inspection
    display(results)

    return 0
 
if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
