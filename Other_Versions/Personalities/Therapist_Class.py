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

class Therapist:

	def __init__(self, name="Ted", kind="default", intro="Nice to meet you, I'm %s", \
		getmore = ["Hmm, tell me more.", "What's really under there?"],\
		adj = ["It seems like you're feeling %s. What do you think initially prompted that?"],\
		noun = ["How long have you been experiencing that sense of %s?"], \
		adv = ["So you're feeling kind of %s?"],\
		verb = ["%s, eh? That's a way of interacting with the world. Why is that your response to life?"],\
		repeater = ["We can't get very far if you just repeat yourself."],\
		hostile = ["Hey now, no need for that kind of talk!"],\
		notme = ["This isn't about me. Let's get back to you."],\
		farewell="Bye now, %s", verb_style="G", petnames=[]):

		self.name = name
		self.kind = kind
		self.intro = intro
		self.getmore = getmore
		self.adj = adj
		self.noun = noun
		self.adv = adv
		self.verb = verb
		self.repeater = repeater
		self.hostile = hostile
		self.notme = notme
		self.farewell = farewell
		self.verb_style = verb_style
		self.petnames = petnames

	def getName(self):
		return self.name

	def getKind(self):
		return self.kind

	def introduce(self, patient_name):
		return self.intro%(patient_name, self.name)

	def getMore(self):
		return random.choice(self.getmore)

	def adj(self, feeling):
		return random.choice(self.adj)%(feeling)

	def noun(self, feeling):
		return random.choice(self.noun)%(feeling)

	def adv(self, feeling):
		return random.choice(self.adv)%(feeling)

	def verb(self, feeling):
		return random.choice(self.verb)%(feeling)

	def Hostile(self):
		return (random.choice(self.hostile))

	def Repeater(self):
		return (random.choice(self.repeater))

	def NotMe(self):
		return (random.choice(self.notme))

	def getStyle(self):
		return self.verb_style

	def petname(self, patient_name):
		if len(petnames) > 1:
			return random.choice(self.petnames)
		else:
			return patient_name

	def AddPetName(self, new_petname):
		self.petnames.append(new_petname)

	def Farewell(self):
		return self.farewell

therapist_directory = {}

fileget = "/Users/rebecca/Desktop/LangTech/reLIZA/OldSchool_personalitieS.txt"
infile = open(fileget, "r+w")

personalities = infile.readlines()

infile.close()

for line in personalities:
	name, kind, intro, getmore, adj, noun, adv, verb, repeater, hostile, notme, farewell, verbstyle, petnames  = line.split("/")
	therapist_directory[name] = Therapist(name, kind, intro, getmore.split(";"), \
		adj.split(";"), noun.split(";"), adv.split(";"), verb.split(";"), \
		repeater.split(";"), hostile.split(";"), notme.split(";"), farewell, verbstyle, petnames.split(";"))






