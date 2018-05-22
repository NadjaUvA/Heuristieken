"""
Algoritme dat een rooster zoekt door allen wissels toe te staan die voor verbetering zorgen.

Linsey Schaap (11036109), Kenneth Goei (11850701), Nadja van 't Hoff (11030720)
"""

import random
import rooster as Rooster
import zaalSlot as ZaalSlot
from visualiseer import visualiseer


def hillClimbing(dagen, tijdsloten):
    # maak een rooster object aan
    rooster = Rooster.Rooster(dagen, tijdsloten)

    minIteraties = 1000
    mutaties = 0
    lijstScore = []
    hillClimberRooster = []

    rooster.vulRandom()
    score = rooster.scoreOnderverdeeld()
    visualiseer(tijdsloten, dagen, rooster, score)

    for i in range(minIteraties):

        # wissel twee willekeurige zaalsloten
        indexZaalslot = random.sample(range(len(rooster.zaalslotenLijst)), 2)
        randomZaalslot1 = rooster.zaalslotenLijst[indexZaalslot[0]]
        randomZaalslot2 = rooster.zaalslotenLijst[indexZaalslot[1]]

        randomZaalslot1.wissel(randomZaalslot2)
        score2 = rooster.score()
        lijstScore.append(score)

        if score2 > score:
            score = score2
            mutaties += 1

        else:
            randomZaalslot2.wissel(randomZaalslot1)

    hillClimberRooster.append([rooster, score])

    aantalIteraties = []
    for i in range(minIteraties):
        aantalIteraties.append(i)

    visualiseer(tijdsloten, dagen, rooster, score2)
    print(hillClimberRooster)
    return hillClimberRooster
