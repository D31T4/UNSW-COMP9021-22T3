# COMP9021 22T3
# Assignment 1 *** Due Monday 24 October (Week 7) @ 9.00am

# DO *NOT* WRITE YOUR NAME TO MAINTAIN ANONYMITY FOR PLAGIARISM DETECTION

from roman_converter import RomanNumeral, GeneralizedRomanNumeral
from min_roman import minimalArab
from input_parser import parseUserInput

TaskNotFound = "I don't get what you want, sorry mate!"
TaskImpossible = "Hey, ask me something that's not impossible to do!"

def please_convert():
    args = parseUserInput(input('How can I help you? '))
    
    if args[0] == 1:
        try:
            print(f'Sure! It is {RomanNumeral.toArab(args[1])}')
        except:
            print(TaskImpossible)

    elif args[0] == 2:
        try:
            assert not args[1].startswith('0')
            print(f'Sure! It is {RomanNumeral.toRoman(int(args[1]))}')
        except:
            print(TaskImpossible)

    elif args[0] == 3:
        try:
            print(f'Sure! It is {GeneralizedRomanNumeral(args[2]).toArab(args[1])}')
        except:
            print(TaskImpossible)

    elif args[0] == 4:
        try:
            assert not args[1].startswith('0')
            print(f'Sure! It is {GeneralizedRomanNumeral(args[2]).toRoman(int(args[1]))}')
        except:
            print(TaskImpossible)

    elif args[0] == 5:
        try:
            value, numerals = minimalArab(args[1])
            print(f'Sure! It is {value} using {numerals}')
        except:
            print(TaskImpossible)

    else:
        print(TaskNotFound)

    # EDIT AND COMPLETE THE CODE ABOVE



# DEFINE OTHER FUNCTIONS

please_convert()
