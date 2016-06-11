# AZILE-partners
A fun variation on ELIZA

Azile Partners README

About:

Azile Partners is a primitive chatbot with superficially different personalities. You can call it from the command line (in the directory in which you’ve saved it) with ‘python Azile.py’ 

You can see the original ELIZA code (as rendered for the website manifestation.com) in ELIZA_original.rtf. Azile includes the same triggers as the original ELIZA, but with adjustments and additions, including the personalities. Personalities can be individually adjusted (or added to!) by changing the .txt files in Azile/therapists/personality_support_files. 

Support files:

Everything is set up to work if left in this file configuration - that is, everything in the Azile folder. All personalities have dictionaries of the same response triggers and their attendant answers, with minor changes between personalities. More fun and more noticeable to change are the dictionaries of dialectic replacement and pet names (and, to a lesser extent, leaders). If you don’t see a change in the pet names or leaders right away, you may want to adjust the frequency with which the personality applies them, a figure found in Azile/therapists/therapy_personalities.txt

Further Info:

There are two other versions of this program in different states of completion. They attempt to be more responsive to content than surface forms, and one is intended to keep track of the conversation, completing when all information on a given issue is extracted, rather than purely on the number of exchanges. They are not in great working order (I decided to go for robust over nuanced) but I include them as examples of other avenues pursued. They’re in Azile/Other_Versions if you want to play around with them.
