# COMP9021 22T3
# Quiz 3 *** Due Friday Week 5 @ 9.00pm
#        *** Late penalty 5% per day
#        *** Not accepted after Monday Week 6 @ 9.00pm

# DO *NOT* WRITE YOUR NAME TO MAINTAIN ANONYMITY FOR PLAGIARISM DETECTION


# Prompts the user for an arity (a natural number) n and a word.
# Call symbol a word consisting of nothing but alphabetic characters
# and underscores.
# Checks that the word is valid, in that it satisfies the following
# inductive definition:
# - a symbol, with spaces allowed at both ends, is a valid word;
# - a word of the form s(w_1,...,w_n) with s denoting a symbol and
#   w_1, ..., w_n denoting valid words, with spaces allowed at both ends and
#   around parentheses and commas, is a valid word.


import sys

from token_checker import stringIsValid

def is_valid(word, arity):
    return stringIsValid(word, arity)


try:
    arity = int(input('Input an arity : '))
    if arity < 0:
        raise ValueError
except ValueError:
    print('Incorrect arity, giving up...')
    sys.exit()

word = input('Input a word: ')

if is_valid(word, arity):
    print('The word is valid.')
else:
    print('The word is invalid.')

