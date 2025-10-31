import json

class Character:
    def __init__(self, name: str, race: str, type: str, ac: str, hp_tot: int, hp_cur: int,
                 bleed: bool, bleed_remain: int, disorient: bool, disorient_remain: int,
                 crack: bool, crack_remain: int, impale: bool, impale_remain: int, disarm: bool,
                 disarm_remain: int, weapon_1: object, weapon_2: object):
        self.name = name
        self.race = race
        self.type = type
        self.ac = ac
        self.hp_tot = hp_tot
        self.hp_cur = hp_cur
        self.bleed = bleed
        self.bleed_remain = bleed_remain
        self.disorient = disorient
        self.disorient_remain = disorient_remain
        self.crack = crack
        self.crack_remain = crack_remain
        self.impale = impale
        self.impale_remain = impale_remain
        self.disarm = disarm
        self.disarm_remain = disarm_remain
        self.weapon_1 = weapon_1
        self.weapon_2 = weapon_2
        self.last_damage = 0  # <-- Added attribute to track last damage taken

    def hp_lose(self, amt: int):
        self.hp_cur = max(self.hp_cur - amt, 0)  # Clamp hp_cur to not go below 0
        self.last_damage = amt  # <-- Store last damage here

    def hp_gain(self, amt: int):
        self.hp_cur += amt

    def ef_bleed(self):
        self.hp_cur -= 1

    def ef_disorient(self):
        print(f"player {self.name} is disadvantaged")

    def ef_crack(self, base_damage):
        if self.ac == "Light_Armour":
            dmg = int(base_damage * 0.1)
        elif self.ac == "Medium_Armour":
            dmg = int(base_damage * 0.25)
        else:  # Heavy_Armour
            dmg = int(base_damage * 0.5)
        return dmg

    def ef_impale(self):
        print(f"player {self.name} can't move")

    def ef_disarm(self):
        print(f"player {self.name} can't attack using {self.weapon_1.weapon}")

    # Effect Application Methods
    def apply_bleed(self, duration):
        self.bleed = True
        self.bleed_remain += duration

    def apply_disorient(self, duration):
        self.disorient = True
        self.disorient_remain += duration

    def apply_crack(self, duration):
        self.crack = True
        self.crack_remain += duration

    def apply_impale(self, duration):
        self.impale = True
        self.impale_remain += duration

    def apply_disarm(self, duration):
        self.disarm = True
        self.disarm_remain += duration

    def status_tick(self):
        if self.bleed and self.bleed_remain > 0:
            self.ef_bleed()
            self.bleed_remain -= 1
            if self.bleed_remain <= 0:
                self.bleed = False
        else:
            self.bleed = False

        if self.disorient and self.disorient_remain > 0:
            self.ef_disorient()
            self.disorient_remain -= 1
            if self.disorient_remain <= 0:
                self.disorient = False
        else:
            self.disorient = False

        if self.crack and self.crack_remain > 0:
            additional_damage = self.ef_crack(self.last_damage)  # <-- Use last_damage here
            self.hp_lose(additional_damage)  # Apply extra damage from crack effect
            self.crack_remain -= 1
            if self.crack_remain <= 0:
                self.crack = False
        else:
            self.crack = False

        if self.impale and self.impale_remain > 0:
            self.ef_impale()
            self.impale_remain -= 1
            if self.impale_remain <= 0:
                self.impale = False
        else:
            self.impale = False

        if self.disarm and self.disarm_remain > 0:
            self.ef_disarm()
            self.disarm_remain -= 1
            if self.disarm_remain <= 0:
                self.disarm = False
        else:
            self.disarm = False

class Weapon:
    def __init__(self, weapon, atk_dice, ability, ability_min: int, duration: int, hit: int):
        self.weapon = weapon
        self.atk_dice = atk_dice
        self.ability = ability
        self.ability_min = ability_min
        self.duration = duration
        self.hit = hit

def load_weapons_from_file(filename):
    with open(filename, "r") as f:
        weapons = json.load(f)
        return {name: dict_to_weapon(stats) for name, stats in weapons.items()}

def dict_to_weapon(d):
    return Weapon(d["weapon"], d["atk_dice"], d["ability"], d["ability_min"], d["duration"], d["hit"])

weapons = load_weapons_from_file("weapons.json")

def apply_armour_bonus(hp_tot, ac):
    if ac == "Light_Armour":
        return int(hp_tot * 1.1)
    elif ac == "Medium_Armour":
        return int(hp_tot * 1.25)
    elif ac == "Heavy_Armour":
        return int(hp_tot * 1.5)
    else:
        return hp_tot  # no bonus if ac not recognized

