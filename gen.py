# -*- coding: utf-8 -*-
import pyAgrum as gum
from pyAgrum.lib.pretty_print import pretty_cpt
import numpy as np
from numpy.random import choice
import random
import os
from operator import itemgetter

class Gen:

	def __init__(self):
		pass

	# Generation du fichier CSV
	def genere(self,nomBif,nomCSV,N):

		# Lecture du Reseau Bayesien
		bn = gum.BayesNet()
		bn.loadBIF(nomBif)

		seq = ''
		# On genere N cas
		for i in range(N):
			# Tirage de toutes les valeurs
			vals = self.tirage(bn)
			# On ajoute les valeurs tirées à une chaine de caractère
			for value in range(len(vals)):
				seq += '{}'.format(vals[value])
				if (value != len(vals)-1):
					seq += ','
			seq += '\n'

		# Ecriture du résultat dans le fichier contenu dans un dossier csvDir
		csvFile = open(os.path.join("csvDir",nomCSV), 'w')
		csvFile.write(seq)
		csvFile.close()

	def tirage(self,bn):

		# Dictionnaire contenant les probas déja calculées pour chaque variable, indexées par chiffre et non pas par lettre
		tirage = {}

		# Tant qu'on a pas les probas de toutes les variables
		while len(tirage) != bn.size():
			# On test pour chaque variable
			for i in range(bn.size()):
				# On test si on n'a pas encore calculé les probas d'une variable
				# et que celles de ses parents l'ont déja étées
				if(not tirage.has_key(ord(bn.variable(i).name())-ord('a')) and set(bn.parents(i)).issubset(set(tirage.keys()))):
					# Si la variable n'a pas de parents, la distribution se fait directement
					listeProbas = []
					if(bn.parents(i) == []):
						listeProbas = bn.cpt(i).tolist()
					# Sinon on calcule la distribution en fonction des valeurs de ses parents
					else:
						# Liste contenant les valeurs des parents triés par ordre alphabetique décroissant
						valParents = []
						for parents in sorted(bn.parents(i))[::-1]:
							valParents.append(tirage[parents])

						# Recuperation de la distrubtion de proba de la variable
						# Si X et Y sont les parents de Z, on obtient P(Z|X,Y) avec bn.cpt(index_z)[valeur_y][valeur_x]
						listeProbas = bn.cpt(i)
						for val in valParents:
							listeProbas = listeProbas[val]
						listeProbas = list(listeProbas)

					# Remplit le tableau avec les nombres correspondant à chaque variable
					# On tire aléatoirement une valeur de la liste des valeurs possible, avec une distribution égale à
					# celle récupérée précédemment, stockée dans listeProbas
					tirage[ord(bn.variable(i).name())-ord('a')] = choice(range(len(listeProbas)), 1, listeProbas)[0]

		return tirage


	def run(self):
		self.genere('bn.bif','csvFile.csv',5)


if __name__ == "__main__":
	gen = Gen()
	gen.run()