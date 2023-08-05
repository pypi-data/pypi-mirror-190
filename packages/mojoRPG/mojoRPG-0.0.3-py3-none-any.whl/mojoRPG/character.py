from .mojocore import Die, Mojo

m = Mojo()

class Character(object):
  def __init__(
    self,
    name,
    strength = 5,
    dexterity = 5,
    constitution = 5,
    inteligence = 5,
    wisdom = 5,
    charisma = 5,
    offense_skill = 0,
    defense_skill = 0,
    armor = 0,
    ddsides = 8,
    ddcount = 1,
    hit_points = 100,
    mojo = 3,
    oMojo = 3,
    dMojo = 1,
  ):
    self._name = name
    self._attribute = {
      "strength": strength,
      "dexterity": dexterity,
      "constitution": constitution,
      "inteligence": inteligence,
      "wisdom": wisdom,
      "charisma": charisma,
    }
    self._skill = {
      "offense": offense_skill,
      "defense": defense_skill,
    }
    self._armor = armor
    self._weapon = {
      "sides": ddsides,
      "count": ddcount,
    }
    self._hit_points = {
      "max": hit_points,
      "current": hit_points,
      "temp": 0,
    }
    self._mojo = {
      "max": mojo,
      "current": mojo,
      "temp": 0,
    }
    self._initiative = 0
    self.actions = []
    self.default_offense_mojo = oMojo
    self.default_defense_mojo = dMojo

  @property
  def name(self):
    return self._name

  @property
  def hpMax(self):
    return self._hit_points["max"]
  @property
  def hpCurrent(self):
    return self._hit_points["current"]
  @property
  def hpTemp(self):
    return self._hit_points["temp"]
  @property
  def hp(self):
    return self.hpCurrent + self.hpTemp

  @property
  def mojoMax(self):
    return self._mojo["max"]
  @property
  def mojoCurrent(self):
    return self._mojo["current"]
  @property
  def mojoTemp(self):
    return self._mojo["temp"]
  @property
  def mojo(self):
    return self.mojoCurrent + self.mojoTemp
  @property
  def mojoAvailable(self):
    return self.mojo + self.mojoMax

  @property
  def armor(self):
    return self._armor

  @property
  def initiative(self):
    return self._initiative

  @hpMax.setter
  def hpMax(self, value):
    self._hit_points["max"] = value
  @hpCurrent.setter
  def hpCurrent(self, value):
    self._hit_points["current"] = value
  @hpTemp.setter
  def hpTemp(self, value):
    self._hit_points["temp"] = value

  @mojoMax.setter
  def mojoMax(self, value):
    self._mojo["max"] = value
  @mojoCurrent.setter
  def mojoCurrent(self, value):
    self._mojo["current"] = value
  @mojoTemp.setter
  def mojoTemp(self, value):
    self._mojo["temp"] = value

  def damage(self, attack_damage):
    temp_hp_used = min(self._hit_points["temp"], attack_damage)
    self._hit_points["temp"] -= temp_hp_used
    current_hp_used = min(self._hit_points["current"], attack_damage-temp_hp_used)
    self._hit_points["current"] -= current_hp_used
    if attack_damage <= 0:
      print(f"{self.name} received no damage")
    elif self.hp > 0:
      print(f"{self.name} received {attack_damage} damage leaving {self.hp}hp.")
    else:
      print(f"{self.name} is dead.")

  def heal(self, hit_points):
    new_hp = min(hpMax(), self.hpCurrent + hit_point)
    self._hit_points["current"] = new_hp
    print(f"{self.name} healed {hit_point}. Hp:{self.hp()} (Temp:{self.hpTemp} Max:{self.hpMax()}).")

  def useMojo(self, mojo):
    temp_mojo_used = min(self.mojoTemp, mojo)
    self._mojo["temp"] -= temp_mojo_used
    mojo_used = min(self.mojoAvailable, mojo - temp_mojo_used)
    self._mojo["current"] -= mojo_used
    print(f"{self.name} used {mojo_used} mojo (and {temp_mojo_used} temp mojo) and now has {self.mojo} left. "+
          f"{self.mojoAvailable} max to use this round.")
    return temp_mojo_used + mojo_used

  def replenishMojo(self):
    new_mojo = min(self.mojo + self.mojoMax, self.mojoTemp + self.mojoMax)
    print(f"{self.name} replenished mojo from {self.mojo} to {new_mojo}")
    self._mojo["current"] = new_mojo

  def getAttribute(self, attribute):
    return self._attribute[attribute]
  def setAttribute(self, attribute, value):
    self._attribute[attribute] = value

  def getSkill(self, skill):
    return self._skill[skill]
  def setSkill(self, skill, value):
    self._skill[skill] = value

  def rollInitiative(self):
    self._initiative = Die(sides = 10, count = 1).roll() + self.getAttribute("dexterity")
    print(f"{self.name} rolled a {self._initiative - self.getAttribute('dexterity')} for initiative " +
          f"({self._initiative - self.getAttribute('dexterity')}+{self.getAttribute('dexterity')} = {self._initiative})")
    return self._initiative

  def toHit(self, mojo):
    return 10 + mojo + self.getSkill("defense")

  def attack(self, defender, oMojo, dMojo):
    oMojoUsed = self.useMojo(oMojo)
    dMojoUsed = defender.useMojo(dMojo)
    action = {"type": "attack"}
    roll = m.rollSkill(oMojoUsed)
    action["attack"] = {
      "roll": roll,
      "average": sum(roll) / len(roll),
      "min": min(roll),
      "max": max(roll),
      "value": m.getAttackValue(roll),
      "overHit": 0,
      "overDamage": 0,
    }
    action["attack"]["overHit"], action["attack"]["overDamage"] = m.getHitDamage(
      attack=m.getAttackValue(roll), target=defender.toHit(dMojoUsed), armor=defender.armor
    )
    droll = m.rollDamageDice(self._weapon["sides"], self._weapon["count"])
    action["damage"] = {
      "roll": droll,
      "average": sum(droll) / len(droll),
      "min": min(droll),
      "max": max(droll),
      "value": m.calculateDamage(droll, 0),
    }
    if action["attack"]["overDamage"] > 0:
      action["total_damage"] = action["damage"]["value"] + action["attack"]["overDamage"]
    else:
      action["total_damage"] = 0
    print(f'Attack: roll: {action["attack"]["roll"]}({action["attack"]["value"]}) ' +
          f'ToHit: {defender.toHit(dMojoUsed)} OverHit:{action["attack"]["overHit"]} ' +
          f'OverDamage: {action["attack"]["overDamage"]} DamageRoll:{action["damage"]["roll"]}({action["damage"]["value"]}) ' +
          f'Damage:{action["total_damage"]}')
    defender.damage(action["total_damage"])
    self.actions.append(action)
    return action

  def endRound(self):
    self.replenishMojo()

  def print(self):
    print("===============================================")
    print(f"Name: {self.name:15}    HP:{self.hp:<3}        Mojo:{self.mojo:<2}")
    print(f"STR: {self.getAttribute('strength'):<2}", end = " ")
    print(f"DEX: {self.getAttribute('dexterity'):<2}", end = " ")
    print(f"CON: {self.getAttribute('constitution'):<2}", end = " ")
    print(f"INT: {self.getAttribute('inteligence'):<2}", end = " ")
    print(f"WIS: {self.getAttribute('wisdom'):<2}", end = " ")
    print(f"CHA: {self.getAttribute('charisma'):<2}")
    print(f"Offensive Skill:{self.getSkill('offense'):<2} Defensive Skill: {self.getSkill('defense'):<2}")
    print("===============================================")
