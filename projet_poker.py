import random
import matplotlib.pyplot as plt
import itertools

noms = [
    'Rien', 'une Paire', 'une Double Paire', 'un Brelan', 'une Quinte',
    'une Couleur', 'un Full', 'un Carré', 'un Quinte Flush'
]


class Carte:

    def __init__(self, color=0, value=2):
        self.couleur = color
        self.valeur = value

    def __repr__(self):
        noms_couleurs = ['trèfle', 'carreau', 'cœur', 'pique']
        noms_valeurs = [
            None, None, '2', '3', '4', '5', '6', '7', '8', '9', '10', 'valet',
            'dame', 'roi', 'as'
        ]
        return noms_valeurs[self.valeur] + " de " + noms_couleurs[self.couleur]

    def __lt__(self, other):
        if other.valeur > self.valeur:
            return True
        else:
            if other.valeur == self.valeur:
                if other.couleur > self.couleur:
                    return True
            return False


class Paquet:

    def __init__(self):
        self.cartes = [Carte(i, j) for i in range(4) for j in range(2, 15)]

    def __repr__(self):
        return str(self.cartes).strip("[]")

    def distribuer_carte(self, n, main):
        for i in range(n):
            carte = random.choice(self.cartes)
            main.cartes.append(carte)
            self.cartes.remove(carte)
        return main.cartes

    def ajouter_carte(self, carte):
        self.cartes.append(carte)

    def battre(self):
        random.shuffle(self.cartes)


class Main(Paquet):

    score1 = 0  # Variable qui va indiqué le score et donc la combinaison

    def __init__(self, etiquette=''):
        self.cartes = []
        self.etiquette = ''
        self.combs = []
        self.carta = [
        ]  # Variable qui va par la suite stocké les cartes si on a une combinaison

    def tri(self):
        return sorted(self.cartes)

    def paire(self, l_carte):
        l_carte.sort()
        values = []
        for i in range(len(l_carte)):
            values.append(
                l_carte[i].valeur
            )  # On stock les valeurs des cartes dans une liste indépendante
        if len(l_carte) == 1 or len(l_carte) == 0:
            return Main.score1
        else:
            if values.count(l_carte[0].valeur) == 2:
                Main.score1 += 1
                for i in self.cartes:
                    if i.valeur == l_carte[
                            0].valeur:  # On enlève les cartes qui forment une paire pour qu'elles n'affectent pas les autres méthode de score
                        self.cartes.remove(i)
                return self.paire(l_carte[1:])
            return self.paire(l_carte[1:])


# La méthode paire vérifie aussi si on a un cas de double paire

    def brelan(self, l_carte):  # Validé
        l_carte.sort()
        values = []
        for i in range(len(l_carte)):
            values.append(l_carte[i].valeur)
        if len(l_carte) == 1 or len(l_carte) == 0:
            return Main.score1
        else:
            if values.count(l_carte[0].valeur) == 3:
                Main.score1 += 3
                for i in self.cartes:
                    if i.valeur == l_carte[0].valeur:
                        self.cartes.remove(i)
                return self.brelan(l_carte[3:])
            return self.brelan(l_carte[1:])

    def quinte(self, l_carte):  # Validé
        l_carte.sort()
        values = []
        for i in range(len(l_carte)):
            values.append(l_carte[i].valeur)
        var = True  # Pour vérifier que la liste contient des nombres successif
        if len(l_carte) >= 5:
            if values[-1] == 14 and values[0] == 2:
                for i in range(
                        len(l_carte) - 2
                ):  # Dans le cas où on a une quinte qui commence par As - 2 - 3...
                    if values[i] - values[i + 1] != -1:
                        var = False
            else:
                for i in range(len(l_carte) -
                               1):  # Dans le cas "normal" (2-3-4-5-6)
                    if values[i] - values[i + 1] != -1:
                        var = False
            if len(l_carte) < 5:
                return Main.score1
            else:
                if var == True:
                    Main.score1 += 4
                    self.cartes = self.cartes[5:]
                    return self.quinte(l_carte[5:])
                return self.quinte(l_carte[1:])
        pass

    def Couleur(self, l_carte):
        l_carte.sort(key=lambda card: card.couleur)
        colors = []
        for i in range(len(self.cartes)):
            colors.append(self.cartes[i].couleur)
        if len(l_carte) == 1 or len(l_carte) == 0:
            return Main.score1
        else:
            if colors.count(l_carte[0].couleur) == 5:
                Main.score1 += 5
                self.cartes = self.cartes[4::]
                return self.Couleur(l_carte[5:])
            return self.Couleur(l_carte[1:])

    def full(self, l_carte):  # Validé
        l_carte.sort()
        self.brelan(l_carte)
        self.paire(l_carte)
        if Main.score1 == 4:  # Vérifcation si on a une paire et un berlan
            Main.score1 = 6
        return Main.score1

    def carre(self, l_carte):
        l_carte.sort()
        values = []
        for i in range(len(l_carte)):
            values.append(l_carte[i].valeur)
        if len(l_carte) == 1 or len(l_carte) == 0:
            return Main.score1
        else:
            if values.count(l_carte[0].valeur) == 4:
                Main.score1 += 7
                self.cartes = self.cartes[3::]
                return self.paire(l_carte[4:])
            return self.paire(l_carte[4:])

    def Quinte_flush(self, l_carte):
        l_carte.sort(key=lambda card: card.couleur)
        colors = []
        for i in range(len(self.cartes)):
            colors.append(self.cartes[i].couleur)
        while len(l_carte) > 5:
            if colors.count(colors[0]) == 5:
                self.quinte(l_carte)
                if Main.score1 == 4:
                    Main.score1 = 8
                else:
                    return self.Quinte_flush(l_carte[1:])
        return Main.score1

    def score(self):
        Main.score1 = 0  # Pour réinistialliser la valeur de Main.score1 qu'on utilise la méthode score()
        self.Quinte_flush(self.cartes)
        self.carre(self.cartes)
        self.full(self.cartes)
        self.Couleur(self.cartes)
        self.quinte(self.cartes)
        self.brelan(self.cartes)
        self.paire(self.cartes)
        return Main.score1

    def combsfunc(self):
        self.combs = list(itertools.combinations(b.cartes, 5))

