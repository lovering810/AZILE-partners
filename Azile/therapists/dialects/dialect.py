import spacy
import string

nlp = spacy.load("en_core_web_sm")


class Dialect:
    def __init__(self, register: str) -> None:
        self.register = register

    @staticmethod
    def gerundify(token: spacy.tokens.Token) -> str:
        revisor = token.text
        revisor[-1] = "'"
        return revisor

    def mod_gerunds(self, doc: spacy.tokens.Doc) -> spacy.tokens.Doc:
        words = [
            self.gerundify(token.text) if token.tag_ == "VBG" else token.text
            for token in doc
        ]
        rejoined = string.join(words)
        return nlp(rejoined)

    @staticmethod
    def auxify(token: spacy.tokens.Token) -> str:
        pass

    def mod_auxes(self, doc: spacy.tokens.Doc) -> spacy.tokens.Doc:
        words = [
            self.auxify(token.text) if token.pos_ == "AUX" else token.text
            for token in doc
        ]
        rejoined = string.join(words)
        return nlp(rejoined)


class Responder:
    def __init__(self, gerunds: bool, pronouns: bool) -> None:
        self.gerunds = gerunds
        self.pronouns = pronouns

    @staticmethod
    def _make_doc(utterance: str):
        return nlp(utterance)

    def apply_dialect(self, utterance: str):
        pass

    def respond(self, utterance: str):
        pass
