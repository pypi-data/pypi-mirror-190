import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import bisect
import click
import mojocore
import pandas as pd

plt.style.use('ggplot')

DVALUES = {}
for n in range(2,100):
  DVALUES[n] = np.array(range(1, n+1))

def average(lst):
  return sum(lst) / len(lst)

# Roll a single die and add an optional modifier
# die - The type of die you want to roll (2-100)
def rollSingleDie(die, modifier=0, explode=False):
  roll = np.random.choice(DVALUES[die])
  roll_sum = roll
  while explode == True and roll == die:
    roll = np.random.choice(DVALUES[die])
    roll_sum += roll
  return roll_sum + modifier

# Roll a single die and add an optional modifier
# die - The type of die you want to roll (2-100)
def rollDice(die, count=1, modifier=0, explode=False):
  rolls = []
  for n in range(count):
    roll = rollSingleDie(die=die, modifier=modifier, explode=explode)
    bisect.insort(rolls, roll)
  rolls.reverse()
  return rolls

# Roll a mojo roll
def mojoRoll(modifier=0, mojo=1, proficiency=10, die=10, explode=False):
  dice_to_roll = min(mojo, proficiency)
  return rollDice(count=dice_to_roll, die=die, modifier=modifier, explode=explode)

# Takes an array of rolls and a hit target and damage target
# sums the rolls and compares that sum to target and damage
# Returns the difference between the sum and hits and hit-armor
def sumMojoHits(rolls, target, armor):
  rolls_sum = sum(rolls)
  if rolls_sum >= target and rolls_sum < target + armor:
    return (rolls_sum - target, 0)
  elif rolls_sum >= target + armor:
    return (0, rolls_sum - (target + armor))
  return (0, 0)

# Takes an array of rolls and a hit target and damage target
# sums the rolls and compares that sum to target and damage
# Returns the number of hits and number of damage hits
def countMojoHits(rolls, target, armor):
  hits = 0
  damages = 0
  for i  in rolls:
    if i >= target and i < target + armor:
      hits += 1
    elif i >=  target + armor:
      damages += 1
  return (hits, damages)

def calculateDamage(rolls, modifier=0):
  return max(0, sum(rolls) + modifier)

@click.group()
def cli():
  pass

@cli.group()
def characterize():
  pass

@cli.group()
def roll():
  pass

@characterize.command()
@click.option("-m", "--mojo", default=1, type=int, help="Number of mojo points to use.")
@click.option("-b", "--base", default=0, type=int, help="Attribute Base value.")
@click.option("-p", "--proficiency", default=1, type=int, help="Proficiency.")
@click.option("-o", "--bonus", default=0, type=int, help="Additional Bonus.")
@click.option("-t", "--target", default=15, type=int, help="Target AC (after defensive bonus).")
def combat(
  mojo,
  base,
  proficiency,
  bonus,
  target,
):
  print(f"Combat Base:{base} Mojo:{mojo} Proficiency:{proficiency} bonus:{bonus}")
  samples = 100

  ax = []
  fig, ax = plt.subplots(nrows=10, sharey=True, figsize=(13,4))

  for m in range(10):
    rolls = []
    vmax = 0
    crit = 0
    rsum = 0
    for n in range(samples):
      hits = 0
      mroll = mojoRoll(modifier=base, mojo=m+1, proficiency=proficiency)
      # print(mroll)
      mavg = average(mroll)
      for m in range(m+1):
        if mroll[m] > 12:
            hits += 1
      rolls.append(hits)
      hit_count += hits
      if vmax < mavg:
        vmax = mavg

    print(f"Average number of hits: {round(hit_count/samples, 2)}")
    print(f"Max roll: {vmax}")

    sns.histplot(rolls, ax=ax[m], bins=10, binrange=[0, 10]).set(title=f'Mojo: {m+1}')
  plt.show()

