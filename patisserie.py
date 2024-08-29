import threading
import time
import math
from abc import ABC, abstractmethod


class Ingredient(ABC):
    def __init__(self, nom, quantite, unite):
        self.nom = nom
        self.quantite = quantite
        self.unite = unite

    @abstractmethod
    def description(self):
        pass


class Oeuf(Ingredient):
    def __init__(self, quantite):
        Ingredient.__init__(self, "Oeuf", quantite, "unité(s)")

    def description(self):
        return f"{self.quantite} {self.unite} d'oeufs"


class Chocolat(Ingredient):
    def __init__(self, quantite):
        Ingredient.__init__(self, "Chocolat", quantite, "grammes")

    def description(self):
        return f"{self.quantite} {self.unite} de chocolat"


class Appareil:
    def __init__(self):
        self.ingredients = []

    def ajouter_ingredient(self, ingredient: Ingredient):
        self.ingredients.append(ingredient)

    def description(self):
        descriptions = [ingredient.description() for ingredient in self.ingredients]
        return f"Mélange : " + ", ".join(descriptions)


class Commis(ABC, threading.Thread):
    def __init__(self, nom):
        threading.Thread.__init__(self) #initialisation de la classe parente
        self.nom = nom

    @abstractmethod
    def run(self):
        pass


class BatteurOeufs(Commis):
    def __init__(self, nom, oeufs: Oeuf):
        Commis.__init__(self, nom)
        self.oeufs = oeufs

    def run(self):
        # on suppose qu'il faut 8 tours de batteur par œuf présent dans le bol
        nb_tours = self.oeufs.quantite * 8
        for no_tour in range(1, nb_tours + 1):
            print(f"\t{self.nom} bat les œufs, tour n°{no_tour}")
            time.sleep(0.5)  # temps supposé d'un tour de batteur


class FondeurChocolat(Commis):
    def __init__(self, nom, appareil: Appareil, chocolat: Chocolat):
        Commis.__init__(self, nom)
        self.appareil = appareil
        self.chocolat = chocolat

    def run(self):
        print(f"{self.nom} met de l'eau à chauffer dans une bouilloire")
        time.sleep(8)
        print(f"{self.nom} verse l'eau dans une casserole")
        time.sleep(2)
        print(f"{self.nom} pose le bol rempli de chocolat")
        time.sleep(1)
        # on suppose qu'il faut 1 tour de spatule par 10 g. de chocolat
        # présent dans le bol pour faire fondre le chocolat
        nb_tours = math.ceil(self.chocolat.quantite / 10)
        for no_tour in range(1, nb_tours + 1):
            print(f"{self.nom} mélange {self.chocolat.description()}, tour n°{no_tour}")
            time.sleep(1)  # temps supposé d'un tour de spatule


if __name__ == "__main__":
    oeufs = Oeuf(6)
    chocolat = Chocolat(200)

    appareil = Appareil()
    appareil.ajouter_ingredient(oeufs)
    appareil.ajouter_ingredient(chocolat)

    batteur = BatteurOeufs("Jonh", oeufs)
    fondeur = FondeurChocolat("Jane",appareil, chocolat)

    batteur.start()
    fondeur.start()

    batteur.join()
    fondeur.join()
    print(f"\n{batteur.nom} peux à présent incorporer le chocolat par {fondeur.nom} aux oeufs")
    print(appareil.description())
