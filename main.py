"""
Hoofdbestand Heuristieken

Linsey Schaap (11036109), Kenneth Goei (11850701), Nadja van 't Hoff (11030720)
"""
import os, sys
import csv
import math

# intialiseer paden naar andere klasses en algoritmes
directory = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(directory, "Code"))
sys.path.append(os.path.join(directory, "Code", "Classes"))
sys.path.append(os.path.join(directory, "Code", "Algoritmes"))

import student as StudentKlasse
import vak as VakKlasse
import zaalSlot as ZaalSlotKlasse

# initialiseer lijsten voor data
studentenLijst = []
vakkenLijst = []
vanVakNaarId = {}
rooster = []

# dagen dat er les wordt gegeven
lesdagen = ["maandag", "dinsdag", "woensdag", "donderdag", "vrijdag"]

# dict om id van tijdsloten om te zetten naar tijd
idNaarTijdslot = {1 : "9:00-11:00", 2 : "11:00-13:00", 3: "13:00-15:00", 4: "15:00-17:00", 5: "17:00-19:00"}

def main():

    # lees de data in de datasructuur in
    initialiseer()

    # voeg vakken aan het rooster toe
    i = 0
    for activiteit in activiteitenLijst:
        toevoegen(rooster[i], activiteit)
        i += 1

    # opstellen van lijst met ingeroosterde activiteiten
    zalenInGebruik = ingeroosterdLijst(rooster)

    # berekenen van de puntenscore
    score = scoreFunctie(vakkenLijst, activiteitenLijst, zalenInGebruik, studentenLijst)

    print(score)


def ingeroosterdLijst(rooster):
    """ opstellen van lijst met ingeroosterde activiteiten"""

    # voeg elk ingeroosterde combinatie van tijdslot en zaal aan lijst toe
    zalenInGebruik = []
    for zaalslot in rooster:
        if zaalslot.inGebruik == 1:
            zalenInGebruik.append(zaalslot)

    return zalenInGebruik

def initialiseer():
    """ Leest de data in en maakt de benodigde lijsten."""

    # aanmaken van dict en vakkenlijst creëren
    teller = 0

    # inlezen van CSV bestand van vakken
    with open('Data/vakken.csv') as csvBestand:
        leesCSV = csv.reader(csvBestand, delimiter=';')
        next(leesCSV, None)

        # rijen van CSV inlezen en vakobject aanmaken
        for rij in leesCSV:
            # nvt naar "oneindig zetten"
            if rij[3] == 'nvt':
                rij[3] = 1000
            if rij[5] == 'nvt':
                rij[5] = 1000

            vakkenLijst.append(VakKlasse.Vak(teller, rij[0], int(rij[1]), int(rij[2]), int(rij[3]), int(rij[4]), int(rij[5])))
            vanVakNaarId[rij[0]] = teller
            teller += 1

    # inlezen van CSV bestand van studenten
    with open('Data/studentenenvakken.csv', 'r', encoding="latin-1") as csvBestand:
        leesCSV = csv.reader(csvBestand, delimiter=",")
        next(leesCSV, None)

        # leest bestand en creeert studenten
        for rij in leesCSV:
            studentVakken = []
            for vak in rij[3:]:
                if vak != "":
                    studentVakken.append(vak)
            studentenLijst.append(StudentKlasse.Student(rij[0], rij[1], rij[2], studentVakken))

    # vakken in studentenlijst met id voorzien
    for student in studentenLijst:
        tijdelijk = []
        for vak in student.vakken:
            tijdelijk.append(vanVakNaarId[vak])
        student.vakken = tijdelijk

    # aantal studenten per vak vastleggen
    for vak in vakkenLijst:
        for student in studentenLijst:
            if vak.id in student.vakken:
                vak.studenten.append(student.studentnummer)
        vak.aantalStudenten = len(vak.studenten)

    # leest bestand en creert zaalsloten
    with open('Data/zalen.csv') as csvBestand:
        leesCSV = csv.reader(csvBestand, delimiter=';')
        next(leesCSV, None)
        # leest elke zaal en maakt per dag en tijdslot een zaalslot
        for rij in leesCSV:
            for dag in lesdagen:
                for i in range(1, len(idNaarTijdslot)):
                    rooster.append(ZaalSlotKlasse.ZaalSlot(rij[0], int(rij[1]), dag, i))

        # voeg zaalsloten toe voor het laatste tijdslot 17.00-19.00
        for dag in lesdagen:
            rooster.append(ZaalSlotKlasse.ZaalSlot("C0.110", 110, dag, 5))


