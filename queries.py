search_word = '''SELECT *
FROM Words W 
LEFT JOIN Synonyms S
ON S.word_id = W.word_id
WHERE W.word LIKE "{}"
'''

search_word_id = '''SELECT word_id
FROM Words
WHERE word like "{}"'''

synonyms_from_word_id = '''SELECT synonym
FROM Synonyms
WHERE word_id = {}'''

# Searching words from synonym
select_words_from_synonym = '''SELECT *
FROM Words
WHERE word_id IN ({})'''

# Word exist in db, for search_word.html
search_synonyms = '''SELECT synonym FROM Synonyms WHERE word_id = {}'''

# Word not exist in db, for search_synonym.html
search_synonym = '''SELECT * 
FROM Synonyms
WHERE synonym LIKE "{}"
'''

# For search_synonyms.html -> synonyms for all found words
group_of_synonyms = '''SELECT word_id, synonym
FROM Synonyms
WHERE word_id IN ({})'''

# Reset Primary Key
pk_reset = '''UPDATE SQLITE_SEQUENCE SET SEQ=0 WHERE NAME="table_name"'''