a = Paquet()
b = Main()


def meilleur_combo(b):
    global noms
    a.distribuer_carte(
        7, b)  #On commence par créer et afficher une main à 7 cartes
    print('Voici la main de 7 cartes : ', b.cartes)
    print("")
    b.combsfunc(
    )  #On utilise la méthode qui utilise itertools pour trouver toutes les combinaisons de 5 possibles à partir de la main de 7
    listmains = []
    for i in b.combs:  #Ici on convertit toutes les mains possibles en objets Main et on les stockent dans la liste listmains
        v = Main()
        for e in i:
            v.cartes.append(e)
            v.carta.append(
                e
            )  #Ici on append également dans la liste carta qui n'est pas modifiée par les méthodes score
        listmains.append(v)
    mainsscores = []

    for i in listmains:
        mainsscores.append(
            [listmains.index(i), i.score()]
        )  #pour tout les objets Main dans la liste, on append leur index et leur score sous forme de liste dans listmain

    e = 0
    index = 0

    for i in mainsscores:  #Ici on trouve la main avec le plus haut score
        if i[1] > e:
            e = i[1]
            index = i[0]

    b.cartes = []  #On vide la liste carte

    b.cartes.append(listmains[index].carta
                    )  #On y append la meilleur main trouvé auparravent
    b.cartes.sort
    return 'Voici la meilleur main possible : ', b.cartes, "et avec un " + str(
        noms[b.score1])  #Et enfin on affiche la main en question


print(meilleur_combo(b))
print("")

resultat = [0] * 9
# Indice 0 = rien / Indice 1 = paire etc...

for i in range(10000):
    a = Paquet()
    b = Main()
    a.distribuer_carte(5, b)
    resultat[b.score()] += 1

print(resultat)
#différentes combinaisons
noms = [
    'Rien', 'une Paire', 'une Double Paire', 'un Brelan', 'une Quinte',
    'une Couleur', 'un Full', 'un Carré', 'un Quinte Flush'
]
somme = sum(resultat)
#calcul des pourcentages
for i in range(len(resultat)):
    print((resultat[i] / somme) * 100, "% de chance d'avoir", noms[i])

#representation graphique avec matplotlib

labels = 'Rien', 'Paire', 'Double Paire', 'Brelan', 'Quinte', 'Couleur', 'Full', 'Carré', 'Quinte Flush'
sizes = resultat
labels_pr = []
for i in range(9):
    labels_pr.append(
        str(labels[i]) + " " + str(round((resultat[i] / 10000) * 100, 2)) +
        "%")
#création du camembert
plt.pie(sizes, shadow=True, startangle=90)

plt.axis('equal')
plt.legend(labels_pr, loc=3)
#affichage du camembert
plt.savefig('cam1.png')
plt.show()

#création d'un camembert qu'avec les combinaisons c-à-d sans le "rien"
labels = 'Paire', 'Double Paire', 'Brelan', 'Quinte', 'Couleur', 'Full', 'Carré', 'Quinte Flush'
sizes = resultat[1:]
labels_pr = []
labels = 'Paire', 'Double Paire', 'Brelan', 'Quinte', 'Couleur', 'Full', 'Carré', 'Quinte Flush'
for i in range(8):
    labels_pr.append(
        str(labels[i]) + " " + str(round((sizes[i] / sum(sizes)) * 100, 2)) +
        "%")
plt.pie(sizes, shadow=True, startangle=90)

plt.axis('equal')
plt.legend(labels_pr, loc=3)
plt.savefig('cam2.png')
plt.show()

fig, ax = plt.subplots()
#liste avec les différents types
types = [
    'Rien', 'Paire', 'Double Paire', 'Brelan', 'Suite', 'Couleur', 'Full',
    'Carré', 'Quinte Flush'
]
#stockage des resultats
counts = resultat
#creation du bar charts
ax.bar(types, counts)
#creation de la legende
ax.set_ylabel("Nombre d'apparition de la combinaison")
ax.set_title("Les fréquences d'apparition de chaque combinaison.")
plt.savefig('chart.png')
plt.show()
