import random

# lists containing several actions that the bots can choose from (randomly if desired)
good_actionList = ["study", "train", "cook", "work", "read", "self-esteem", "walk"]
bad_actionList = ["fight", "steal", "swear", "stalk", "shout", "gossip", "bomb"]
extra_actionList = ["relax", "day-dream", "ski", "picnick", "bird-watch", "sew", "draw"]
all_actionList = good_actionList + bad_actionList


# Four different bots that return alternative responses according to the given arguments a and b (actions)
def alice(a, b=None):
    if b is None and a in good_actionList:
        result = "Alice: {} sounds like a good idea".format(a.capitalize() + "ing")
    elif b is None and a in bad_actionList:
        result = "Alice: Hmmm, I am not sure about {}. Can we not {} instead?".format(a + "ing", random.choice(extra_actionList))
    else:
        result = "Alice: I will join you for whatever you are planning."
    return result


def bob(a, b=None):
    if b is None:
        result = "Bob: I guess I could hang out with you for {}.".format(a + "ing")
    else:
        result = "Bob: Yeah, {} is possible. But we should rather consider {}.".format(a + "ing", b + "ing")
    return result


def musti(a, b=None):
    if b is None and a in bad_actionList:
        result = "Musti: I agree with Alice. {} is not a good idea.".format(a + "ing")
    elif b is not None and b in bad_actionList:
        result = "Musti: I would choose {} or {} in the forest rather than {}.".format(a + "ing", random.choice(extra_actionList), b + "ing")
    else:
        result = "Musti: How about {}?".format(random.choice(extra_actionList) + "ing")
    return result


def hellokitty(a, b=None):
    if b is None:
        result = "Hellokitty: {} might be fun!".format(a.capitalize() + "ing")
    elif a in bad_actionList:
        result = "Hellokitty: We did {} last time as well;-( We could try {} or {} this time.".format(a, b + "ing", random.choice(extra_actionList) + "ing")
    else:
        result = "Hellokitty: {} is fine for me! Let's move then!".format(a.capitalize() + "ing")
    return result
