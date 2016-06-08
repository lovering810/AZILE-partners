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
import en
from Patient_Class import Patient
from Therapist_Class import Therapist
from Therapist_Class import therapist_directory
from string import *
from nltk.stem.snowball import SnowballStemmer
from stopwords import stopword_list
stemmer = SnowballStemmer("english")

# RegEx patterns to call on later
YeaNayPattern = re.compile(r'(([Yy](e(s|ah))|up)|([Nn](o|ot really)))')
HostilePattern = re.compile(r'(.*([Ff]uck|[Ss]hit(ty)?|[Dd]amn).*)')
SecondPPattern = re.compile(r"(.*?\byou(('re|r)?\b).*)")
FirstPPattern = re.compile(r"(.*?\b(I(\b|'m)|[mM](e|y)|[wW]e)\b)")
verbVP = re.compile(r'VP: (.*)?/VB.*')
gbye = re.compile(r'(([Gg]ood)?[Bb]ye)')
stopverbs = re.compile(r'(.*(think|feel|hurt|be|contemplate|consider|wonder|be|have|do|go|say).*)')

VP_Pattern = 'VP: {((<MD>)?((<VB.*>(<RB.*>)?|(<RB.*><VB.*>))))}'



# Introduces therapist options and lets user choose one
def ChooseTherapist():

	for item in therapist_directory:
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

# Check name input for proper noun.
def NameCheck(name):

	namen = ""
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

# Get patient name_input
def getPtName():

	name = raw_input("What's your name?\n\n")

	name = NameCheck(name)

	return name

# Get basic info for session (calls other functions)
def InitializeSession():

	therapist = ChooseTherapist()

	patient = getPtName()	

	first_Uresponse = raw_input("%s\n"%(Therapist.introduce(therapist,patient)))

	return therapist, patient, first_Uresponse

# Check response for triggers
def DangerZone(user_response):

	suicidetrigger = re.search(r".*?(([sS]uicid(e|al))|[Kk]ill(ing)? myself).*?", user_response)
	selfharmtrigger = re.search(r".*?h(arm|urt)(ing)? myself.*?", user_response)
	
	if suicidetrigger != None:
		print "Hey, all joking aside, suicide is a serious thing,\n\
		 and if you're thinking about it, you should speak to a human. \n\
		 You can call one at 1-800-273-8255, any time. \n"
		return True
	elif selfharmtrigger!= None:
		print "Self harm is serious stuff, and you should talk to a live human and get some help.\n\
		Try calling 1-800-273-TALK or 1-800-334-HELP, any time."
		return True
	else:
		return False

# if user wants to leave, says goodbye, program ends.
def Goodbye(Uresponse):
	if re.search(gbye, Uresponse) != None:
		return True
	else:
		return False

# Check for inputs that preclude processing of content
def InputBattery(Uresponse, last_Uresponse):

	if DangerZone(Uresponse)==True:
		return "Farewell"
	else:
		if Goodbye(Uresponse)==True:
			return "Farewell"
		else:
			if Uresponse==last_Uresponse:
				return "Repeater"
			else:
				if re.match(YeaNayPattern, Uresponse) or len(en.sentence.tag(Uresponse))<3:
					return "getMore"
				else:
					if re.match(HostilePattern, Uresponse):
						return "Hostile"
					else:
						if re.match(SecondPPattern, Uresponse) and not re.match(FirstPPattern, Uresponse):
							return "NotMe"
						else:
							return False

# looking for emotion words, POS of emotion
def DetectFeels(Uresponse):

	feelcount = 0

	Uresponse = en.sentence.tag(Uresponse)

	for (word, tag) in Uresponse:
		if stemmer.stem(word):
			word = stemmer.stem(word)
		else:
			word = word

		if tag[:2]=="NN" and en.noun.is_emotion(word) and word not in stopword_list:
			feelcount = feelcount+1
			feel = word
			feelkind = "noun"
		elif tag[:2]=="JJ" and en.adjective.is_emotion(word)==True and word not in stopword_list:
			feelcount=feelcount+1
			feel = word
			feelkind = "adj"
		elif tag[:2]=="RB" and en.adverb.is_emotion(word)==True and word not in stopword_list:
			feelcount = feelcount+1
			feel = word
			feelkind = "adv"
		elif tag[:2]=="VB" and en.verb.is_emotion(word)==True and word not in stopword_list:
			feelcount=feelcount+1
			feel = word
			feelkind = "verb"


	if feelcount==0:		
		return False
	else:
		return feel, feelkind

# looking for have-to, must, etc.
def Obligation(Uresponse):

	obligated = re.compile(r'(.*I? ((have to|must|got to|gotta)(.*))\.)')
	musts = re.search(obligated, Uresponse)

	if musts:
		borrowed_chunk = Pronounify(musts.group(2))
		response = "Feeling that you %s can be stressful."%(borrowed_chunk)
		return response
	else:
		return False

