import student
import vak
import zaal
import copy

studentenLijst = student.studentenLijst
vakkenLijst = vak.vakkenlijst

def main():

    # dict om id van tijdsloten om te zetten naar tijd
    idNaarTijdslot = {1 : "9:00-11:00", 2 : "11:00-13:00", 3 : "15:00-17:00", 4 : "17:00-19:00"}

    # dict met alle zalen per dag
    dag = {1 : zaal.zaalLijst[:], 2 : zaal.zaalLijst[:], 3 : zaal.zaalLijst[:], 4 : zaal.zaalLijst[:]}

    # rooster
    rooster = {"maandag" : copy.deepcopy(dag), "dinsdag" : copy.deepcopy(dag), "woensdag" : copy.deepcopy(dag), "donderdag" : copy.deepcopy(dag), "vrijdag" : copy.deepcopy(dag)}

    for persoon in studentenLijst:
        temp = []
        for college in persoon.vakken:    
            temp.append(vak.vanVakNaarId[college])
        persoon.vakken = temp
   
    for college in vakkenLijst:
        for persoon in studentenLijst:
            if college.id in persoon.vakken:
                college.studenten.append(persoon.studentnummer)
        college.aantalStudenten = len(college.studenten)

if __name__ == "__main__":
    main()
