##!/usr/bin/python
##
## September 13, 2015
## Author: Rebecca Lovering 
## Class: Language Technology (taught by Andrew Rosenberg at CUNY GC)
##
import re
#import gdbm
import random
import string
import nltk
from string import *

## Personality-dependent variables:

vocatives = {"a":["sport","buddy","champ","tiger","bud","hotshot",\
"killer","buster","kid","kiddo","lil buddy","lil champ","ace","slugger","squirt","shaver"], \
"b":["you gorgeous thing, you","you shining star","you adorable creature","you divine person",\
"pet","love","darling","lamb","babe","sweetie","honey","sweetheart","sugar","dear"]}

getmore = {"a":["What else ya got cookin'", "Whatcha thinkin' about now"], \
"b":["Can you get under that to how you're feeling", "Tell me more, why don't you", "Go on; how did it make you feel"]}

intros = {"a":"\nHey there %s, I'm Jim.",\
"b":"\nWhy, hello there %s, I'm Lizzie!",\
"c":"\nHello %s, I am Eliza."}

greetings = {"a":"\nHiya, %s, what's on your mind?\n",\
"b":"\nWell alrighty, %s, what's on your mind today?\n",\
"c":"\nHello %s. What is on your mind?\n"}

farewell = {"a":"Well, I'm afraid we have to wrap it up. Come by again sometime!",\
"b":"Sugar pie, I'm afraid we are out of time today. You come on back if you want to chat again, though!",\
"c":"That is all I can do for today. Please come talk again another time."}

## Initialize with greeting and menu of options

def CharacterCheck(character):

	if character in vocatives.keys():	
		return character
	else:
		character = raw_input("I'm afraid that wasn't one of the options. \nPlease pick again, from the options listed above.\n")
		return CharacterCheck(character)

def NameCheck(name):

	namen = ""
	tokenized_name = nltk.word_tokenize(name)
	name_tagged = nltk.pos_tag(tokenized_name)
	name_tags = [x[1] for x in name_tagged]

	if "NNP" in name_tags:
		ind = name_tags.index("NNP")
		name = name_tagged[ind][0]
		print name

	else:
		name = raw_input("I'm sorry, I didn't catch that. Please enter your name:\n")
		NameCheck(name)

	return name

def Introduction():

	print "\n Welcome to reLIZA! We have a couple of personalities to chooose from:\n\
	\n a = avuncular\n\
	\n b = bubbly"

	character = (raw_input("\nWhat kind of therapy experience would you find most helpful today?\n\n")).lower()
	character = CharacterCheck(character)

	pet_names = vocatives[character]
	last_petname = random.choice(pet_names)

	print intros[character]%(last_petname)

## Get patient name
	name = raw_input("What's your name?\n\n")

	name = NameCheck(name)

	first_Uresponse = raw_input(greetings[character]%(name))

	return first_Uresponse, character, pet_names, last_petname, name

## Replace 1st person with 2nd person pronouns

def Pronounify(ur_tagged):

	partial_prons = {"I":"you","me":"you","you":"I","Me":"You","You":"I", \
	"They":"They","they":"they","your":"my","It":"it","it":"it","we":"we","We":"We","Y'all":"We all","y'all":"we all"}

	print ur_tagged
	
	partial_ur = [x if v[:3]!="PRP" else partial_prons[x] for (x,v) in ur_tagged]
	
	answer = string.join(partial_ur)
	
	return answer

def DangerZone(user_response):

	suicidetrigger = re.search(r".*?[sS]uicid(e|al).*?", user_response)
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

def Punctualize(answer):

	punct = [".",",","!"]

	if answer[-1] in punct:
		answer = answer[:-1]
	elif answer[-1] == "?":
		answer = raw_input("\nI don't know, what do you think?\n")
	answer = answer.capitalize()

	return answer

def YesNo(answer, character):

	YeaNayPattern = re.compile(r'(([Yy](e(s|ah))|up)|([Nn](o|ot really)))')

	if re.match(YeaNayPattern, answer) or len(answer) < 2 :
		answer = random.choice(getmore[character])
	else:
		answer = answer

	return answer

def PetNamer(last_petname,pet_names, answer):
	
	pet_tag = random.choice(pet_names)

	while pet_tag == last_petname:
		pet_tag = random.choice(pet_names)

	answer = answer+", %s"%(pet_tag)
	return answer

def SimpleReflect(answer):

	return "%s, huh"%(answer)

def Challenge(answer):

	answer = answer.split()
	answer[0] = answer[0].lower()
	answer = string.join(answer)

	answer = "Do you REALLY think %s"%(answer)
	return answer

def SubjectChange(answer):

	answer_parts = answer.split()
	answer_parts = sorted(answer_parts, key = len)
	topic = answer_parts[-1]

	answer = "I'm not sure talking about %s is helping us make progress.\n\
	 Tell me something else about yourself, okay"%(topic)
	return answer
	
def Creativize(answer):

	AnswerTypes = [SimpleReflect, Challenge]
	#SubjectChange

	RandomAnswer = random.choice(AnswerTypes)

	answer = RandomAnswer(answer)
	return answer

def CheckIllegals(answer):

	illegals = {"you'm":"you're", "You'm":"You're", "i'm":"I'm", "'m":"are"}

	illegals = dict((re.escape(k), v) for k, v in illegals.iteritems())
	pattern = re.compile("|".join(illegals.keys()))
	answer = pattern.sub(lambda m: illegals[re.escape(m.group(0))], answer)
	return answer

def GenerateAnswer(user_response, count, character):
	while count < 20:
		if DangerZone(user_response) == True:
			break
		#elif Incomp(user_response) == True:
			#answer = getmore[character]
		else:

			last_response = user_response

			tokenized_ur = nltk.word_tokenize(user_response)
			ur_tagged = nltk.pos_tag(tokenized_ur)

			answer = Pronounify(ur_tagged)

			answer = Punctualize(answer)

			#check to see if answer is just yes or no
			answer1 = YesNo(answer, character)
			if answer1 == answer:
				answer = Creativize(answer)
			else:
				answer = answer1

			#check illegal combinations
			answer = CheckIllegals(answer)

			answer = PetNamer(last_petname,pet_names, answer)

			user_response = raw_input("\n%s?\n"%(answer))
			
			if user_response == last_response:
				user_response = raw_input("\nWe can't make progress if you just repeat yourself! Tell me something new.\n")

			count = count+1

			GenerateAnswer(user_response, count, character)
	
first_Uresponse, character, pet_names, last_petname, name = Introduction()

count = 0

GenerateAnswer(first_Uresponse, count, character)

print farewell[character]