# looking for incomplete sentences
def SubjectVerb(Uresponse):

	if en.sentence.find(Uresponse, "(.*)NN*(.*?)VB*(.*)"):
		return False
	else:
		response = "You do not seem to have a subject for each of your verbs."
		return response

# looking for "because" and attendant information
def Causal(Uresponse):

	cuz = re.compile(r'(.*(([Bb]ecause|[Ss]o)(.*?)\.))')
	becuz = re.search(cuz, Uresponse)

	if becuz or en.sentence.find(Uresponse, ".*NN*(.*)?VB* that NN*(.*)?VB*"):
		response = "What makes you sure that '%s' is really causally related?"%(becuz.group(2))
		return response

	else:
		return False

# find breakup, sad words.
def HeartBreak(Uresponse):

	sadnesses = re.compile(r'((.*heart(.*)?(break|broken).*)|(.*break ?up).*)')
	sadness = re.search(sadnesses, Uresponse)

	if sadness:
		response = "I am so sorry to hear that. That can feel like the end of the world."
		return response
	else:
		return False

# looking for a handful of things I couldn't generalize successfully with the other patterns
def BuiltIns(Uresponse):
	if Obligation(Uresponse)==False:
		if SubjectVerb(Uresponse)==False:
			if Causal(Uresponse)==False:
				if HeartBreak(Uresponse)==False:
					return False
				else:
					response = HeartBreak(Uresponse)
			else:
				response = Causal(Uresponse)
		else:
			response = SubjectVerb(Uresponse)
	else:
		response = Obligation(Uresponse)

	return response

# if no feeling words, looking for events
def DetectEvent(Uresponse):

	actions = []

	Uresponse = en.sentence.tag(Uresponse)

	Ur_words = [word for (word, tag) in Uresponse]

	for (word, tag) in Uresponse:
		if tag[0:2]=="VB" and not tag=="VBN" and not re.match(stopwords, stemmer.stem(word)) and word[-3:]!= "ing":
			# print "Verb of interest!", stemmer.stem(word)
			if stemmer.stem(word)!=None:
				actions.append(stemmer.stem(word))
			else:
				actions.append(word)
		elif tag[0:2]=="VB" and not tag=="VBN" and not re.match(stopwords, stemmer.stem(word)) and word[-3:]== "ing":
			# print "ing verb of interest", stemmer.stem(word)
			if stemmer.stem(word)!=None:
				actions.append(stemmer.stem(word))
			else:
				actions.append(word)
		elif tag[0:2]=="VB" and not re.match(stopwords, word) and tag=="VBN":
			# print "potential passive!", stemmer.stem(word)
			if stemmer.stem(word)!= None:
				actions.append(stemmer.stem(word))
			else:
				actions.append(word)

	if len(actions)==0:
		return False

	else:
		# get longest verb - cheap way to look for "interest"
		actions.sort(key=len)
		# make longest verb into a gerund, return it
		return en.verb.present_participle(actions[-1])

# Wild deviation from course of conversation.
def Absurd(nym):

	wildgloss = en.noun.absurd_gloss(nym)
	if wildgloss=="":
		return False
	else:
		response = "Well, as everyone knows, %s is %s. Given that, how do you feel about it?"%(nym, wildgloss)
		return response

# Abstract away from noun
def Hypernym(nym):
	print "hypernym"
	if len(en.list.flatten(en.noun.hypernym(nym)))>1:
		hypernym = en.list.flatten(en.noun.hypernym(nym))[0]
		sing_nym = en.noun.singular(nym)
		response = "As long as %s is on your mind, let us step back and look at %s. What are your thoughts?"%(sing_nym, hypernym)
		return response
	else:
		return False

# Find a related concept to noun
def Meronym(nym):
	print "meronym"
	if len(en.list.flatten(en.noun.meronym(nym)))>1:
		meronym = en.noun.plural(en.list.flatten(en.noun.meronym(nym))[0])
		plu_nym = en.noun.plural(nym)
		response = "Related to %s, what do %s mean to you?"%(plu_nym, meronym)
		return response
	else:
		return False

# Go up a category from the noun of choice
def LexName(nym):
	print "category"
	category = en.noun.lexname(nym)
	if category == "":
		return False
	else:
		response = "How do you feel %s has affected you more generally?"%(category)
		return response

# Ask after the opposite
def Antonym(nym):
	print "antonym"
	antonym = en.noun.antonym(nym)
	if antonym=="":
		return False
	else:
		response = "Given how you feel about %s, what do you think about %s?"%(nym, antonym)
		return response

