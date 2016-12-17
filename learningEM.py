# -*- coding: utf-8 -*-
import os
import random
import pyAgrum as gum
from pyAgrum.lib.pretty_print import pretty_cpt
import matplotlib.pyplot as plt

from gen import *

class LearningEM:

	def __init__(self):
		pass

	def genere_missing(self,nomBIF,nomCSV,N,p):
		# Creation d'un objet generateur pour le tirage
		gen = Gen()
		# Lecture du Reseau Bayesien
		bn = gum.BayesNet()
		bn.loadBIF(os.path.join("BIF",nomBIF))

		seq = ''
		# On genere N cas
		for i in range(N):
			# Tirage de toutes les valeurs
			vals = gen.tirage(bn)
			# On ajoute les valeurs tirées à une chaine de caractère
			for value in range(len(vals)):
				# On remplace avec un pourcentage p la valeur générée par 100
				if(random.random() < p):
					seq += '100'
				else:
					seq += '{}'.format(vals[value])
				if (value != len(vals)-1):
					seq += ','
			seq += '\n'

		# Ecriture du résultat dans le fichier contenu dans un dossier csvDir
		csvFile = open(os.path.join("CSV",nomCSV), 'w')
		csvFile.write(seq)
		csvFile.close()


	def run(self):
		self.genere_missing('bn.bif','csvFile.csv',10,0.1)


if __name__ == "__main__":
	learningEM = LearningEM()
	learningEM.run()