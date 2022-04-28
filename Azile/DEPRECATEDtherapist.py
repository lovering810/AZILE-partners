#!/usr/bin/python
#
# September 13, 2015
# Author: Rebecca Lovering
# Class: Language Technology (taught by Andrew Rosenberg at CUNY GC)
#
from datetime import timedelta
import random
from typing import Callable, Optional, Union
from string import join

import logging

logging.basicConfig()


class Therapist:
    def __init__(
        self,
        name: str = "Ted",
        kind: str = "default",
        intro: str = "Nice to meet you, I'm %s",
        farewell: str = "Bye now, %s",
        petname_likelihood: float = 0.5,
        leader_likelihood: float = 0.15,
    ):

        self.name = name
        self.kind = kind
        self.intro = intro
        self.farewell = farewell
        self.petname_likelihood = petname_likelihood
        self.leader_likelihood = leader_likelihood
        self.leaders = self.load_personality_aspect(aspect="leaders")
        self.petnames = self.load_personality_aspect(aspect="petnames")
        self.dialect = self.load_personality_aspect(
            aspect="dialect", split_logic=self._parse_dialect
        )
        self.response_dict = self.load_personality_aspect(
            aspect="responses", split_logic=self._parse_responses
        )

    def load_personality_aspect(
        self, aspect: str, split_logic: Optional[Callable] = None
    ) -> Union[dict, list]:
        try:
            with open(
                f"therapists/personality_support_files/{self.name}_{aspect}.txt"
            ) as infile:
                aspects = [aspect.strip() for aspect in infile.readlines()]
            if split_logic is not None:
                return split_logic(aspects)
            else:
                return aspects
        except FileNotFoundError as fe:
            logging.warn(f"No therapist file for that: {fe}")

    @staticmethod
    def _prononify(utterance) -> str:

        # tokenized_ur = nltk.word_tokenize(response)
        # ur_tagged = nltk.pos_tag(tokenized_ur)

        # ur_tagged = [(x, v) for (x, v) in ur_tagged if v!="."]

        partial_prons = {
            "I": "you",
            "me": "you",
            "you're": "I'm",
            "you": "I",
            "your": "my",
            "my": "your",
            "me": "you",
            "we": "we",
            "y'all": "we all",
        }

        partial_ur = [
            partial_prons[x.lower()] if x in partial_prons else x for x in utterance
        ]

        response = join(partial_ur)

        return response

    @staticmethod
    def _parse_dialect(lines: list) -> dict:
        dialect = {}
        for dialect_line in lines:
            key, content = dialect_line.split(":")
            dialect[key.strip()] = content.strip()
        return dialect

    @staticmethod
    def _parse_responses(lines: list) -> dict:
        response_dict = {}
        for line in lines:
            prompt, answer = line.split("/")
            response_dict[prompt] = answer.strip().split(";")
        return response_dict

    def _apply_dialect(self, utterance: str) -> str:
        return join(
            [
                self.dialect[word] if word in self.dialect else word
                for word in utterance.split()
            ]
        )

    def _leader(self):
        return random.choice(self.leaders)

    def _petname(self, patient_name):
        return random.choice(self.petnames) if len(self.petnames) > 1 else patient_name

    def introduce(self, patient_name):
        return self.intro.format(patient_name, self.name)

    def farewell(self, time_remaining: timedelta):
        if time_remaining < timedelta(minutes=10):
            return self.farewell
        else:
            return f"I know it's early, but now seems like the right time to close. {self.farewell}"

    def respond(self, key: str):
        response_list = self.response_dict[key]
        template = random.choice(response_list)
        return template
