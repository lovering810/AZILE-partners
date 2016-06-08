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
from Therapist_Class import Therapist
from Therapist_Class import therapist_directory
from string import *
from nltk.stem.snowball import SnowballStemmer
from stopwords import stopword_list
stemmer = SnowballStemmer("english")

original_responses = {\
"lizcant":["Don't you believe that I can %s?","Do you want me to be able to %s?"],\
"Icant":["How do you know you can't %s?","Have you tried to %s?","Perhaps you can %s now.",\
"Perhaps you would like to be able to %s?","Perhaps you don't want to %s.",\
"Do you want to be able to %s?",\
"Do you think you should be able to %s?","Why can't you %s?"],\
"lizis":["What makes you think I am %s?","Does it please you to believe I am %s?","Perhaps you would like to be %s?",\
"Do you sometimes wish you were %s?","Why are you interested in whether or not I am %s?","Would you prefer if I were not %s?",\
"Perhaps in your fantasies I am %s."],\
"Idont":["Don't you really %s?","Why don't you %s?","Do you wish you could %s?"],\
"Ifeel":["Do you often feel %s?","Do you enjoy feeling %s?"],\
"lizdoesnt":["Do you really believe that I don't %s?","Perhaps in good time I will %s.","Do you want me to %s?"],\
"Iam":["Did you come to me because you are %s?","How long have you been %s?","Do you believe it is normal to be %s?","Do you enjoy being %s?"],\
"IamGerund":["Did you come to me because you are %s?", "Do you like %s?","Do you think it is normal to be %s?"],\
"Iwant":["Why do you want %s?","Suppose you got %s.","What would you do if you got %s?","I sometimes also want %s."],\
"your":["Why are you concerned about my %s?","What about your own %s?"],\
"Ithink":["But you are not sure you %s?","Do you doubt you %s?"],\

"Iask":["Why do you ask?","Does that question interest you?","What answer would please you the most?",\
"What do you think?","Are such questions on your mind often?","What is it that you really want to know?",\
"Have you asked anyone else?","Have you asked such questions before?","What else comes to mind when you ask that?"],\
"because":["Is that the real reason?","Do any other reasons come to mind?","Does that reason explain anything else?","What other reasons might there be?"],\
"sorry":["Please do not apologize!","Apologies are not necessary.","What does apologizing make you feel?"],\
"idream":["What do your dreams suggest to you?","Do you dream often?","Who shows up in your dreams?","Are you disturbed by your dreams?"],\
"maybe":["Why the uncertain tone?","You do not seem quite certain.","You are not sure?"],\
"name":["Names do not interest me.","I do not care about names, please go on."],\
"no":["Are you saying no just to be negative?","You are being a bit negative.","Why not?","Are you sure?", "Why no?"],\
"yes":["You seem quite positive.","Are you sure?"],\
"friends":["Why do you bring up friends?","Do your friends worry you?","Do your friends pick on you?", "Are you sure you have any friends?","Perhaps your love for your friends worries you."],\
"computer":["Do computers worry you?","Are you talking about me in particular?",\
"Are you frightened by machines?","Does the prospect of a fully self-aware machine disturb you?",\
"Why do you mention computers?","What do you think machines have to do with your problems?",\
"Don't you think computers can help people?","What is it about machines that worries you?"],\

"repeat":["Why did you repeat yourself?","Do you expect a different answer by repeating yourself?"],\
"notme":["We were discussing you, not me.","You can't really be talking about me."],\
"belikeNP":["In what way?","What resemblance do you see?","What does the similarity suggest to you?","What other connections do you see?","Could there really be some connection?","How?"],\
"compare":["What makes that like %s?","How is that like %s?", "How is %s like that?","Why do you think %s is like that?"],\
"generic":["Does that bother you?","Tell me more about those feelings.","What are you thinking of?","What makes you say that?","I see.",\
"I understand.","Say, do you have any psychological problems?","I'm not sure I understand you fully.",\
"Can you elaborate on that?","That is quite interesting."]}

