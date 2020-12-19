from random import choice, randint, sample
from time import time

MAX_IN_ONE_MAIL = 5
MAX_TREATS_OF_KIND = 5

FIRST_NAMES = ['Jacek', 'Michal', 'Piotrek', 'Janusz', 'Andrzej', 'Jan', 'Pawel', 'Kasia', 'Malgosia']
SURNAMES = ['Kowalski', 'Przygoda', 'Rutka', 'Olkowski', 'Marczak', 'Poszko', 'Kuntyna', 'Waza']

TREATS = ['zozole','michalki', 'czekolada gorzka','czekolada mleczna','mietusy','rozga', 'wegiel']
COUNTIRES = ['POLAND', 'RUSSIA', 'USA', 'CZECH', 'KIRGISTAN']

# generates mails for elves
def get_mails(number):
    
    MAILS = []

    for i in range(number):
        treats = [] 

        # get random set of candies
        subset = sample(TREATS, randint(1, MAX_IN_ONE_MAIL))

        # how many candy of each kind
        for treat_name in subset:
            treats.append((treat_name, randint(1, MAX_TREATS_OF_KIND)))

        LIST = {
            'country': choice(COUNTIRES), 
            'name': choice(FIRST_NAMES) + ' ' + choice(SURNAMES), 
            'treats': treats
        }
        MAILS.append(LIST)

    return MAILS
