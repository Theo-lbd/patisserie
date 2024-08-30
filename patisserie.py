import threading
import time
import math
from abc import ABC, abstractmethod


class Ingredient(ABC):
    """
    Classe abstraite représentant un ingrédient de base.

    :param nom: Le nom de l'ingrédient
    :param quantite: La quantité de l'ingrédient
    :param unite: L'unité de mesure de l'ingrédient
    """
    def __init__(self, nom, quantite, unite):
        self.nom = nom
        self.quantite = quantite
        self.unite = unite

    @abstractmethod
    def description(self):
        """
        Retourne une description de l'ingrédient.

        :return: Description de l'ingrédient
        """
        pass


class Oeuf(Ingredient):
    """
    Représente l'ingrédient 'Œuf'.

    :param quantite: Le nombre d'œufs
    """
    def __init__(self, quantite):
        Ingredient.__init__(self, "Oeuf", quantite, "unité(s)")

    def description(self):
        """
        Retourne une description de la quantité d'œufs.

        :return: Description de la quantité d'œufs
        """
        return f"{self.quantite} {self.unite} d'oeufs"


class Chocolat(Ingredient):
    """
    Représente l'ingrédient 'Chocolat'.

    :param quantite: Le poids du chocolat en grammes
    """
    def __init__(self, quantite):
        Ingredient.__init__(self, "Chocolat", quantite, "grammes")

    def description(self):
        """
        Retourne une description de la quantité de chocolat.

        :return: Description de la quantité de chocolat
        """
        return f"{self.quantite} {self.unite} de chocolat"


class Appareil:
    """
    Représente un appareil de cuisine qui mélange les ingrédients.
    """
    def __init__(self):
        """
        Initialise un appareil de cuisine vide.
        """
        self.ingredients = []

    def ajouter_ingredient(self, ingredient: Ingredient):
        """
       Ajoute un ingrédient à l'appareil.

       :param ingredient: L'ingrédient à ajouter
       """
        self.ingredients.append(ingredient)

    def description(self):
        """
        Retourne une description du mélange d'ingrédients dans l'appareil.

        :return: Description des ingrédients mélangés
        """
        descriptions = [ingredient.description() for ingredient in self.ingredients]
        return f"Mélange : " + ", ".join(descriptions)


class Commis(ABC, threading.Thread):
    """
    Classe abstraite représentant un commis de cuisine.

    :param nom: Le nom du commis
    :param recipient: Le récipient dans lequel le commis travaille
    """
    def __init__(self, nom, recipient):
        # initialisation de la classe parente
        threading.Thread.__init__(self)
        self.nom = nom
        self.recipient = recipient

    @abstractmethod
    def run(self):
        """
        Méthode abstraite représentant la tâche que le commis doit exécuter.
        """
        pass


class BatteurOeufs(Commis):
    """
    Représente un commis spécialisé dans le battage des œufs.

    :param nom: Le nom du commis
    :param recipient: Le récipient contenant les œufs
    """
    def __init__(self, nom, recipient: 'Recipient'):
        Commis.__init__(self, nom, recipient)

    def run(self):
        """
        Exécute le processus de battage des œufs.
        """
        oeufs = self.recipient.contenu
        # on suppose qu'il faut 8 tours de batteur par œuf présent dans le bol
        nb_tours = oeufs.quantite * 8
        for no_tour in range(1, nb_tours + 1):
            print(f"\t{self.nom} bat les œufs dans le {self.recipient.get_description()}, tour n°{no_tour}")
            time.sleep(0.5)  # temps supposé d'un tour de batteur


class FondeurChocolat(Commis):
    """
    Représente un commis spécialisé dans le fondage du chocolat.

    :param nom: Le nom du commis
    :param recipient: Le récipient contenant du chocolat
    """
    def __init__(self, nom, recipient: 'Recipient'):
        Commis.__init__(self, nom, recipient)

    def run(self):
        """
        Exécute le processus de fondage du chocolat.
        """
        appareil = self.recipient.contenu
        chocolat = None

        # cherche ingredient chocolat dans l'apparail
        for ingredient in appareil.ingredients:
            if isinstance(ingredient, Chocolat):
                chocolat = ingredient
                break

        if chocolat is None:
            raise ValueError("Pas de chocolat trouvé dans l'appareil")

        print(f"{self.nom} met de l'eau à chauffer dans une bouilloire")
        time.sleep(8)
        print(f"{self.nom} verse l'eau dans une casserole")
        time.sleep(2)
        print(f"{self.nom} pose le bol rempli de chocolat")
        time.sleep(1)
        # On suppose qu'il faut 1 tour de spatule par 10 g. de chocolat
        # présent dans le bol pour faire fondre le chocolat
        nb_tours = math.ceil(chocolat.quantite / 10)
        for no_tour in range(1, nb_tours + 1):
            print(f"{self.nom} mélange {chocolat.description()} dans le {self.recipient.description}, tour n°{no_tour}")
            time.sleep(1)  # temps supposé d'un tour de spatule


