import bisect

import numpy as np

DVALUES = {}
for n in range(2, 100):
    DVALUES[n] = np.array(range(1, n + 1))


def average(lst):
    return sum(lst) / len(lst)
def sortInitiative(e):
    return e.initiative

class Die(object):
    def __init__(self, sides=10, count=1):
        self.sides = sides
        self.count = count
        self.roll()

    def roll(self):
        self.value = 0
        for i in range(self.count):
            self.value += np.random.choice(DVALUES[self.sides])
        return self.value

    def getValue(self):
        return self.value


class Mojo(object):
    def __init__(
        self,
        attack_die_sides=10,
        attack_die_count=2,
        explode=10,
    ):
        self.option = {}
        self.option["attack_die_sides"] = attack_die_sides
        self.option["attack_die_count"] = attack_die_count
        if explode == 1:
            exit(-1)
        self.option["explode"] = explode

    # Roll a single die and explode
    def rollSkillDie(self):
        die = Die(sides=self.option["attack_die_sides"])
        roll_total = die.getValue()
        while self.option["explode"] == die.getValue():
            roll_total += die.roll()
        return roll_total

    # Roll some dice
    # count - the number of dice to roll
    # sides - The type of die you want to roll (2-100)
    # explode - boolean to indicate if dice are exploded
    # RETURN: array of dice values order high to low
    def rollSkillDice(self, count=1):
        dice = []
        for n in range(count):
            roll = self.rollSkillDie()
            bisect.insort(dice, roll)
        dice.reverse()
        return dice

    # Roll a mojo roll
    def rollSkill(self, mojo=1, proficiency=100):
        return self.rollSkillDice(count=min(mojo, proficiency))

    # Roll a single die for damage
    def rollDamageDie(self, sides, explode=0):
        return Die(sides).getValue()

    # Roll some dice
    # count - the number of dice to roll
    # sides - The type of die you want to roll (2-100)
    # explode - boolean to indicate if dice are exploded
    # RETURN: array of dice values order high to low
    def rollDamageDice(self, sides, count=1):
        dice = []
        for n in range(count):
            dice.append(self.rollDamageDie(sides))
        return dice

    def calculateDamage(self, dice, damage_bonus):
        return sum(dice) + damage_bonus

    # Takes an array of rolls and sums the largest dice
    def getAttackValue(self, dice):
        return sum(dice[0 : self.option["attack_die_count"]])

    # return attack value above hit and damage
    def getHitDamage(self, attack, target, armor):
        return (max(0, attack - (target - 1)), max(0, attack - (target + armor - 1)))

    def fight(self, players, auto=False):
        for player in players:
            player.print()

        for player in players:
            player.rollInitiative()

        round_num = 0
        winner = False
        while not winner:
            queue = []

            # move this to mojo core

            players = sorted(players, key=lambda x: x.initiative)

            round_num += 1
            print(f"")
            print(f"============ Round: {round_num} ============ ")
            for player in players:
                print(
                    f"  Initiative: {player.initiative}      {player.name} (hp:{player.hp} mojo:{player.mojo}) "
                )

            for i in range(len(players)):
                o = players[i]
                d = players[(i + 1) % len(players)]
                if o.mojo <= 0:
                    print(f"TURN SKIP: {o.name} has no mojo left for this round, skipping turn")
                else:
                    while o.mojo > 0:
                        print(
                            f"TURN: {o.name}! Enter offensive mojo to use (current:{o.mojo} max:{o.mojoMax}) [0 to skip turn]:",
                            end=" ",
                        )
                        if auto:
                            print("")
                            oMojoToUse = o.default_offense_mojo
                        else:
                            oMojoToUse = int(input() or o.default_offense_mojo)
                        if oMojoToUse == 0:
                            break
                        oMojoToUse = o.useMojo(oMojoToUse)
                        print(
                            f"  {d.name} is defending. Enter deffensive mojo to use (current:{d.mojo} max:{d.mojoMax}):",
                            end=" ",
                        )
                        if auto:
                            print("")
                            dMojoToUse = d.default_defense_mojo
                        else:
                            dMojoToUse = int(input() or d.default_defense_mojo)
                        dMojoToUse = d.useMojo(dMojoToUse)
                        print(
                            f"  {o.name} will roll {oMojoToUse} dice and add the best {min(2, oMojoToUse)} "
                        )
                        print(
                            f"  {d.name}'s Defense - ToHit:{d.toHit(dMojoToUse)} ToDamage:{d.toHit(dMojoToUse)+d.armor}  "
                        )
                        if not auto:
                            print("  press enter to roll", end="")
                            input()
                        action = o.attack(d, oMojoToUse, dMojoToUse)

                    if d.hp <= 0:
                        winner = True
                        break
            for player in players:
                player.endRound()
