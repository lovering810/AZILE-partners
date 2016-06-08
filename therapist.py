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
		response_dict = {}, dialect = {}, petnames=[], leaders=[], farewell="Bye now, %s",prop_pn=0.5, prop_ld=0.15):

		self.name = name
		self.kind = kind
		self.intro = intro
		self.response_dict = response_dict
		self.dialect = dialect
		self.farewell = farewell
		self.petnames = petnames
		self.prop_pn = prop_pn
		self.prop_ld = prop_ld
		self.leaders = leaders

	def getName(self):
		return self.name

	def getKind(self):
		return self.kind

	def introduce(self, patient_name):
		return self.intro%(patient_name, self.name)

	def respond(self, key):
		response_list = self.response_dict[key]
		return random.choice(response_list)
	
	def getStyle(self):
		return self.verb_style

	def petname(self, patient_name):
		if len(petnames) > 1:
			namen = random.choice(self.petnames)
			return namen
		else:
			return patient_name

	def prop_pn(self):
		return prop_pn

	def prop_ld(self):
		return prop_ld

	def AddPetName(self, new_petname):
		self.petnames.append(new_petname)

	def Dialect(self):
		return self.dialect

	def getLeader(self):
		return random.choice(self.leaders)

	def Farewell(self):
		return self.farewell

therapist_directory = {}
filepath = "/Users/rebecca/Desktop/LangTech/"
fileget = "%sAzile/therapists/therapy_personalities.txt"%(filepath)
infile = open(fileget, "r+w")

personalities = infile.readlines()

infile.close()

for line in personalities:

	# Get basic info for personality
	name, kind, intro, farewell, prop_pn, prop_ld  = line.split("/")
	print name


	# Unpack and store dictionary of idiolect replacements
	dialect_fileget = "%sAzile/therapists/personality_support_files/%s_dialect.txt"%(filepath,name)
	infile = open(dialect_fileget,"r")
	dialects = infile.readlines()
	dialect = {}
	for line in dialects:
		key, content = line.split(":")
		if content[-1]=="\n":
			content = content[:-1]
		dialect[key]=content

	# Unpack and store all responses that go with this personality
	respond_fileget = "%sAzile/therapists/personality_support_files/%s_responses.txt"%(filepath,name)
	in_file = open(respond_fileget,"r")
	responses = in_file.readlines()
	response_dict = {}
	for line in responses:
		prompt, answer = line.split("/")
		if answer[-1]=="\n":
			answer=answer[:-1]
		response_dict[prompt] = answer.split(";")

	# Unpack and store all pet names for this personality
	petnames_fileget = "%sAzile/therapists/personality_support_files/%s_petnames.txt"%(filepath,name)
	infileP = open(petnames_fileget, "r")
	petnames = infileP.read()
	petnamen = petnames.split(";")
	print petnamen
	for pname in petnamen:
		if pname[-1]=="\n":
			pname = pname[:-1]

	# Unpack and store all leading phrases
	leaders_fileget = "%sAzile/therapists/personality_support_files/%s_leaders.txt"%(filepath,name)
	infileL = open(leaders_fileget, "r")
	leader = infileL.read()
	leaders = leader.split(";")
	for lead in leaders:
		if lead[-1]=="\n":
			lead=lead[:-1]


	therapist_directory[name] = Therapist(name, kind, intro, response_dict, dialect, petnamen, leaders, farewell, prop_pn, prop_ld)







