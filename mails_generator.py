from random import choice, randint, sample
from time import time


def get_mails(number):

    #start = time()
    # for 1000 mail about 200ms
    MAX_IN_ONE_MAIL = 5
    MAX_TREATS_OF_KIND = 5

    FIRST_NAMES = ['Jacek', 'Michal', 'Piotrek', 'Janusz', 'Andrzej', 'Jan', 'Pawel', 'Kasia', 'Malgosia']
    SURNAMES = ['Kowalski', 'Przygoda', 'Rutka', 'Olkowski', 'Marczak', 'Poszko', 'Kuntyna', 'Waza']

    TREATS = ['zozole','michalki', 'czekolada gorzka','czekolada mleczna','mietusy']

    COUNTIRES = ['POLAND', 'RUSSIA', 'USA', 'CZECH', 'KIRGISTAN']

    MAILS = []

    for i in range(number):
        treats = [] 
        subset = sample(TREATS, randint(1, MAX_IN_ONE_MAIL))
        for treat_name in subset:
            treats.append((treat_name, randint(1, MAX_TREATS_OF_KIND)))

        LIST = {
            'country': choice(COUNTIRES), 
            'name': choice(FIRST_NAMES) + ' ' + choice(SURNAMES), 
            'treats': treats
        }
        MAILS.append(LIST)

    #print(MAILS)
    #print('time: ', (time() - start) * 1000, ' ms')
    return MAILS

#print(get_mails(10))