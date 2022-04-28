from therapist import Therapist
from datetime import datetime, timedelta
from random import random
import session_responses
import re


class Session:
    def __init__(self, patient, therapist: Therapist, length: int = 45) -> None:
        self.start_time = datetime.now()
        self.end_time = self.start_time + timedelta(minutes=length)
        self.therapist = therapist
        self.patient = patient
        self.patient_says = []
        self.therapist_says = []
        self.active = True
        self.aborted = False
        self.dialogue(input(self.therapist.introduce(self.patient)))

    def summarize(self):
        # TODO: add summary based on exchanges
        raise NotImplementedError

    def wrap_up(self):
        farewell = self.therapist.farewell(
            time_remaining=self.end_time - datetime.now()
        )
        if not self.aborted:
            summary = self.summarize()
            final_response = self.stylize(f"{summary}\n{farewell}")
            print(final_response)
        else:
            print(farewell)
        self.active = False
        exit

    # Tailor output by therapist personality
    def stylize(self, response):

        if len(self.therapist.dialect.keys()) == 1:
            response[0].upper()
        else:
            for key in self.therapist.dialect.keys():
                response = re.sub(key, self.therapist.dialect[key.lower()], response)
            name_variable = float(random())
            ld_variable = float(random())
            if name_variable < self.therapist.petname_likelihood:
                punct = response[-1]
                response = response[:-1]
                petname = self.therapist._petname(self.patient)
                response = f"{response}, {petname}{punct}"

                if ld_variable < self.therapist.leader_likelihood:
                    leader = self.therapist._leader
                    if response[0] != "I":
                        resp2 = response[0].lower()
                        response = response[1:]
                        response = f"{leader} {resp2}{response}"
                    else:
                        response = f"{leader} {response}"
                else:
                    response = f"{response}"

        return response

    # Process a single user utterance
    def process_input(self, utterance: str) -> str:

        last_said = str(self.patient_says[-1])
        self.patient_says.append(utterance)
        if utterance == utterance.upper():
            response_template = self.therapist.respond("allcaps")
        elif utterance == last_said:
            response_template = self.therapist.respond("repeat")

        utterance_filters = session_responses.filter_utterance(utterance)
        if not utterance_filters:
            response_template = self.therapist.respond("generic")

        # check for trigger words, bailing on the session
        if "suicide" in utterance_filters:
            self.active = False
            response_template = """
            Hey, all joking aside, suicide is a serious thing,
            and if you're thinking about it, you should speak to a human.
            You can call one at 1-800-273-8255, any time."""
        elif "selfharm" in utterance_filters:
            self.active = False
            response_template = """Self harm is serious stuff,
            and you should talk to a live human and get some help.
            Try calling 1-800-273-TALK or 1-800-334-HELP, any time."""
        elif "goodbye" in utterance_filters:
            self.active = False
            response_template = ""
        else:
            # TODO: address multiple filters on purpose (currently random)
            response_template = self.therapist.respond(
                key=random(utterance_filters.keys())
            )

        response = self.stylize(response_template)
        self.therapist_says.append(response)
        return response

    # Handle conversation for length of session
    def dialogue(self, utterance):
        while datetime.now() < self.end_time or self.active:
            response = self.process_input(utterance)
            return self.dialogue(input(response))
        self.wrap_up()
