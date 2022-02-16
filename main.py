import random
import csv
import pandas as pd

import constants as c

print(c.debug_flag_info, "Hello! This is One Piece D20 character generator")
print(c.debug_flag_info, "If you want to randomize any input, enter 'r'")

randomize_everything = True
if not randomize_everything:
    name_char = input(c.debug_flag_input + "Give your character a name:")
    level_char = int(input(c.debug_flag_input + "On what level should your character be?"))
    class_char = input(c.debug_flag_input + "What class do you want for the character?")

    print(c.debug_flag_info, f"Generating {name_char} as {c.enumToString(class_char)} on level: {level_char}")
else:
    name_char = "Random D. Name"
    level_char = random.randint(1, 20)
    class_char = random.choice(list(c.CharClass))
    print(c.debug_flag_info, f"Generating {name_char} as {c.enumToString(class_char)} on level: {level_char}")

favored_ranks = [0]
for level in range(0, 20):
    favored_ranks.append(level + 4)

unfavored_ranks = [0]
ranks = 1
for level in range(1, 21):
    if level % 2 == 0:
        ranks += 1
        unfavored_ranks.append(ranks)
    else:
        unfavored_ranks.append(ranks)

feats = [0]
number_of_feats = 4
for level in range(1, 21):
    if level % 2 == 0:
        number_of_feats += 2
        feats.append(number_of_feats)
    else:
        number_of_feats += 1
        feats.append(number_of_feats)

char_num_of_feats = feats[level_char]
char_unfavored = unfavored_ranks[level_char]
char_favored = favored_ranks[level_char]




# attributes
con_attr_char, dex_attr_char, str_attr_char, wis_attr_char, int_attr_char, cha_attr_char \
    = c.spendAttributePoints(c.calculatePointsToSpend(level_char), level_char, class_char)

# modifiers
con_mod_char = c.calcModifier(con_attr_char)
str_mod_char = c.calcModifier(str_attr_char)
dex_mod_char = c.calcModifier(dex_attr_char)
wis_mod_char = c.calcModifier(wis_attr_char)
int_mod_char = c.calcModifier(int_attr_char)
cha_mod_char = c.calcModifier(cha_attr_char)

# health and damage reduction
hp_char = (5 + con_mod_char) * level_char
dr_char = level_char

# todo: pick favored primary skills
# 0 = unarmed strike, 1 = weapon attack, 2 = ranged shot, 3 = initiative, 4 = reflex save, 5 = fortitude save, 6 = willpower save
primary_skills = c.calculatePrimarySkills(class_char, str_mod_char, dex_mod_char, int_mod_char, con_mod_char, wis_mod_char, char_favored, char_unfavored)
data = {'Name': name_char, 'Race': "Human", 'Class': c.enumToString(class_char), "Level": level_char, "HP": hp_char, "DR": dr_char}
attribute_stats = {"STR": str_attr_char, "DEX": dex_attr_char, "CON": con_attr_char, "WIS": wis_attr_char, "INT": int_attr_char, "CHA": cha_attr_char}
primary_stats = {"Unarmed Strike": primary_skills[0], "Weapon Attack": primary_skills[1], "Ranged Shot": primary_skills[2], "Initiative": primary_skills[3],
     "Reflex Save": primary_skills[4], "Fortitude Save": primary_skills[5], "Willpower Save": primary_skills[6], "Defense": primary_skills[7]}

df_attributes = pd.DataFrame(attribute_stats, index=[1])
df_primaries = pd.DataFrame(primary_stats, index=[1])


def generateHTML():
    text = f'''
    <html>
        <body>
            <h1>{data["Name"]}</h1>
            <h2>{data["Race"]} {data["Class"]}</h2>
            <h2>Level: {level_char} / HP: {hp_char} / DR: {dr_char}</h2>
            <h3>{df_attributes.to_html()}</h3>
            <h3>{df_primaries.to_html()}</h3>

        </body>
    </html>
    '''
    # write to file
    with open('sheet.html', 'w') as file:
        writer = csv.writer(file)
        file.write(text)
        #for key, value in data.items():
            #writer.writerow([key, value])

generateHTML()
print(c.debug_flag_info, "Finished generating Pirate. Have fun!")