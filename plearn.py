# -*- coding: utf-8 -*-

import pyAgrum as gum
from pyAgrum.lib.pretty_print import pretty_cpt
import numpy as np
import random
import csv
import gen
import matplotlib.pyplot as plt

def plearn(nomBIF, nomCSV, nomNew):
	
	# Chargement du BN
	bn = gum.BayesNet()
	bn.loadBIF('./BIF/'+nomBIF)	
	
	# Ouverture du CSV
	with open('./CSV/'+nomCSV, 'rb') as ficCSV:
		# Lecture de l'ensemble des lignes 	
		tirages = csv.reader(ficCSV, delimiter=',')
		# Pour chaque ligne (= tirage généré en partie 1) 
		for tirage in tirages :
				for nodeid in enumerate(tirage):
					parents = bn.parents(nodeid)
					# Si le noeud n'a pas de parent
					if len(parents) == 0 :
						bn.cpt(nodeid)[{bn.variables(nodeid).name:nodeid}] +=1
					# Sinon
					else:
						# Creation d'un dictionnaire pour gérer les parents	
						print 'a faire'
		
		bn.saveBIF('./BIF/'+nomNew)

def compareParams(bn1BIF, bn2BIF):
	
	# On charge les 2 BNs
	bn1 = gum.BayesNet()
	bn1.loadBIF('./BIF/'+bn1BIF)	
	bn2 = gum.BayesNet()
	bn2.loadBIF('./BIF/'+bn2BIF)	
	
	s = 0.0

	# Pour chaque variable du BN
	for nodeid in range(bn1.size()):
		# On récupère les probas
		p1 = bn1.cpt(nodeid)
		p2 = bn2.cpt(nodeid)

		# On instancie		
		i = gum.Instantiation (p1)
		i.setFirst()
		# On itere
		while (not i.end()):
			print(i)
			# On ajoute
			s+= pow((p1.get(i1) - p2.get(i1)), 2)
			i.inc()

	epsilon = 1.0 / bn1.size() * diffBN
	return epsilon

def evalLearning(nomBIF):

	resultats = []

	for i in range(1,1000):
		print 'N = '+i
		
		# On génère i cas sur le bn d'origine
		gen.genere('./CSV/tmp.csv','./BIF/bn.bif', i)

		# On apprend par rapport au CSV généré précedemment
		plearn('empty_bn.bif','tmp.csv','tmp.bif')

		# On compare le résultats (et l'ajoute à notre tableau pour la visualisation finale)
		resultats.append(compareParams('bn.bif','tmp.bif'))		
		
	plt.plot(resultats)
	plot.show()



#plearn('bn.bif', 'csvFile.csv')

resultats = [1,2,3]
plt.plot(resultats)
plt.show()