# if no feelings or events, assess nouns for significance
def DownToNouns(Uresponse, count):

	noun_handler = [Hypernym, Meronym, LexName, Antonym]

	op = random.choice(noun_handler)

	# tag actual response
	Uresponse = en.sentence.tag(Uresponse)

	# get just the nouns (I tried to do a list comprehension, but couldn't get it to work)
	nouns = []
	for (word, tag) in Uresponse:
		if tag[:2]=="NN":
			nouns.append(word)
		else:
			pass

	#pick the longest one (shorthand for "most interesting")
	if len(nouns) >= 2:
		nym = random.choice(nouns)
		print nym

		# every nineteen exchanges, it just goes off on a tangent
		if count==19:
			response = Absurd(nym)
		else:
			print "picking a process"
			response = op(nym)
			print response
			return response
	else:
		return False

# if failed all other tests, get generic more info
def Generics(patient):

	possibilities = ["Hey %s, tell me about the single most occupying thought in your mind.", \
	"I am not sure we are making the kind of progress I would like us to, %s. Tell me what is in your heart.",\
	"I am not a native speaker, so sometimes turns of phrase confuse me, %s. Try telling me about yourself in complete sentences.",\
	"Hmm, I can't detect your true feelings or the pivotal event from what you have said. That may be my command of English, sorry, %s. Tell me how you feel, please."]
	possibility = random.choice(possibilities)
	response = possibility%(patient)
	return response

# Dispatch processing of user input
def ProcessInput(therapist, patient, Uresponse, last_Uresponse):
	
	# separate user inputs that require processing from those that don't
	if InputBattery(Uresponse, last_Uresponse)==False:

		# look for stock phrases I've decided are likely.
		if BuiltIns(Uresponse)==False:

			# look for feelings-words
			if DetectFeels(Uresponse)==False:

				#look at nouns
				if DownToNouns(Uresponse, count)==False:

					# look for events
					if DetectEvent(Uresponse)==False:

							#last resort is a generic solicitor for more info
							response = Generics(patient)
					else:
						event = DetectEvent(Uresponse)
						response = "How is the %s making you feel?"%(event)
				else:
					response = DownToNouns(Uresponse, count)

			else:
				feel, feelkind = DetectFeels(Uresponse)
				if feelkind=="noun":
					response = Therapist.noun(therapist, feel)
				elif feelkind=="adj":
					response = Therapist.adj(therapist, feel)
				elif feelkind=="adv":
					response = Therapist.adv(therapist, feel)
				elif feelkind=="verb":
					response = Therapist.verb(therapist, feel)		
		else:
			response = BuiltIns(Uresponse)

	# if input fails initial battery, go-to operations apply
	else:
		op = InputBattery(Uresponse, last_Uresponse)
		if op == "Farewell":
			response = Therapist.Farewell(therapist)
		elif op=="Repeater":
			response = Therapist.Repeater(therapist)
		elif op == "getMore":
			response = Therapist.getMore(therapist)
		elif op=="Hostile":
			response = Therapist.Hostile(therapist)
		else:
			response = Therapist.NotMe(therapist)

	return response

# swap first and second person pronouns
def Pronounify(response):

	tokenized_ur = nltk.word_tokenize(response)
	ur_tagged = nltk.pos_tag(tokenized_ur)
	print ur_tagged

	partial_prons = {"I":"you","me":"you","you":"I","my":"your","My":"Your","Me":"You","You":"I", \
	"They":"They","they":"they","we":"we","We":"We","Y'all":"We all","y'all":"we all"}

	partial_ur = [x if v[:3]!="PRP" else partial_prons[x] for (x,v) in ur_tagged]

	response = string.join(partial_ur)

	return response

# Tailor output by therapist personality
def Stylize(therapist, patient, response):

	N_type_replacements = {"ing ":"in' ","You\b":"ya\b","you\b":"ya\b", \
	" is ":"'s ", "\bare\b":"'re\b", "\bhave\b":"'ve\b"}

	if Therapist.getStyle(therapist)=="NG":
		response = response
	else:
		for key in N_type_replacements.keys():
			response = re.sub(key, N_type_replacements[key], response)
		punct = response[-1]
		response = response[:-1]
		response[0].upper()
		petname = Therapist.petname(therapist, patient)
		response = "%s, %s%s"%(response, petname, punct)

	return response

# Handle conversation for 25 exchanges
def Dialogue(therapist, patient, Uresponse, last_Uresponse, count):
	while count < 25:
		response = ProcessInput(therapist, patient, Uresponse, last_Uresponse)
		if response == Therapist.Farewell(therapist):
			break
		else:
			last_Uresponse = Uresponse
			response = "\n%s\n"%(Stylize(therapist, patient, response))
			Uresponse = raw_input(response)
			return Dialogue(therapist, patient, Uresponse, last_Uresponse, count)

	print Therapist.Farewell(therapist)

# get things going
last_Uresponse = ""
therapist, patient, Uresponse = InitializeSession()

# initialize count to put a cap on the conversation
count =0

# Hand off conversation for 25 exchanges.
Dialogue(therapist, patient, Uresponse, last_Uresponse, count)

