class Verseur(Commis):
    """
    Représente un commis chargé de verser le contenu d'un récipient dans un autre.

    :param nom: Le nom du commis
    :param recipient_source: le récipient source contenant le contenu à verser
    :param recipient_destination: Le récipient destination où le contenu sera versé
    :param rythme: Le rythme de versement (quantité par seconde)
    """
    def __init__(self, nom, recipient_source: 'Recipient', recipient_destination: 'Recipient', rythme: float):
        Commis.__init__(self, nom, recipient_source)
        self.recipient_source = recipient_source
        self.recipient_destination = recipient_destination
        self.rythme = rythme

    def run(self):
        """
        Exécute le processus de versement du contenu d'un récipient à un autre.
        """
        contenu_source = self.recipient_source.contenu

        if isinstance(contenu_source, Ingredient):
            self.verser_ingredient(contenu_source)
        elif isinstance(contenu_source, Appareil):
            # On verse tous les ingrédients de l'appareil
            for ingredient in contenu_source.ingredients:
                self.verser_ingredient(ingredient)
        else:
            raise TypeError("Le contenu du récipient source n'est ni un Ingredient ni un Appareil.")

    def verser_ingredient(self, ingredient):
        quantite_a_verser = ingredient.quantite

        while quantite_a_verser > 0:
            versement = min(self.rythme, quantite_a_verser)
            ingredient.quantite -= versement

            if isinstance(self.recipient_destination.contenu, Appareil):
                self.recipient_destination.contenu.ajouter_ingredient((
                    type(ingredient)(versement)
                ))
            elif isinstance(self.recipient_destination.contenu, Ingredient):
                self.recipient_destination.contenu.quantite += versement
            else:
                self.recipient_destination.contenu = type(ingredient)(versement)

            quantite_a_verser -= versement
            print(f"{self.nom} verse {versement} {ingredient.unite} de {ingredient.nom} dans {self.recipient_destination.get_description()}")
            time.sleep(1)

        print(f"{self.nom} a terminé de verser {ingredient.nom}")


class Recipient:
    """
    Représente un récipient contenant des ingrédients.

    :param description: Description du récipient
    :param contenu: Contenu du récipient (Ingredient/Appareil, optional)
    """
    def __init__(self, description, contenu=None):
        self.description = description
        self.contenu = contenu

    def get_description(self):
        """
        Retourne la description du récipient.

        :return: La description du récipient
        """
        return self.description


if __name__ == "__main__":
    oeufs = Oeuf(6)
    chocolat = Chocolat(200)

    appareil = Appareil()
    appareil.ajouter_ingredient(oeufs)
    appareil.ajouter_ingredient(chocolat)

    recipient_oeufs = Recipient("cul de poule avec œufs", oeufs)
    recipient_chocolat = Recipient("bol avec chocolat", appareil)
    recipient_chocolat_2 = Recipient("second bol avec chocolat", appareil)  # Nouveau récipient
    recipient_melange = Recipient("récipient pour mélange")  # Récipient destination pour le versement

    batteur = BatteurOeufs("Jonh", recipient_oeufs)
    fondeur = FondeurChocolat("Jane", recipient_chocolat)
    fondeur_2 = FondeurChocolat("Doe", recipient_chocolat_2) # Nouveau Fondeur
    verseur = Verseur("Alan", recipient_chocolat, recipient_melange, rythme=50)  # Nouveau verseur

    batteur.start()
    fondeur.start()
    fondeur_2.start()
    verseur.start()

    batteur.join()
    fondeur.join()
    fondeur_2.join()
    verseur.join()

    print(f"\n{batteur.nom} peut à présent incorporer le chocolat fondu par {fondeur.nom} et {fondeur_2.nom} aux œufs.")
    print(appareil.description())