@characterize.command()
@click.option("-l", "--mojo_low", default=1, type=int, help="Number of mojo points to use.")
@click.option("-h", "--mojo_high", default=1, type=int, help="Number of mojo points to use.")
@click.option("-s", "--skill", default=0, type=int, help="Attribute Base value.")
@click.option("-p", "--proficiency", default=1, type=int, help="Proficiency.")
@click.option("-o", "--bonus", default=0, type=int, help="Additional Bonus.")
@click.option("-t", "--target", default=15, type=int, help="Target AC (after defensive bonus).")
@click.option("-a", "--armor", default=15, type=int, help="Target AC (after defensive bonus).")
@click.option("-d", "--damage_die", default=8, type=int, help="Damage to roll.")
@click.option("-e", "--extra", default=0, type=int, help="Extra Damage addition.")
def damage(
  mojo_low,
  mojo_high,
  skill,
  proficiency,
  bonus,
  target,
  armor,
  damage_die,
  extra,
):
  samples = 10000
  toHit = max(0, target)

  ax = []
  fig, ax = plt.subplots(nrows=(mojo_high+1-mojo_low), sharey=True, figsize=(13,4))

  for mojo in range(mojo_low, mojo_high+1):
    rolls = []
    vmax = 0
    crit = 0
    rsum = 0
    hit_count = 0
    damage_count = 0
    damage_sum = 0
    miss_count = 0
    for n in range(samples):
      mrolls = mojoRoll(mojo=(skill+mojo), proficiency=proficiency)
      mavg = average(mrolls)

      hits, damages = countMojoHits(rolls=mrolls, target=toHit, armor=armor)
      if hits > 0 and damages == 0: hit_count += 1
      elif damages > 0: damage_count += 1
      else: miss_count += 1

      damage_rolls = rollDice(count=damages, die=damage_die, modifier=extra)

      damage = calculateDamage(rolls=damage_rolls)
      damage_sum += damage
      rolls.append(damage)

      print(f"Roll: {mrolls} ToHit: {toHit}({hits}) DamageHit: {toHit++armor}({damages}) Damage:{damage_rolls} ({damage})")
      vmax = max(damage, vmax)

    print(f"Attacker(Skill: {skill} Mojo: {mojo} Damage: '1d{damage_die}') Defender(Target: {target} Armor: {armor}) 'Adjusted To Hit': {toHit} 'Adjusted To Damage': {toHit+armor}")
    print(f"Percentage of damaging strikes: {round(damage_count/samples*100, 2)}%")
    print(f"Percentage of hits (no damage): {round(hit_count/samples*100, 2)}%")
    print(f"Percentage of misses:           {round(miss_count/samples*100, 2)}%")
    print(f"Average damage inflicted:       {round(damage_sum/damage_count, 2)}")
    print(f"Max Damage roll:                {vmax}")

    if mojo_high == mojo_low:
      sns.histplot(rolls, ax=ax, bins=vmax+1, binrange=[0, vmax+1]).set(title=f'Mojo: {mojo}')
    else:
      sns.histplot(rolls, ax=ax[mojo-mojo_low], bins=vmax+1, binrange=[0, vmax+1]).set(title=f'Mojo: {mojo}')
  plt.show()


