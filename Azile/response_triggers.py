import re
from typing import Optional
from random import random

# regexes for all the categories triggered in the original Eliza
RESPONSE_TRIGGERS = {}

grouping_patterns = {
    "lizcant": (re.compile(r".*([Yy]ou (can't|cannot)(.*))"), 3),
    "lizdoesnt": (re.compile(r".*([Yy]ou (don't|do not)(.*))"), 3),
    "lizis": (re.compile(r".*([Yy]ou('re| are)(.*))"), 3),
    "Icant": (re.compile(r".*(I can('t|not)(.*))"), 3),
    "Idont": (re.compile(r".*(I do(n't| not)(.*))"), 3),
    "Iwant": (re.compile(r".*(I (want|wish) (.*))"), 3),
    "Ifeel": (re.compile(r".*(I feel (.*))"), 2),
    "Ithink": (re.compile(r".*(I think (.*))"), 2),
    "your": (re.compile(r".*[Yy]our (\w*)?"), 1),
}

simple_patterns = {
    "sorry": re.compile(r"(.*[Ss]orry.*)"),
    "maybe": re.compile(r"(.*[Mm]aybe.*)"),
    "friends": re.compile(r"(.*[Ff]riends?.*)"),
    "computer": re.compile(r"(.*[Cc]omputers?.*)"),
    "yes": re.compile(r"(.*[Yy](eah|es|up).*)"),
    "no": re.compile(r"(.*\b[Nn]o(t really)?\b.*)"),
    "hostile": re.compile(r".*([Ff]uck|FUCK|SHIT|DAMN|[Ss]hit|[Ss]hit(ty)?|[Dd]amn).*"),
    "goodbye": re.compile(r"(([Gg]ood)?[Bb]ye)"),
    "suicide": re.compile(r".*?(([sS]uicid(e|al))|[Kk]ill(ing)? myself).*?"),
    "selfharm": re.compile(r".*?h(arm|urt)(ing)? myself.*?"),
}


class ResponseTrigger:
    def __init__(self, name: str, pattern: str, group: Optional[int] = None) -> None:
        self.name = name
        self.pattern = pattern
        self.group = group

    def _compose_frame_and_fill(self, match_item):
        if self.group is not None:
            frame, fill = self.name, match_item.group(self.group)
        else:
            frame, fill = self.name
        return frame, fill

    def respond(self, utterance: str):
        found = re.search(self.pattern, utterance)
        if found is not None:
            return self._compose_frame_and_fill(found)
        else:
            return False


class IsLike(ResponseTrigger):
    """
    Identifies and composes response frame for comparison statements
    """

    def __init__(self) -> None:
        name = "islike"
        pattern = re.compile(
            r".*(((is|'s)|seems|([Yy]ou('re| are))) (like|as though) (.*))"
        )
        super().__init__(name, pattern, None)

    def _compose_frame_and_fill(self, match_item):
        if len(match_item.group(7)) > 1:
            frame = random.choice(["belikeNP", "compare"])
            match frame:
                case "compare":
                    fill = match_item.group(7)
                case "belikeNP":
                    fill = ""
            return frame, fill
        else:
            return False


# class Iam(ResponseTrigger):
#     """
#     Identifies, composes response for "I am" statements
#     """

#     def __init__(self) -> None:
#         name = "iam"
#         pattern = re.compile(r".*(([Ii]'m|[Ii] am)(.*))")
#         super().__init__(name, pattern, None)

#     def _compose_frame_and_fill(self, match_item):
#         if len(match_item.group(3)) > 1:
#             tokens = nltk.word_tokenize(match_item.group(3))
#             tagged_tokens = nltk.pos_tag(tokens)
#             if tagged_tokens[1][1] == "VBG":
#                 frame, fill = "IamGerund", match_item.group(3)
#             else:
#                 frame, fill = "Iam", match_item.group(3)
#             return frame, fill
#         else:
#             return False


class MutuallyExclusiveOrdered(ResponseTrigger):
    def __init__(
        self, name: str, pattern1: str, pattern2: str, group: Optional[int] = None
    ) -> None:
        name = name
        self.pattern1 = pattern1
        self.pattern2 = pattern2
        super().__init__(name, pattern1, group)

    def respond(self, utterance: str):
        if re.match(self.pattern1, utterance) and not re.match(
            self.pattern2, utterance
        ):
            return self.name, ""
        else:
            return False


class NotMe(MutuallyExclusiveOrdered):
    """checks to make sure patient is talking about him/her self"""

    def __init__(self) -> None:
        name = "notme"
        pattern1 = re.compile(r"(.*?\byou(('re|r)?\b).*)")
        pattern2 = re.compile(r"(.*?\b(I(\b|'m)|[mM](e|y)|[wW]e)\b)")
        super().__init__(name, pattern1, pattern2)


def populate_triggers():
    group_triggers = {
        key: ResponseTrigger(
            name=key, pattern=grouping_patterns[key][0], group=grouping_patterns[key][1]
        )
        for key in grouping_patterns
    }
    simple_triggers = {
        key: ResponseTrigger(name=key, pattern=simple_patterns[key])
        for key in simple_patterns
    }
    complex_triggers = {"islike": IsLike()}  # "iam": Iam(),
    return {**group_triggers, **simple_triggers, **complex_triggers}


RESPONSE_TRIGGERS = populate_triggers()