liz_cant = re.compile(r".*([Yy]ou (can't|cannot)(.*))")
liz_doesnt = re.compile(r".*([Yy]ou (don't|do not)(.*))")
liz_is = re.compile(r".*([Yy]ou('re| are)(.*))")
I_cant = re.compile(r".*(I can('t|not)(.*))")
I_dont = re.compile(r".*(I do(n't| not)(.*))")
I_am = re.compile(r".*((I'm|I am)(.*))")
I_feel = re.compile(r'.*(I feel (.*))')
I_want = re.compile(r'.*(I (want|wish) (.*))')
I_think = re.compile(r'.*(I think (.*))')
your = re.compile(r'.*(your (\w*?))')

sorry = re.compile(r'(.*[Ss]orry.*)')
maybe = re.compile(r'(.*[Mm]aybe.*)')
friends = re.compile(r'(.*[Ff]riends?.*)')
computer = re.compile(r'(.*[Cc]omputers?.*)')
yes = re.compile(r'(.*[Yy](eah|es|up).*)')
no = re.compile(r'(.*[Nn]o(t really)?.*)')

is_like = re.compile(r".*(((is|'s)|seems|([Yy]ou('re| are))) (like|as though) (.*))")

HostilePattern = re.compile(r'(.*([Ff]uck|[Ss]hit(ty)?|[Dd]amn).*)')

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
	elif I_Am_S and len(I_Am_S.group(3))>1:
		tokens = nltk.word_tokenize(I_Am_S.group(3))
		tagged_tokens = nltk.pos_tag(tokens)
		if tagged_tokens[0][1]=="VBG":
			frame, fill = "IamGerund",I_Am_S.group(3)
		else:
			frame, fill = "Iam", I_Am_S.group(3)
	elif Is_Like_S:

		frame = random.choice(["belikeNP","compare"])
		
		if frame == "compare":
			frame, fill = "compare", Is_Like_S.group(7)
		else:
			frame = "belikeNP"

	elif I_Feel_S:
		frame, fill = "Ifeel", I_Feel_S.group(2)
	elif I_Want_S:
		frame, fill = "Iwant", I_Want_S.group(3)
	elif I_Think_S:
		frame, fill = "Ithink", I_Think_S.group(2)
	elif Your_S:
		frame, fill = "your", Your_S.group(2)

	elif "?" in Uresponse:
		frame = "Iask"
	elif Sorry_S:
		frame = "sorry"
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
		response = random.choice(original_responses["notme"])
		return response
	else:
		return False

# looks for comparisons/similarities
def IsLike(Uresponse):
	Is_Like_S = re.search(is_like,Uresponse)
	if Is_Like_S:
		response = random.choice(original_responses["belikeNP"])
		return response
	else:
		return False

# Totally bland stuff that can go with anything - where we get when nothing else is there.
def Generics(Uresponse):
	response = random.choice(original_responses["generic"])
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
#(less important in this version of the program, but still makes a difference)
def ChooseTherapist():
	print "\nHello! Welcome to the ElIZA Partners! We have several partners available to talk to.\n"
		
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

	N_type_replacements = {"ing ":"in' "," are not ":" aren't "," do ":"d'","Do ":"D'","because":"'cause","You ":"ya ","you\b":"ya\b", \
	" is ":"'s ", "\bam\b":"'m ","\bwill\b":"'ll"," are ":"'re ", "\bnot\b":"n't\b","\bhave\b":"'ve\b","\bwould":"'d"}

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
				response = random.choice(original_responses["repeat"])

			else:
				# check for yelling
				if Uresponse==Uresponse.upper():
					response = Therapist.Hostile(therapist)

				else:
					# check for profanity
					if re.match(HostilePattern, Uresponse):
						response = Therapist.Hostile(therapist)
					else:
						# first level catches most things
						if RegExProcesses(Uresponse) != False:
							frame, fill = RegExProcesses(Uresponse)
							fill = Pronounify(fill)
							frame = random.choice(original_responses[frame])
							if fill == "":
								response = frame
							else:
								response = frame%fill
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

