##!/usr/bin/python
##
## September 13, 2015
## Author: Rebecca Lovering 
## Class: Language Technology (taught by Andrew Rosenberg at CUNY GC)
##
'''A primitive chat bot that will engage a user for 25 exchanges\
 with any one of several personality skins overlaying the responses.'''
 
import re
import random
import string
import nltk
from therapist import Therapist
from therapist import therapist_directory
from string import *
#from stopwords import stopword_list

liz_cant = re.compile(r".*([Yy]ou (can't|cannot)(.*))")
liz_doesnt = re.compile(r".*([Yy]ou (don't|do not)(.*))")
liz_is = re.compile(r".*([Yy]ou('re| are)(.*))")
I_cant = re.compile(r".*(I can('t|not)(.*))")
I_dont = re.compile(r".*(I do(n't| not)(.*))")
I_am = re.compile(r".*((I'm|I am)(.*))")
I_feel = re.compile(r'.*(I feel (.*))')
I_want = re.compile(r'.*(I (want|wish) (.*))')
I_think = re.compile(r'.*(I think (.*))')
your = re.compile(r'.*[Yy]our (\w*)?')
sorry = re.compile(r'(.*[Ss]orry.*)')
maybe = re.compile(r'(.*[Mm]aybe.*)')
friends = re.compile(r'(.*[Ff]riends?.*)')
computer = re.compile(r'(.*[Cc]omputers?.*)')
yes = re.compile(r'(.*[Yy](eah|es|up).*)')
no = re.compile(r'(.*\b[Nn]o(t really)?\b.*)')
is_like = re.compile(r".*(((is|'s)|seems|([Yy]ou('re| are))) (like|as though) (.*))")
HostilePattern = re.compile(r'.*([Ff]uck|FUCK|SHIT|DAMN|[Ss]hit|[Dd]amn).*')

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

# regexes for all the categories triggered in the original Eliza
def RegExProcesses(Uresponse):

	fill = ""
	Liz_Cant_S = re.search(liz_cant, Uresponse)
	Liz_Doesnt_S = re.search(liz_doesnt, Uresponse)
	Liz_Is_S = re.search(liz_is, Uresponse)
	Is_Like_S = re.search(is_like, Uresponse)
	I_Cant_S = re.search(I_cant, Uresponse)
	I_Dont_S = re.search(I_dont, Uresponse)
	I_Am_S = re.search(I_am, Uresponse)

	I_Feel_S = re.search(I_feel, Uresponse)
	I_Want_S = re.search(I_want, Uresponse)
	I_Think_S = re.search(I_think, Uresponse)
	Your_S = re.search(your, Uresponse)

	Sorry_S = re.search(sorry, Uresponse)
	Maybe_S = re.search(maybe, Uresponse)
	Friends_S = re.search(friends, Uresponse)
	Computer_S = re.search(computer, Uresponse)
	Yes_S = re.search(yes, Uresponse)
	No_S = re.search(no, Uresponse)

	if Liz_Cant_S:
		frame, fill = "lizcant", Liz_Cant_S.group(3)
	elif Liz_Doesnt_S:
		frame, fill = "lizdoesnt", Liz_Doesnt_S.group(3)
	elif Liz_Is_S:
		frame, fill = "lizis", Liz_Is_S.group(3)
	elif I_Cant_S:
		frame, fill = "Icant", I_Cant_S.group(3)
	elif I_Dont_S:
		frame, fill = "Idont", I_Dont_S.group(3)
	elif Sorry_S:
		frame = "sorry"

	elif Is_Like_S:
		if len(Is_Like_S.group(7))>1:
			frame = random.choice(["belikeNP","compare"])
			if frame == "compare":
				frame, fill = "compare", Is_Like_S.group(7)
			else:
				frame = "belikeNP"

	elif I_Am_S and len(I_Am_S.group(3))>1:
		tokens = nltk.word_tokenize(I_Am_S.group(3))
		tagged_tokens = nltk.pos_tag(tokens)
		if tagged_tokens[1][1]=="VBG":
			frame, fill = "IamGerund",I_Am_S.group(3)
		else:
			frame, fill = "Iam", I_Am_S.group(3)


	elif I_Feel_S:
		frame, fill = "Ifeel", I_Feel_S.group(2)
	elif I_Want_S:
		frame, fill = "Iwant", I_Want_S.group(3)
	elif I_Think_S:
		frame, fill = "Ithink", I_Think_S.group(2)
	elif Your_S:
		frame, fill = "your", Your_S.group(1)

	elif "?" in Uresponse:
		frame = "Iask"
	elif Maybe_S:
		frame = "maybe"
	elif Friends_S:
		frame = "friends"
	elif Computer_S:
		frame = "computer"
	elif Yes_S:
		frame = "yes"
	elif No_S:
		frame = "no"
	else:
		return False


	return frame, fill

# checks to make sure patient is talking about him/her self
def NotMe(Uresponse):
	SecondPPattern = re.compile(r"(.*?\byou(('re|r)?\b).*)")
	FirstPPattern = re.compile(r"(.*?\b(I(\b|'m)|[mM](e|y)|[wW]e)\b)")
	if re.match(SecondPPattern, Uresponse) and not re.match(FirstPPattern, Uresponse):
		response = Therapist.respond(therapist,"notme")
		return response
	else:
		return False