def dict_to_character(d):
    weapon_1 = dict_to_weapon(d["weapon_1"])
    weapon_2 = dict_to_weapon(d["weapon_2"])

    # Apply armour bonus once here to hp_tot
    adjusted_hp_tot = apply_armour_bonus(d["hp_tot"], d["ac"])

    # Make sure current hp is at max on creation/load
    hp_cur = adjusted_hp_tot

    return Character(
        name=d["name"],
        race=d["race"],
        type=d["type"],
        ac=d["ac"],
        hp_tot=adjusted_hp_tot,
        hp_cur=hp_cur,
        bleed=d["bleed"],
        bleed_remain=d["bleed_remain"],
        disorient=d["disorient"],
        disorient_remain=d["disorient_remain"],
        crack=d["crack"],
        crack_remain=d["crack_remain"],
        impale=d["impale"],
        impale_remain=d["impale_remain"],
        disarm=d["disarm"],
        disarm_remain=d["disarm_remain"],
        weapon_1=weapon_1,
        weapon_2=weapon_2
    )

def load_characters(filename):
    with open(filename, "r") as f:
        data = json.load(f)  # data is a list of character dicts
    return [dict_to_character(d) for d in data]

characters = load_characters("characters.json")

def find_character_by_name(the_name):
    for char in characters:
        if char.name == the_name:
            return char

def get_valid_input(prompt, valid_values=None, input_type=str):
    while True:
        try:
            user_input = input(prompt).strip()
            # Convert to desired type
            value = input_type(user_input)
            # If valid_values is set, check membership (for strings or ints)
            if valid_values and value not in valid_values:
                print(f"Invalid input. Please enter one of: {valid_values}")
                continue
            return value
        except ValueError:
            print(f"Invalid input type. Please enter a valid {input_type.__name__}.")

RUN = True
while RUN:
    for char in characters:
        char.status_tick()

    for char in characters:
        print(f'''{char.name}
hp :      {char.hp_cur}/{char.hp_tot}
bleed:    {char.bleed} -> {char.bleed_remain}
crack:    {char.crack} -> {char.crack_remain}
impale:   {char.impale} -> {char.impale_remain}
disarm:   {char.disarm} -> {char.disarm_remain}
disorient:{char.disorient} -> {char.disorient_remain}
''')

    # Validate attacker
    attacker_name = get_valid_input("Who is attacking?\n> ", valid_values=[c.name for c in characters], input_type=str)
    attacker = find_character_by_name(attacker_name)

    # Select weapon 1 or 2
    weapon_choice = get_valid_input(
        f"Select weapon (1 or 2) for {attacker.name}:\n> ",
        valid_values=[1, 2],
        input_type=int
    )
    current_weapon = attacker.weapon_1 if weapon_choice == 1 else attacker.weapon_2

    # Validate defender
    defender_name = get_valid_input("Who is defending?\n> ", valid_values=[c.name for c in characters], input_type=str)
    defender = find_character_by_name(defender_name)

    # Validate d20 roll (1-20)
    roll = get_valid_input("d20 roll?\n> ", input_type=int)
    if not 1 <= roll <= 20:
        print("Roll must be between 1 and 20. Try again.")
        continue

    # Validate damage dealt (non-negative integer)
    dmg = get_valid_input("Damage dealt?\n> ", input_type=int)
    if dmg < 0:
        print("Damage must be zero or positive. Try again.")
        continue

    # Validate effect roll (0-100)
    effect = get_valid_input("Effect roll?\n> ", input_type=int)
    if not 0 <= effect <= 100:
        print("Effect roll must be between 0 and 100. Try again.")
        continue

    if roll >= current_weapon.hit:
        # checks if roll is bigger than the minimum roll required
        if effect > current_weapon.ability_min:
            #checks to see if effect roll is greater than the minimum requirement, since ability chanc
            if current_weapon.ability == "bleed":
                defender.apply_bleed(current_weapon.duration)
            elif current_weapon.ability == "crack":
                defender.apply_crack(current_weapon.duration)
            elif current_weapon.ability == "disorient":
                defender.apply_disorient(current_weapon.duration)
            elif current_weapon.ability == "disarm":
                defender.apply_disarm(current_weapon.duration)
            elif current_weapon.ability == "impale":
                defender.apply_impale(current_weapon.duration)

        defender.hp_lose(dmg)
    else:
        print("Miss!")