@characterize.command()
@click.option("-l", "--mojo_low", default=1, type=int, help="Number of mojo points to use.")
@click.option("-h", "--mojo_high", default=1, type=int, help="Number of mojo points to use.")
@click.option("-s", "--skill", default=0, type=int, help="Attribute Base value.")
@click.option("-p", "--proficiency", default=1, type=int, help="Proficiency caps mojo.")
@click.option("-o", "--bonus", default=0, type=int, help="Additional Bonus.")
@click.option("-t", "--target", default=15, type=int, help="Target AC (after defensive bonus).")
@click.option("-a", "--armor", default=5, type=int, help="Target AC (after defensive bonus).")
@click.option("-d", "--ddsides", default=8, type=int, help="Damage die to roll.")
@click.option("-b", "--dbonus", default=0, type=int, help="Extra Damage addition.")
def damage1(
  mojo_low,
  mojo_high,
  skill,
  proficiency,
  bonus,
  target,
  armor,
  ddsides,
  dbonus,
):
  samples = 10000
  toHit = max(0, target-skill)
  ddcount = 1
  m = mojocore.Mojo(explode=10)

  ax = []
  # fig, ax = plt.subplots(nrows=(mojo_high+1-mojo_low), sharey=True, figsize=(13,4))
  # fig, ay = plt.subplots(nrows=1, sharey=True, stacked=True, figsize=(13,4))
  a = [[],[]]
  stats = {
    'damage': [],
    'hit': [],
    'miss': []
  }
  index = []

  for mojo in range(mojo_low, mojo_high+1):
    actions = []
    for n in range(samples):
      action = m.actionMelleAttack(mojo, toHit, armor, ddcount, ddsides, dbonus, proficiency)
      actions.append(action)

    rolls = []
    vmax = 0
    hit_count = 0
    damage_count = 0
    damage_sum = 0
    miss_count = 0
    damage_overage_sum = 0
    for action in actions:
      rolls.append(action["attack"]["roll"])
      if action["attack"]["overDamage"] > 0:
        damage_count += 1
      elif action["attack"]["overHit"] > 0:
        hit_count += 1
      else:
        miss_count += 1
      damage_overage_sum += action["attack"]["overDamage"]
      damage_sum += action["damage"]["value"] + action["attack"]["overDamage"]
      vmax = max(action["damage"]["value"] + action["attack"]["overDamage"], vmax)

    print(f"Attacker(Skill: {skill} Mojo: {mojo} Damage: '1d{ddsides}') Defender(Target: {target} Armor: {armor}) 'Adjusted To Hit': {toHit} 'Adjusted To Damage': {toHit+armor}")
    damage_percent = round(damage_count/samples*100, 2)
    print(f"Percentage of damaging strikes: {damage_percent}%")
    hit_percent = round(hit_count/samples*100, 2)
    print(f"Percentage of hits (no damage): {hit_percent}%")
    miss_percent = round(miss_count/samples*100, 2)
    print(f"Percentage of misses:           {miss_percent}%")
    print(f"Average of damge Overage:       {round(damage_overage_sum/damage_count, 2)}")
    if damage_count > 0:
      print(f"Average damage inflicted:       {round(damage_sum/damage_count, 2)}")
    print(f"Max Damage roll:                {vmax}")
    stats["hit"].append(hit_percent)
    stats["damage"].append(damage_percent)
    stats["miss"].append(miss_percent)
    index.append(mojo)

  df = pd.DataFrame(stats, index)

  # create stacked bar chart for monthly temperatures
  df.plot(kind='bar', stacked=True, title=f"OffSkill:{skill} Target:{target} Armor:{armor}", color=['red', 'skyblue', 'green'])
  plt.xlabel('Mojo')
  plt.ylabel('Percent')
    # sns.lineplot(a, ax=ay).set(title=f'Mojo: {mojo}')
  plt.show()
      # if mojo_high == mojo_low:
      #   sns.histplot(rolls, ax=ax, bins=vmax+1, binrange=[0, vmax+1]).set(title=f'Mojo: {mojo}')
      # else:
      #   sns.histplot(rolls, ax=ax[mojo-mojo_low], bins=vmax+1, binrange=[0, vmax+1]).set(title=f'Mojo: {mojo}')
    # plt.show()