# looks for comparisons/similarities
def IsLike(Uresponse):
	Is_Like_S = re.search(is_like,Uresponse)
	if Is_Like_S:
		response = Therapist.respond(therapist,"belikeNP")
		return response
	else:
		return False

# Totally bland stuff that can go with anything - where we get when nothing else is there.
def Generics(Uresponse):
	response = Therapist.respond(therapist,"generic")
	return response

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

# give user choice of personality 
def ChooseTherapist():
	print "\nHello! Welcome to Azile Partners!\n\
	We have several partners available to talk to.\n"
		
	for item in therapist_directory:
		print "%s\t(%s)"%(item, Therapist.getKind(therapist_directory[item]))

	therapist_choice = raw_input("\nWho would you like as your therapist today?\n\n")

	if therapist_choice in therapist_directory.keys():

		therapist = therapist_directory[therapist_choice]

		print "\nAll set to talk to %s.\n"%(Therapist.getName(therapist))

		return therapist

	else:
		print "\nI'm afraid that wasn't one of the options. \
		\nPlease choose again, and be sure to type the full name!\n"
		return ChooseTherapist()

# Tailor output by therapist personality
def Stylize(therapist, patient, response):

	N_type_replacements = Therapist.Dialect(therapist)

	if len(N_type_replacements.keys())==1:
		response[0].upper()
	else:
		for key in N_type_replacements.keys():
			response = re.sub(key, N_type_replacements[key], response)
		name_variable = random.random()
		ld_variable = random.random()
		if float(name_variable) < float(Therapist.prop_pn(therapist)):
			punct = response[-1]
			response = response[:-1]
			petname = Therapist.petname(therapist, patient)
			response = "%s, %s%s"%(response, petname, punct)

			if float(ld_variable) < float(Therapist.prop_ld(therapist)):
				leader = Therapist.getLeader(therapist)
				if response[0]!="I":
					resp2 = response[0].lower()
					response = response[1:]
					response = "%s %s%s"%(leader, resp2,response)
				else:
					response = "%s %s"%(leader, response)
			else:
				response = "%s"%(response)

	return response

# swap first and second person pronouns
def Pronounify(response):

	tokenized_ur = nltk.word_tokenize(response)
	ur_tagged = nltk.pos_tag(tokenized_ur)

	ur_tagged = [(x, v) for (x, v) in ur_tagged if v!="."]

	partial_prons = {"I":"you","it":"it","It":"It","me":"you","you're":"I'm","you":"I","your":"my","my":"your","My":"Your","Me":"You","You":"I", \
	"They":"They","they":"they","we":"we","We":"We","Y'all":"We all","y'all":"we all"}

	partial_ur = [x if v[:3]!="PRP" or x not in partial_prons.keys() else partial_prons[x] for (x,v) in ur_tagged]

	response = string.join(partial_ur)

	return response

# Get basic info for session (calls other functions)
def InitializeSession():

	therapist = ChooseTherapist()

	patient = getPtName()	

	first_Uresponse = raw_input("\n%s\n\n"%(Therapist.introduce(therapist,patient)))

	return therapist, patient, first_Uresponse

# Dispatch processing of user input
def ProcessInput(therapist, patient, Uresponse, last_Uresponse):

	# check for trigger words
	if DangerZone(Uresponse)==True:
		response = Therapist.Farewell(therapist)
	else:
		# check that user not trying to leave
		gbye = re.compile(r'(([Gg]ood)?[Bb]ye)')
		if re.search(gbye, Uresponse):
			response = Therapist.Farewell(therapist)
		else:

			# check for repetition
			if last_Uresponse==Uresponse:
				response = Therapist.respond(therapist,"repeat")

			else:
				# check for yelling
				if Uresponse==Uresponse.upper():
					response = Therapist.respond(therapist,"allcaps")

				else:
					# check for profanity
					if re.match(HostilePattern, Uresponse):
						response = Therapist.respond(therapist,"hostile")
					else:
						# first level catches most things
						if RegExProcesses(Uresponse) != False:
							frame, fill = RegExProcesses(Uresponse)
							fill = Pronounify(fill)
							frame = Therapist.respond(therapist,frame)
							if fill == "":
								response = frame
							else:
								response = frame%(fill)
						else:
							# checks to be sure user is talking about self
							if NotMe(Uresponse)!=False:
								response = NotMe(Uresponse)
							else:
								# look for comparisons
								if IsLike(Uresponse)!=False:
									response = IsLike(Uresponse)
								else:
									# last resort responses
									response = Generics(Uresponse)

	return response

# Handle conversation for 25 exchanges
def Dialogue(therapist, patient, Uresponse, last_Uresponse, count):
	while count < 25:
		response = ProcessInput(therapist, patient, Uresponse, last_Uresponse)
		if response == Therapist.Farewell(therapist):
			break
		else:
			last_Uresponse = Uresponse
			response = "\n%s\n\n"%(Stylize(therapist, patient, response))
			Uresponse = raw_input(response)
			count = count+1
			return Dialogue(therapist, patient, Uresponse, last_Uresponse, count)

	print "\n\n%s\n\n"%(Therapist.Farewell(therapist))

# get things going
last_Uresponse = ""
therapist, patient, Uresponse = InitializeSession()

# initialize count to put a cap on the conversation
count =0

# Hand off conversation for 25 exchanges.
Dialogue(therapist, patient, Uresponse, last_Uresponse, count)

