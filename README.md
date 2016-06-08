# AZILE-partners
A fun variation on ELIZA

Azile Partners README

About:

Azile Partners is a primitive chatbot with superficially different personalities. You can call it from the command line (in the directory in which you’ve saved it) with ‘python Azile.py’ 

Azile includes the same triggers as the original ELIZA, but with adjustments and additions, including the personalities. Personalities can be individually adjusted (or added to!) by changing the .txt files in Azile/therapists/personality_support_files. 

Support files:

Everything is set up to work if left in this file configuration:

Azile (folder)
  Azile_Partners.py
  therapist.py
  therapists (folder)
    therapy_personalities
    personality_support_files (folder)
      [everything with the format Name_responses, Name_petnames, Name_leaders, or Name_dialect]

- that is, everything in the Azile folder. To start, there are personalities named Willy, Lizzy, Jim, Eliza (of course), Daria, Brady, and Caroline.

All personalities have dictionaries of the same response triggers and their attendant answers, with minor changes between personalities. More fun and more noticeable to change are the dictionaries of dialectic replacement and pet names (and, to a lesser extent, leaders). If you don’t see a change in the pet names or leaders right away, you may want to adjust the frequency with which the personality applies them, a figure found in Azile/therapists/therapy_personalities.txt
