#!/usr/bin/python
#
# September 13, 2015
# Author: Rebecca Lovering
# Class: Language Technology (taught by Andrew Rosenberg at CUNY GC)
#
"""A primitive chat bot that will engage a user for 25 exchanges\
 with any one of several personality skins overlaying the responses."""

from therapist import Therapist
from session import Session

# from string import *


def populate_directory():
    therapist_directory = {}
    fileget = "therapists/therapy_personalities.txt"
    with open(fileget, "r+w") as infile:
        personalities = infile.readlines()

    therapist_directory = {}

    # TODO: replace with grep through therapists dir
    for line in personalities:

        # Get basic info for personality
        name, kind, intro, farewell, prop_pn, prop_ld = line.split("/")

        therapist_directory[name] = Therapist(
            name, kind, intro, farewell, float(prop_pn), float(prop_ld)
        )

    return therapist_directory


# Check name input for proper noun.
# def NameCheck(name):

#     tokenized_name = nltk.word_tokenize(name)
#     name_tagged = nltk.pos_tag(tokenized_name)
#     name_tags = [x[1] for x in name_tagged]

#     if "NNP" in name_tags:
#         ind = name_tags.index("NNP")
#         name = name_tagged[ind][0]

#     else:
#         name = input("I'm sorry, I didn't catch that. Please enter your name:\n")
#         NameCheck(name)

#     return name


# Get patient name_input
def getPtName():

    name = input("What's your name?\n\n")

    # name = NameCheck(name)

    return name


# give user choice of personality
def ChooseTherapist(therapist_directory: dict) -> Therapist:
    print(
        "\nHello! Welcome to Azile Partners!\n\
    We have several partners available to talk to.\n"
    )

    for item in therapist_directory:
        print(f"{item}, {therapist_directory[item].kind}")

    therapist_choice = input("\nWho would you like as your therapist today?\n\n")

    if therapist_choice in therapist_directory.keys():

        therapist = therapist_directory[therapist_choice]

        print(f"\nAll set to talk to {therapist.name}.\n" % ())

        return therapist

    else:
        print(
            "\nI'm afraid that wasn't one of the options. \
        \nPlease choose again, and be sure to type the full name!\n"
        )
        return ChooseTherapist(therapist_directory)


# Get basic info for session (calls other functions)
def InitializeSession() -> Session:

    directory = populate_directory()
    therapist = ChooseTherapist(directory)

    patient = getPtName()

    return Session(patient=patient, therapist=therapist)


# get things going
InitializeSession()
