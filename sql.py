from flask import render_template, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from config import *
from forms import *
from models import *
from queries import *
from functions import *


def xindex():
    loginform = LoginForm()

    if loginform.validate_on_submit():
        user = User.query.filter_by(username=loginform.username.data).first()
        if user:
            if check_password_hash(user.password, loginform.password.data):
                login_user(user, remember=loginform.remember.data)
                return redirect(url_for('dashboard'))
            return render_template('err_login.html', loginform=loginform)
    return render_template('index.html', loginform=loginform)


def xaddword():
    searchform = SearchForm()
    addform = AddForm()

    if addform.validate_on_submit():
        new_word_check = db.engine.execute(search_word.format(addform.word.data.strip()))
        new_word_check = resultproxy_to_dict(new_word_check)

        if bool(new_word_check) is False:
            user_id = current_user.get_id()
            # Word + definition trimming
            var_word = addform.word.data.strip()
            var_word = var_word.lower()
            var_definition = addform.definition.data.strip()
            var_definition = var_definition.lower()
            # SQLalchemy object
            new_word = Words(word=var_word, definition=var_definition, added_by_user_id=user_id)
            # String of synonyms from addword form
            synonyms_string = str(addform.synonym.data)
            # Add new word + definition to db
            db.session.add(new_word)
            db.session.commit()
            # Check id of new added word
            new_word_id = db.engine.execute(search_word_id.format(addform.word.data))
            new_word_id = resultproxy_to_list(new_word_id)
            new_word_id = extract_values(str(new_word_id))
            # Add synonyms to db
            new_synonyms = trash_remove(synonyms_string)
            new_synonyms = synonyms_add_db(new_word_id, new_synonyms)

            return render_template('addword_ok.html', addform=addform, searchform=searchform)
        else:
            return render_template('word_exist.html', addform=addform, searchform=searchform)

    if searchform.validate_on_submit():
        return xdashboard()

    return render_template('addword.html', addform=addform, searchform=searchform)


def xdashboard():
    searchform = SearchForm()

    if searchform.validate_on_submit():
        word_check = db.engine.execute(search_word.format(searchform.search.data.strip()))
        word_check = resultproxy_to_dict(word_check)
        # If word not exist
        if bool(word_check) is False:
            synonym_check = db.engine.execute(search_synonym.format(searchform.search.data))

            if bool(synonym_check) is True:
                synonym_check = resultproxy_to_list(synonym_check)
                synonym_check = tuple_to_list(synonym_check)
                # Data from Synonyms table as dict
                synonym_check = synonym_list_to_dict(synonym_check)
                # Word ID's extraction of words assigned to searched synonym
                synonym_check_word_id = extract_word_id(synonym_check)
                # Search all words assigned to searched synonym (new variable name is more suggestive about its destiny)
                all_words = db.engine.execute(select_words_from_synonym.format(synonym_check_word_id))
                # Results convertions -> dict of related words needed as final result
                all_words = resultproxy_to_list(all_words)
                all_words = extract_values_2(all_words)
                all_words = sort_values(all_words)
                all_words = word_list_to_dict(all_words)

                # Group synonyms for particular words: variable -> synonyms_in_groups, def -> group_synonym
                synonyms_in_groups = str(group_synonym(synonym_check))
                # Remove redundant characters (i.e. for group_of_synonyms query)
                synonyms_in_groups = extract_values(synonyms_in_groups)
                # Add comma to word_ids
                synonyms_in_groups = add_comma(synonyms_in_groups)
                # Select all synonyms for all related words
                synonyms_in_groups = db.engine.execute(group_of_synonyms.format(synonyms_in_groups))
                # Convert ResultProxy object to list
                synonyms_in_groups = resultproxy_to_list(synonyms_in_groups)
                # Remove redundant characters (i.e. '(' )
                synonyms_in_groups = extract_values_2(synonyms_in_groups)
                # Convert string representation of list to list
                synonyms_in_groups = sort_values(synonyms_in_groups)
                synonyms_in_groups = word_list_to_dict_2(synonyms_in_groups)
                ############################################################
                # Data display rules defined in search_synonym.html
                return render_template('search_synonym.html', searchform=searchform, synonyms_in_groups=synonyms_in_groups, all_words=all_words)
            else:
                return render_template('err_search.html', searchform=searchform)
        # If word exist
        else:
            synonyms = db.engine.execute(search_synonyms.format(str(word_check['word_id'])))
            synonyms = resultproxy_to_list(synonyms)
            synonyms = extract_synonyms(synonyms)
            return render_template('search_word.html', word_check=word_check, synonyms=synonyms, searchform=searchform)

    return render_template('dashboard.html', searchform=searchform)

def xregister():
    registerform = RegisterForm()

    if registerform.validate_on_submit():
        hashed_password = generate_password_hash(registerform.password.data, method='sha256')
        new_user = User(username=registerform.username.data, password=hashed_password, email=registerform.email.data)
        db.session.add(new_user)
        db.session.commit()
        return render_template('register_ok.html', registerform=registerform)
    return render_template('register.html', registerform=registerform)

def xinfo():
    searchform = SearchForm()

    if searchform.validate_on_submit():
        return xdashboard()

    return render_template('info.html', searchform=searchform)
