import numpy as np
import bisect

DVALUES = {}
for n in range(2,100):
  DVALUES[n] = np.array(range(1, n+1))

def average(lst):
  return sum(lst) / len(lst)

class Die(object):
  def __init__(self, sides = 10, count = 1):
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
    attack_die_sides = 10,
    attack_die_count = 2,
    explode = 10,
  ):
    self.option = {}
    self.option["attack_die_sides"] = attack_die_sides
    self.option["attack_die_count"] = attack_die_count
    if explode == 1:
      exit(-1)
    self.option["explode"] = explode

  # Roll a single die and explode
  def rollSkillDie(self):
    die = Die(sides = self.option["attack_die_sides"])
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
  def rollSkill(self, mojo = 1, proficiency = 100):
    return self.rollSkillDice(count=min(mojo, proficiency))

  # Roll a single die for damage
  def rollDamageDie(self, sides, explode = 0):
    return Die(sides).getValue()

  # Roll some dice
  # count - the number of dice to roll
  # sides - The type of die you want to roll (2-100)
  # explode - boolean to indicate if dice are exploded
  # RETURN: array of dice values order high to low
  def rollDamageDice(self, sides, count = 1):
    dice = []
    for n in range(count):
      dice.append(self.rollDamageDie(sides))
    return dice

  def calculateDamage(self, dice, damage_bonus):
    return sum(dice) + damage_bonus

  # Takes an array of rolls and sums the largest dice
  def getAttackValue(self, dice):
    return sum(dice[0:self.option["attack_die_count"]])

  # return attack value above hit and damage
  def getHitDamage(self, attack, target, armor):
    return (max(0, attack - (target - 1)), max(0, attack - (target + armor - 1)))

  def actionMelleAttack(self, mojo, toHit, armor, ddcount, ddsides, dbonus, proficiency=100):
    action = {"type": "attack"}
    roll = self.rollSkill(mojo, proficiency)
    action["attack"] = {
      "roll": roll,
      "average": average(roll),
      "min": min(roll),
      "max": max(roll),
      "value": self.getAttackValue(roll),
      "overHit": 0,
      "overDamage": 0,
    }
    action["attack"]["overHit"], action["attack"]["overDamage"] = self.getHitDamage(
      attack=self.getAttackValue(roll), target=toHit, armor=armor
    )
    droll = self.rollDamageDice(ddsides, ddcount)
    action["damage"] = {
      "roll": droll,
      "average": average(droll),
      "min": min(droll),
      "max": max(droll),
      "value": self.calculateDamage(droll, dbonus),
    }

    print(f'Attack: roll: {action["attack"]["roll"]}({action["attack"]["value"]}) ToHit: {action["attack"]["overHit"]} DamageHit: {action["attack"]["overDamage"]} Damage:{action["damage"]["roll"]} ({action["damage"]["value"]})')
    return action