@characterize.command()
@click.option("-l", "--mojo_low", default=1, type=int, help="Number of mojo points to use.")
@click.option("-h", "--mojo_high", default=1, type=int, help="Number of mojo points to use.")
@click.option("-s", "--skill", default=0, type=int, help="Attribute Base value.")
@click.option("-p", "--proficiency", default=1, type=int, help="Proficiency caps mojo.")
@click.option("-o", "--bonus", default=0, type=int, help="Additional Bonus.")
@click.option("-t", "--target", default=15, type=int, help="Target AC (after defensive bonus).")
@click.option("-a", "--armor", default=5, type=int, help="Target AC (after defensive bonus).")
@click.option("-d", "--damage_die", default=8, type=int, help="Damage to roll.")
@click.option("-e", "--extra_damage", default=0, type=int, help="Extra Damage addition.")
def combat1(
  mojo_low,
  mojo_high,
  skill,
  proficiency,
  bonus,
  target,
  armor,
  damage_die,
  extra_damage,
):
  samples = 10000
  toHit = max(0, target)

  ax = []
  fig, ax = plt.subplots(nrows=(mojo_high+1-mojo_low), sharey=True, figsize=(13,4))

  vmax = 70
  for mojo in range(mojo_low, mojo_high+1):
    rolls = []
    crit = 0
    rsum = 0
    hit_count = 0
    damage_count = 0
    damage_sum = 0
    miss_count = 0
    for n in range(samples):
      mrolls = mojoRoll(mojo=mojo, proficiency=proficiency, explode=False)
      mavg = average(mrolls)

      result = sum(mrolls[0:2])
      rolls.append(result)

      vmax = max(result, vmax)

    # print(f"Attacker(Skill: {skill} Mojo: {mojo} Damage: '1d{damage_die}') Defender(Target: {target} Armor: {armor}) 'Adjusted To Hit': {toHit} 'Adjusted To Damage': {toHit+armor}")
    # print(f"Percentage of damaging strikes: {round(damage_count/samples*100, 2)}%")
    # print(f"Percentage of hits (no damage): {round(hit_count/samples*100, 2)}%")
    # print(f"Percentage of misses:           {round(miss_count/samples*100, 2)}%")
    # print(f"Average damage inflicted:       {round(damage_sum/damage_count, 2)}")
    # print(f"Max Damage roll:                {vmax}")

    if mojo_high == mojo_low:
      sns.histplot(rolls, ax=ax, bins=vmax+1, binrange=[0, vmax+1]).set(title=f'Mojo: {mojo}')
    else:
      sns.histplot(rolls, ax=ax[mojo-mojo_low], bins=vmax+1, binrange=[0, vmax+1]).set(title=f'Mojo: {mojo}')
  plt.show()



@roll.command()
@click.option("-m", "--mojo", default=3, type=int, help="Number of mojo points to use.")
@click.option("-b", "--base", default=3, type=int, help="Attribute Base value.")
@click.option("-p", "--proficiency", default=0, type=int, help="Proficiency.")
@click.option("-o", "--bonus", default=10, type=int, help="What die to roll.")
def combat(
  mojo,
  base,
  proficiency,
  bonus,
):
  print(mojoRoll1(modifier=base, mojo=mojo, proficiency=proficiency, bonus=bonus))


@characterize.command()
@click.option("-m", "--mojo", default=3, type=int, help="Number of mojo points to use.")
@click.option("-b", "--base", default=3, type=int, help="Attribute Base value.")
@click.option("-p", "--proficiency", default=0, type=int, help="Proficiency.")
@click.option("-o", "--bonus", default=10, type=int, help="What die to roll.")
def attribute(
  mojo,
  base,
  proficiency,
  count,
  die,
):
  if die == None:
    die = base
  print(f"Attribute Base:{base} Mojo:{mojo} Proficiency:{proficiency} bonus:{bonus}")

  vmax = 0
  rsum = 0
  samples = 10000
  rolls = []
  for n in range(samples):
    rolls.append(mojoRoll1(base=base, proficiency=proficiency, mojo=mojo, bonus=bonus))
    if vmax < rolls[n]:
      vmax = rolls[n]
    rsum+=rolls[n]

  print(f"Avg: {rsum/samples}")
  print(f"Max: {vmax}")

  fig, (ax1) = plt.subplots(ncols=1, sharey=True, figsize=(13,4))
  sns.histplot(rolls, ax=ax1, binrange=[0, max(rolls)])
  plt.show()

@roll.command()
@click.option("-m", "--mojo", default=3, type=int, help="Number of mojo points to use.")
@click.option("-b", "--base", default=3, type=int, help="Attribute Base value.")
@click.option("-p", "--proficiency", default=0, type=int, help="Proficiency.")
@click.option("-o", "--bonus", default=10, type=int, help="Bonus to add to roll.")
def attribute(
  mojo,
  base,
  proficiency,
  bonus,
):
  print(mojoRoll(modifier=base, proficiency=proficiency, mojo=mojo, bonus=bonus))

