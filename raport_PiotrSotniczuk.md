---
author: Piotr Sotniczuk
title: ZBD-Zad3 Raport Dla Elfów
geometry: margin=30mm
---

# Wstęp
Witajcie Drogie Elfy,
Składam wam raport dotyczący waszej prośby o wgląd w wasz system pracy. 
Piszę z dobrymi wieściami, ponieważ udało mi się znacząco poprawić prędkość waszej pracy i 
jestem pewny, że w tym roku spokojnie zdążycie przygotować wszystkie prezenty, a św. Mikołaj
wreszcie będzie mógł na dłużej zabawić w każdym domu.

# Diagnostyka Aktualnego Systemu
Aktualnie system działa przede wszystkim zatrważająco wolno. 
Przy 20 elfach co chwila zdarzają się tzw. deadlocki, czyli co najmniej dwa elfy chca naraz dostęp 
do updatu paru słodyczy w spisie magazynu, ale zabrali sobie nawzajem brakujące elementy.
Ta sytuacja powoduje długie zawieszenie 
systemu na próbie zrobienia 'update'. Jest to przyczyna tak wolno działającej bazy.
System generuje wtedy także błąd, a pewne dziecko nie dostanie prezentu.
Dziecko nie dostanie prezentu również, gdy wystąpi błąd ujemnej liczby elementów w magazynie.
To dzieje się, gdy zaczyna brakować pewnego słodycza, a naraz dwóch elfów próbuje go zapakować.

# Zgubne pomysły
Niektóre elfy z zarządu (wcale nie ja) próbując poprawić działanie fabryki uciekały się do 
dziwnych pomysłów dających mierne rezultaty. 

## UPDATE na końcu transakcji
Jednym pomysłem było zapisanie wszystkich
updatów odnośnie paczki na kartce elfa, a dopiero na końcu transakcji wpisanie ich do spisu.
Taki pomysł dawał nieznaczną poprawę wydolności systemu. 

## SERIALIZACJA
Innym pomysłem była zmiana izolacji pracy z READ_COMMITED na REAPEATABLE_READ lub SERIALIZABLE.
Jednak wtedy zaczęły pojawiać się problemy z ułożeniem transakcji "ERROR:  could not serialize access", a
deadlocki wcale nie znikały. Jednak problem z serializacją można naprawić próbując jeszcze raz lub do skutku.

W przypadku do 5 prób był wysyłany już co drugi list, a czas pracy był podobny jak nie lepszy.

W przypadku do 10 prób było wysyłane około 75% listóœ, ale czas był dwukrotnie gorszy.

Przy próbie do skutku rzeczywiście każdy list byłby wysłany, lecz czas wykonania możnaby szacować na
święta 2050, a serwerownia byłaby tak rozgrzana, że z bieguna północnego zrobiłyby się Hawaje. 

# Rozwiązanie
Skoro największym problemem są deadlocki to je należy rozwiązać najpierw.
Proponuję ustalić kolejność rezerwowania dostępu do spisu słodyczy np. według kolejności alfabetycznej.
Teraz elfy nie będą w stanie się zdeadlockować. Zauważmy, że są tu możliwe 2 poziomy izolazji do 2 różnych celi:

## SERIALIZABLE lub REPEATABLE_READ
W tym rozwiązaniu nie dojdzie do zmniejszenia elementów magazynie, poniżej zera lecz dosyć dużym kosztem.
Błędy serializacji spowodują mocne spowolnienie procesu, gdyż wiele transakcji będzie trzeba powtórzyć, a 
niekóre mogą być tak dotkliwe, że powtarzanie nie pomoże przez co skuteczność metody to około 90% listów.
Zauważmy, że przy tym poziomie izolazji problemem nie są jedynie updaty, ale również selecty. Nie jesteśmy w stanie
posortować takiego dostępu nie blokując całej bazy. To powoduje błędy serializacji.

## READ_COMMITTED
Czy napewno potrzebujemy takiej izolacji? Trochę tak, ale nie koniecznie.
Nie jesteśmy w stanie kontrolować, czy przez naszą transakcję liczba elementów w magazynie spadnie poniżej zera, ale jeśli tak się stanie,
to wystarczy powtórzyć daną transakcję. Nowa próba już wie, że nie starczy elementów, więc ten błąd się nie powtórzy.
Skuteczność tego rozwiązania to 100%, a liczba powtórzonych transakcji znikoma. To wszystko razem z niskim poziomem
izolacji daje niespotykany wynik czasowy. Jedyne dostęp, który musimy w tym wypadku sortować to dostęp do updata.
W takim razie najlepiej, żeby elf najpierw patrząc na stan magazynu zapisał sobie ile czego zamierza wziąć, a na sam koniec transakcji
posortował sobie te słodycze alfabetycznie i zrobił updaty na bazie.

# Ahhh te leniwe elfy
Doszły mnie słuchy, że wśród elfów znajdują sie leniuchy i prosiliście mnie o pewne rozwiązanie.
Moje rozwiązanie jest niezłe, ale niestety są miejsca gdzie leniwy elf spowoduje opóźnienia.
Jeśli adwersarz pójdzie na przerwę zablokuje każdy słodycz w spisie, na którym zrobił update, ale nie zakomitował.
W początkowym rozwiązaniu ten wrażliwy moment ciągnie się od spakowania pierwszego słodycza do commita.
W moim rozwiązaniu updaty są tuż przed commitem, więc adwersarz musiałby zrobić przerwę właśnie w tym miejscu.
Możnaby z tym walczyć np. zmuszając leniwe elfy do drzemki przed updatem lub stawiając dozorcę pilnującego, aby elf 
bezzwłocznie po dokananiu updatów spróbował zakomitować zmiany.













Początkowo read_commited: 
20 workerow kazdy po 10 listow
-deadlock on update in_magazine
-new row 

-około 25% sie udaje reszta error
-okolo 0.13-0.24 TR/SEKs


Update na koncu:
-skutecznosc 35%
-okolo 0.16-0.4

Serializacja do upadlego:
-0.028-0.036

Serializacja maks 5 razy BEST
- 52%-56%
- 0.3- 0.7


trzeba powtarzac
albo i=10
144
72% 
0.2-0.2
153/29sek

kurwa tak posortowane
5.9 sekundy 83%

najlepiej read_commited XD
