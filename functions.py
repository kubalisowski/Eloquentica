from models import *
import ast

###Convertions###
def resultproxy_to_dict(search):
    d, a = {}, []
    for resultproxy in search:
        for tup in resultproxy.items():
            d = {**d, **{tup[0]: tup[1]}}
            a.append(d)
        # Returning last element from list as it returns redundant data
        a = a[-1]
        return a

# Add commas to string with word_ids -> for proper query formatting
def add_comma(strr):
    strr = strr.strip()
    strr = strr.replace(' ', ',')
    return strr


# Resultproxy object to string representation of list -> converted to list in extract_synonyms()
def resultproxy_to_list(listt):
    return ["%s" % v for v in listt]


# Remove redundant characters (i.e. for group_of_synonyms query)
# Non <list> object
def extract_values(listt):
    t = str.maketrans({'[': '', ']': '', '\'': '', '(': '', ')': '', ',': ''})
    listt = listt.translate(t)
    return listt

# <list> object
def extract_values_2(listt):
    a = []
    for l in listt:
        t = str.maketrans({'(': '', ')': '', ',': '', '\'': ''})
        l = l.translate(t)
        a.append(l)
    return a

# Sort values -> create lists of items within list ([[item1,item2], [item1,item2]]) for word_list_to_dict() function
def sort_values(listt):
    a = []
    for l in listt:
        x = l.split(' ')
        a.append(x)
    return a


###OnWords###
# word_id to be used in query: select_words_from_synonym
def extract_word_id(dicts):
    a = []
    for d in dicts:
        a.append(str(d['word_id']))
    a = str(a)
    t = str.maketrans({'[': '', ']': '', '\'': '', ' ': ''})
    a = a.translate(t)
    return a


def word_list_to_dict(listt):
    a = []
    keys = ['word_id', 'word', 'definition', 'added_by_user_id']
    for l in listt:
        l = dict(zip(keys, l))
        a.append(l)
    return a


def word_list_to_dict_2(listt):
    a = []
    keys = ['word_id', 'synonym']
    for l in listt:
        l = dict(zip(keys, l))
        a.append(l)
    return a


###OnSynonyms###
# Returns list of synonyms
def trash_remove(strr):
    strr = strr.split(',')
    a = []
    for s in strr:
        if s.isspace() is False:
            a.append(s)
        else:
            continue

    while '' in a : a.remove('')

    aa = []
    for s in a:
        s = s.strip()
        aa.append(s)

    return aa

def synonyms_add_db(new_word_id, synonyms):
    for s in synonyms:
        s = s.lower()
        add_synonym = Synonyms(word_id=new_word_id, synonym=s)
        db.session.add(add_synonym)
        db.session.commit()


# List of strings to list (from resultproxy_to_list()
def extract_synonyms(synonym_list):
    a = []
    for x in synonym_list:
        t = str.maketrans({'(': '', ')': '', '\'': '', ',': ''})
        x = x.translate(t)
        a.append(x)
    return a


# Synonyms for all words for search_synonym.html
def group_synonym(var):
    a = []
    for v in var:
        a.append(v['word_id'])
    return a


def tuple_to_list(listt):
    a = []
    for l in listt:
        t = str.maketrans({'(': '[', ')': ']'})
        l = l.translate(t)
        l = ast.literal_eval(l)
        a.append(l)
    return a


def synonym_list_to_dict(listt):
    a = []
    keys = ['synonym_id', 'word_id', 'synonym']
    for l in listt:
        l = dict(zip(keys, l))
        a.append(l)
    return a