def zaalgrootteConflict(zaalslotLijst):
    "deze functie berekent de maluspunten voor te kleine zalen"

    malusPunten = 0

    # itereer over alle zalen
    for zaalslot in zaalslotLijst:

        # bekijk of er meer studenten zijn dan capaciteit van de zaal
        verschil = zaalslot.capaciteit - zaalslot.activiteit.nrStud

        # keer maluspunten uit aan studenten die niet in zaal passen
        if verschil < 0:
            malusPunten = malusPunten  - verschil

    # geef het aantal maluspunten terug
    return malusPunten


def vakSpreiding(vakkenLijst, activiteitenLijst):
    "deze functie berekent de punten voor de spreiding van de activiteiten"

    malusPunten = 0

    # itereer over ieder vak
    for vak in vakkenLijst:

        # onthoud op welke dagen activiteiten zijn geroosterd
        verdeeldAantalDagen = 0
        dag = []

        # itereer over alle activiteiten
        for activiteit in activiteitenLijst:

            # controleer of alle activiteiten overeen komen met hetzelfde vak
            if activiteit.vakId == vak.id:

                # voeg nieuwe dag toe wanneer activiteit op andere dag
                if activiteit.dag not in dag:
                    dag.append(activiteit.dag)
                    verdeeldAantalDagen += 1

        # bepaal aantal activiteiten van het vak
        aantalActiviteiten = vak.hc + vak.wc + vak.prac

        # bepaal op hoeveel dagen de activiteiten zijn verdeeld
        x = aantalActiviteiten - verdeeldAantalDagen

        # bereken maluspunten
        malusPunten = malusPunten + x * 10

    # geef het aantal maluspunten terug
    return malusPunten


def roosterConflicten(studentenLijst, zaalslotLijst):
    "deze functie berekent de punten bij roosterconflicten per student"

    malusPunten = 0

    # itereer over iedere student
    for student in studentenLijst:

        # lijst om iedere activiteit op te slaan
        tijdslotenStudent = []

        # itereer over alle zalen
        for zaalslot in zaalslotLijst:

            # controleer in welke zaal de student voorkomt
            if student.studentnummer in zaalslot.activiteit.welkeStud:

                # voeg de activiteit toe mits tijd en dag nog niet voorkomt
                dagtijd = [zaalslot.dag, zaalslot.tijdslot]
                if dagtijd not in tijdslotenStudent:
                    tijdslotenStudent.append(dagtijd)

                # voeg maluspunt toe als de dag en tijd al voorkomt
                else:
                    malusPunten += 1

    # geef het aantal maluspunten terug
    return malusPunten


def extraTijdslot(studentenLijst, zaalslotLijst):
    "deze functie berekent de punten bij het gebruik van het extra tijdslot"

    malusPunten = 0

    # kijkt of zaal in tijdslot 5 (17.00-19.00) wordt gebruikt
    for zaal in zaalslotLijst:
        if zaal.tijdslot == 5 and zaal.inGebruik == 1:
            malusPunten += 50

    # geef het aantal maluspunten terug
    return malusPunten


def scoreFunctie(vakkenLijst, activiteitenLijst, zaalslotLijst, studentenLijst):
    "deze functie berekent de score van een rooster"

    malusPunten = vakSpreiding(vakkenLijst, activiteitenLijst) + zaalgrootteConflict(zaalslotLijst) + roosterConflicten(studentenLijst, zaalslotLijst) + extraTijdslot(studentenLijst, zaalslotLijst)
    score = 1000 - malusPunten

    return score

def vakkenIngeroosterd():
    """ Controleert of alle vakken zijn ingeroosterd."""

    # controleert of een activiteit nog niet is ingeroosterd aan de had van tijdslot 0
    for activiteit in activiteitenLijst:
        if activiteit.tijdslot == 0:
            print("Niet alle vakken zijn ingeroosterd")
            return False
    return True

if __name__ == "__main__":
    main()
