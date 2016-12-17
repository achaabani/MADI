# -*- coding: utf-8 -*-
import os
import csv
import copy
import pyAgrum as gum
from pyAgrum.lib.pretty_print import pretty_cpt

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

	def compareParams(bn1,bn2):
		epsilon = 0


	def evalLearningP(nomBN):
		pass

	def run(self):
		self.plearn('empty_bn.bif','csvFile.csv')

if __name__ == "__main__":
	learning1 = Learning1()
	learning1.run()