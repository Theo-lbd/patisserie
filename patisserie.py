import threading
import time
import math
from abc import ABC, abstractmethod

class Commis(ABC, threading.Thread):
    def __init__(self, nom):
        threading.Thread.__init__(self) #initialisation de la classe parente
        self.nom = nom

    @abstractmethod
    def run(self):
        pass

class BatteurOeufs(Commis):
    def __init__(self, nom, nb_oeufs):
        Commis.__init__(self, nom)
        self.nb_oeufs = nb_oeufs

    def run(self):
        # on suppose qu'il faut 8 tours de batteur par œuf présent dans le bol
        nb_tours = self.nb_oeufs * 8
        for no_tour in range(1, nb_tours + 1):
            print(f"\t{self.nom} bat les {self.nb_oeufs} oeufs, tour n°{no_tour}")
            time.sleep(0.5)  # temps supposé d'un tour de batteur


class FondeurChocolat(Commis):
    def __init__(self, nom, quantite):
        Commis.__init__(self, nom)
        self.quantite = quantite  # en grammes

    def run(self):
        print(f"{self.nom} met de l'eau à chauffer dans une bouilloire")
        time.sleep(8)
        print(f"{self.nom} verse l'eau dans une casserole")
        time.sleep(2)
        print(f"{self.nom} pose le bol rempli de chocolat")
        time.sleep(1)
        # on suppose qu'il faut 1 tour de spatule par 10 g. de chocolat
        # présent dans le bol pour faire fondre le chocolat
        nb_tours = math.ceil(self.quantite / 10)
        for no_tour in range(1, nb_tours + 1):
            print(f"{self.nom} mélange {self.quantite} de chocolat à fondre, tour n°{no_tour}")
            time.sleep(1)  # temps supposé d'un tour de spatule


if __name__ == "__main__":
    batteur = BatteurOeufs("Jonh", 6)
    fondeur = FondeurChocolat("Jane",200)
    batteur.start()
    fondeur.start()
    batteur.join()
    fondeur.join()
    print("\nJonh peux à présent incorporer le chocolat que Jane à fait fondre aux oeufs")
