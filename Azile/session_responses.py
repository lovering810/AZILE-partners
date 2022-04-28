from response_triggers import RESPONSE_TRIGGERS


def filter_utterance(utterance):
    utterance_filters = {
        f.name: f if f.filter(utterance) else None for f in RESPONSE_TRIGGERS
    }
    return utterance_filters


# Check response for dangerous triggers
def danger_zone(found_elements: list) -> bool:

    if "suicide" in found_elements:
        print(
            "Hey, all joking aside, suicide is a serious thing,\n\
         and if you're thinking about it, you should speak to a human. \n\
         You can call one at 1-800-273-8255, any time. \n"
        )
        return True
    elif "selfharm" in found_elements:
        print(
            "Self harm is serious stuff, and you should talk to a live human and get some help.\n\
        Try calling 1-800-273-TALK or 1-800-334-HELP, any time."
        )
        return True
    else:
        return False
