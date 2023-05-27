import math
from enum import Enum
import random

# debug flags
debug_flag_info = "[INFO]"
debug_flag_error = "[ERROR]"
debug_flag_output = "[OUT]"
debug_flag_input = "[IN] "


# char_class enums
class CharClass(Enum):
    BRAWLER = 0
    SWORDSMAN = 1
    MARKSMAN = 2
    ROGUE = 3
    WARRIOR = 4
    SPECIALIST = 5


class CharRace(Enum):
    HUMAN = 0
    FISHMAN = 1
    MINK = 2
    SKYISLANDER = 3
    AMAZONESS = 4
    TONTATTA = 5


def enumClassToString(enum):
    if enum == CharClass.BRAWLER:
        return "Brawler"
    elif enum == CharClass.SWORDSMAN:
        return "Swordsman"
    elif enum == CharClass.MARKSMAN:
        return "Marksman"
    elif enum == CharClass.ROGUE:
        return "Rogue"
    elif enum == CharClass.WARRIOR:
        return "Warrior"
    elif enum == CharClass.SPECIALIST:
        return "Specialist"


def enumRaceToString(enum):
    if enum == CharRace.HUMAN:
        return "Human"
    elif enum == CharRace.FISHMAN:
        return "Fishman"
    elif enum == CharRace.MINK:
        return "Mink"
    elif enum == CharRace.SKYISLANDER:
        return "Sky Islander"
    elif enum == CharRace.AMAZONESS:
        return "Amazoness"
    elif enum == CharRace.TONTATTA:
        return "Tontatta"


def spend_attribute_points(points, level, class_):
    points += 6 * 8
    val_list = [(8 + random.randint(0, points)) for x in range(6)]
    score = sum(val_list)
    while score > points:
        val_list.sort()
        if val_list[1] > 9:
            decrease = 0
        # third best stat max at 14
        elif val_list[3] > 14:
            decrease = 3
        # max value is 24
        elif val_list[5] > 24:
            decrease = 5
        # no character with a level lower than 5 should have values above 16
        elif level < 5 and val_list[5] > 16:
            decrease = 5
        else:
            decrease = random.randint(0, 5)
        if level >= 10:
            while val_list[decrease] < 10:
                decrease = random.randint(0, 5)
        else:
            while val_list[decrease] < 9:
                decrease = random.randint(0, 5)
        val_list[decrease] -= 1
        score = sum(val_list)

    if class_ == CharClass.BRAWLER:
        val_list.sort()
        int_, cha_, dex_, wis_, con_, str_ = val_list
    elif class_ == CharClass.WARRIOR:
        val_list.sort()
        wis_, int_, cha_, dex_, str_, con_ = val_list
    elif class_ == CharClass.SWORDSMAN:
        val_list.sort()
        wis_, int_, cha_, con_, dex_, str_ = val_list
    elif class_ == CharClass.MARKSMAN:
        val_list.sort()
        str_, con_, wis_, int_, cha_, dex_ = val_list
    elif class_ == CharClass.ROGUE:
        val_list.sort()
        con_, wis_, int_, str_, cha_, dex_ = val_list
    else:
        random.shuffle(val_list)
        con_, dex_, str_, wis_, int_, cha_ = val_list
    return con_, dex_, str_, wis_, int_, cha_


def calculatePointsToSpend(level):
    points = 22
    # TODO: add race specific boni
    # if race == CharRace.HUMAN:
    #     points += 2

    # points earned for reaching specific levels
    if level >= 4:
        points += 2
    if level >= 8:
        points += 2
    if level >= 10:
        points += 6
    if level >= 12:
        points += 2
    if level >= 16:
        points += 2
    if level >= 20:
        points += 8

    return points


def calcModifier(score):
    return math.floor((score - 10) / 2)


def calculatePrimarySkills(class_, strength, dex, intelligence, constitution, wisdom, fav_rank, unfav_rank):
    base_attack = []
    # calculate skills based on OPD20 formular
    if strength > dex:
        ua = strength
        base_attack.append("STR")
        wa = strength
        base_attack.append("STR")
    else:
        ua = dex
        base_attack.append("DEX")
        wa = dex
        base_attack.append("DEX")

    # ranged shot is either dex or wis
    if wisdom > dex:
        rs = wisdom
        base_attack.append("WIS")
    else:
        rs = dex
        base_attack.append("DEX")

    # defense and initiative is either dex or int
    if intelligence > dex:
        defense = intelligence
        base_attack.append("INT")
        init = intelligence
        base_attack.append("INT")
    else:
        defense = dex
        base_attack.append("DEX")
        init = dex
        base_attack.append("DEX")


    refsav = dex
    fortsav = constitution
    willsav = wisdom

    # 0 = weapon attack, 1 = unarmed strike, 2 = ranged shot, 3 = defense, 4 = initiative, 5 = fortitude save, 6 = reflex save, 7 = willpower save
    favored = []
    unfavored = []
    if class_ == CharClass.BRAWLER:
        favored.append(2)
        favored.append(3)
        favored.append(6)
    if class_ == CharClass.WARRIOR:
        favored.append(3)
        favored.append(0)
    if class_ == CharClass.SWORDSMAN:
        favored.append(0)
    if class_ == CharClass.MARKSMAN:
        favored.append(2)
    if class_ == CharClass.ROGUE:
        favored.append(0)
    while len(favored) < 4:
        rand = random.randint(0, 7)
        if rand not in favored:
            favored.append(rand)
    for x in range(0, 8):
        if x not in favored:
            unfavored.append(x)
    skills = [wa, ua, rs, defense, init, fortsav, refsav, willsav, favored, unfavored, base_attack]
    for element in favored:
        skills[element] += fav_rank
    for element in unfavored:
        skills[element] += unfav_rank
    return skills