@cli.command()
@click.option("--mojo1", default=3, type=int, help="Number of mojo points to use.")
@click.option("--base1", default=0, type=int, help="Attribute Base value.")
@click.option("--proficiency1", default=10, type=int, help="Proficiency.")
@click.option("--bonus1", default=0, type=int, help="What die to roll.")
@click.option("--target1", default=15, type=int, help="Target AC (after defensive bonus).")
@click.option("--armor1", default=0, type=int, help="Target AC (after defensive bonus).")
@click.option("--damage1", default="1d6", type=str, help="Damage to roll.")
@click.option("--extra1", default=0, type=int, help="Extra Damage addition.")
@click.option("--hp1", default=0, type=int, help="Extra Damage addition.")
@click.option("--mojo2", default=3, type=int, help="Number of mojo points to use.")
@click.option("--base2", default=0, type=int, help="Attribute Base value.")
@click.option("--proficiency2", default=10, type=int, help="Proficiency.")
@click.option("--bonus2", default=0, type=int, help="What die to roll.")
@click.option("--target2", default=15, type=int, help="Target AC (after defensive bonus).")
@click.option("--armor2", default=0, type=int, help="Target AC (after defensive bonus).")
@click.option("--damage2", default="1d6", type=str, help="Damage to roll.")
@click.option("--extra2", default=0, type=int, help="Extra Damage addition.")
@click.option("--hp2", default=0, type=int, help="Extra Damage addition.")
def fight(
  mojo1,
  base1,
  proficiency1,
  bonus1,
  target1,
  armor1,
  damage1,
  extra1,
  hp1,
  mojo2,
  base2,
  proficiency2,
  bonus2,
  target2,
  armor2,
  damage2,
  extra2,
  hp2,
):
  damage_sum = 0
  hit = 0
  rounds = 10000
  print(f"Executing a fight!")
  print(f"Player 1: Starts with {hp1} HP")
  print(f"Offense: Base:{base1} Proficiency:{proficiency1}. Mojo:{mojo1} (per attack). Damage:{damage1}+{extra1}")
  print(f"Defense: Target: {target1}. Armor: {armor1}")
  print(f"Player 2: Starts with {hp2} HP")
  print(f"Offense: Base:{base2} Proficiency:{proficiency2}. Mojo:{mojo2} (per attack). Damage:{damage2}+{extra2}")
  print(f"Defense: Target: {target2}. Armor: {armor2}")
  rolls = []
  for n in range(rounds):
    mroll = mojoRoll1(modifier=base1, mojo=mojo1, proficiency=proficiency1, bonus=bonus1)
    damage = damage_roll(target=target2, mroll=mroll, dstring=damage1, extra=extra1)
    if damage <= 0:
      print(f"Player1 rolled a {mroll} miss!!")
    elif damage <= armor2:
      print(f"Player1 rolled a {mroll} hitting Player2's armor!. damage of {damage} is not more than armor: {armor2}")
    else:
      hp2 -= (damage - armor2)
      print(f"Player1 rolled a {mroll} hitting Player2 for {damage}. Player2's armor blocked {min(armor2, damage)} dealing {damage-armor2} hp. Player 2 now has {hp2} HP left.")
    if hp2 <= 0:
      break
    mroll = mojoRoll1(modifier=base2, mojo=mojo2, proficiency=proficiency2, bonus=bonus2)
    damage = damage_roll(target=target1, mroll=mroll, dstring=damage2, extra=extra2)
    if damage <= 0:
      print(f"Player2 rolled a {mroll} miss!!")
    elif damage <= armor1:
      print(f"Player2 rolled a {mroll} hitting Player1's armor!. damage of {damage} is not more than armor: {armor1}")
    else:
      hp1 -= (damage - armor1)
      print(f"Player2 rolled a {mroll} hitting Player1 for {damage}. Player1's armor blocked {min(armor1, damage)} dealing {damage-armor1} hp. Player 1 now has {hp1} HP left.")
    if hp1 <= 0:
      break


if __name__ == "__main__":
    cli()
