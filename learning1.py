# -*- coding: utf-8 -*-
import os
import csv
import pyAgrum as gum
from pyAgrum.lib.pretty_print import pretty_cpt
import matplotlib.pyplot as plt

from gen import *

class Learning1:

	def __init__(self):
		pass

	def	plearn(self,nomBIF,nomCSV):		
		# Lecture du Reseau Bayesien
		bn = gum.BayesNet()
		bn.loadBIF(os.path.join("BIF",nomBIF))
		# Ouverture du fichier CSV contenant les tirages
		csvFile = open(os.path.join("CSV",nomCSV), 'rb')

		# Pour chaque tirage, on incrémente le nombre d'occurences (on suppose la base initiale vide)
		for tirage in csv.reader(csvFile, delimiter = ","):
			# Pour chaque valeur tirée
			for var in range(len(tirage)):
				# Si elle n'a pas de parent, on l'incrémente directement
				if (bn.parents(var) == []):
					bn.cpt(var)[int(tirage[var])] += 1
				# Sinon
				else:
					# On filtre le tableau avec la valeur de la variable observee et celle de ses parents
					parents = {}
					for parent in bn.parents(var):
						parents[bn.variable(parent).name()] = int(tirage[bn.names().index(bn.variable(parent).name())])
					parents[bn.variable(var).name()] = int(tirage[var])
					# On incrémente la valeur filtree
					bn.cpt(var)[parents] += 1

		# Normalisation du BN pour obtenir des probas
		for i in range(len(bn.names())):
			bn.cpt(i).normalize()

		return bn

	def compareParams(self,bn1,bn2):

		# Valeur d'epsilon
		epsilon = 0

		# On calcule la somme des carrés de la difference de toutes les valeurs des BN deux à deux
		for i in range(len(bn1.names())):
			inst = gum.Instantiation(bn1.cpt(i))
			inst.setFirst()
			epsilon += pow(bn1.cpt(i).get(inst) - bn2.cpt(i).get(inst), 2)
			inst.inc()

		# On divise la somme par le nombre de paramètres
		epsilon /= len(bn1.names())

		return epsilon


	def evalLearningP(self,nomBIF,nomCSV, N):
		# Genere les fichiers CSV selon le réseau bayesien en parametre
		generator = Gen()

		# Tableau où les valeurs de epsilon seront stockées
		tab = []

		# Compare les reseaux bayesiens selon les parametres appris
		for i in range(1,N):
			# Affichage de l'état de l'avancement
			print i
			# Generation de valeurs et apprentissage du réseau bayesien
			generator.genere('bn.bif',nomCSV,i)
			bn1 = self.plearn('empty_bn.bif',nomCSV)
			# Ajout dans le tableau de la valeur de epsilon
			bn2 = gum.BayesNet()
			bn2.loadBIF(os.path.join("BIF",'bn.bif'))

			tab.insert(i,self.compareParams(bn1,bn2))

		# Creation et affichage de la courbe représentant l'évolution de epsilon selon N
		plt.plot(tab)
		plt.show()

	def run(self):
		self.evalLearningP('empty_bn.bif','csvFile.csv',200)


if __name__ == "__main__":
	learning1 = Learning1()
	learning1.run()