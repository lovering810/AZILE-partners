##!/usr/bin/python
##
## September 16, 2015
## Author: Rebecca Lovering 
## Class: Language Technology (taught by Andrew Rosenberg at CUNY GC)
##
import re
import random
import string
import nltk
from Patient_Class import Patient as pt
from Therapist_Class import Therapist
from Therapist_Class import therapist_directory
from string import *

def NameCheck(name):

	tokenized_name = nltk.word_tokenize(name)
	name_tagged = nltk.pos_tag(tokenized_name)
	name_tags = [x[1] for x in name_tagged]

	if "NNP" in name_tags:
		ind = name_tags.index("NNP")
		name = name_tagged[ind][0]

	else:
		name = raw_input("I'm sorry, I didn't catch that. Please enter your name:\n")
		NameCheck(name)

	return name

def ChooseTherapist():

	for item in therapist_directory:
		print "Hello! Welcome to the ElIZA Partners! We have several partners available to talk to."
		print "%s\t%s"%(item, Therapist.getKind(therapist_directory[item]))

	therapist_choice = raw_input("\nWho would you like as your therapist today?\n")

	if therapist_choice in therapist_directory.keys():

		therapist = therapist_directory[therapist_choice]

		print "\nAll set to talk to %s.\n"%(Therapist.getName(therapist))

		return therapist

	else:
		print "\nI'm afraid that wasn't one of the options. \
		\nPlease choose again, and be sure to type the full name!\n"
		return ChooseTherapist()

def sussProblem(patient):

	while Patient.checkProblem(patient)==False:
		if len(Patient.getSymptoms(patient))<1:


def CheckPatient(patient):
	

	if Patient.checkProblem(patient)==False:
		 sussProblem(patient)

	elif Patient.checkProblem(patient)==True \
	and Patient.checkProposal(patient)==False:
		sussProposal(patient) 

	elif Patient.checkProblem(patient)==True \
	and Patient.checkProposal(patient)==True \
	and Patient.checkAdvantages(patient)==False:
		sussAdvantages(patient) 

	elif Patient.checkProblem(patient)==True \
	and Patient.checkProposal(patient)==True \
	and Patient.checkAdvantages(patient)==True \
	and Patient.checkAP(patient)==False:
		sussActionPlan(patient)

	if Patient.checkProblem(patient)==True \
	and Patient.checkProposal(patient)==True \
	and Patient.checkAdvantages(patient)==True \
	and Patient.checkAP(patient)==True:
		Summarize(patient)

def Stylize(therapist, answer):

	tokenized_answer = nltk.word_tokenize(answer)
	answer_tagged = nltk.pos_tag(answer)

	if Therapist.getStyle(therapist)=="NG":

		answer = answer

	else:

		answer = re.sub("ing\W", "in' ", answer)

	return answer

def DetectFeels(user_input):

	feel_think = re.compile(r'(.*?((feel|think)(ing)?)(.*)\.)')

	if re.match(feel_think, user_input):
		answer = "What makes you %s that way?"%(feel_think.group(1))


therapist = ChooseTherapist()

name = NameCheck(raw_input("\nAnd what's your name?\n\n"))

patient = pt(name)

print Therapist.introduce(therapist,name)

opener = Stylize(therapist, "\nWhat would you say is the single biggest challenge you're facing right now?")

user_init = raw_input(opener+"\n\n")








