##!/usr/bin/python
##
## September 13, 2015
## Author: Rebecca Lovering 
## Class: Language Technology (taught by Andrew Rosenberg at CUNY GC)
##
import re
import random
import string
import nltk
from string import *

class Patient:

	def __init__(self, name, probCause="", probSymptoms=[], \
		propEssence="", propDetails=[], advMain="", advAdded=[], advDis=[], \
		apImmediate="", apLT="", corpus={}):
		self.name = name
		self.probCause = probCause
		self.probSymptoms = probSymptoms
		self.propEssence = propEssence
		self.propDetails = propDetails
		self.advMain = advMain
		self.advAdded = advAdded
		self.advDis = advDis
		self.apImmediate = apImmediate
		self.apLT = apLT
		self.corpus = corpus

		def getName(self):
			return self.name

		def getProblem(self):
			return self.probCause, self.probSymptoms

		def getCause(self):
			return self.probCause

		def getSymptoms(self):
			return self.probSymptoms

		def getProposal(self):
			return self.propEssence, self.propDetails

		def getEssence(self):
			return self.propEssence

		def getDetails(self):
			return self.getDetails

		def getAdvantages(self):
			return self.advMain, self.advAdded, self.advDis

		def getMainAdv(self):
			return self.advMain

		def getAddedAdv(self):
			return self.advAdded

		def getDisAdv(self):
			return self.advDis

		def getCorpus(self):
			return self.corpus

		def addToCorpus(self, dialogue):
			self.corpus.append(dialogue)

RJ = Patient("RJ")
print RJ.probCause



