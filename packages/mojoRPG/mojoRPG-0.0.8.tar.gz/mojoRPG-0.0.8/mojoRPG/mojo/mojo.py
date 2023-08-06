import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from itertools import islice
import bisect
import click
import dice

plt.style.use('ggplot')

DVALUES = {}
for n in range(2,100):
  DVALUES[n] = np.array(range(1, n+1))
DEFAULT_DICE_ADD_COUNT = 2
DEFAULT_DIE_NUMBER = 10

def mojo_roll1(base=0, mojo=1, proficiency=10, legendary_bonus=0, bonus=0, die_max=DEFAULT_DIE_NUMBER):
  dice_to_roll = min(mojo, proficiency)
  dice_to_add = min(mojo, 3 + legendary_bonus)
  rolls = []
  rolls = dice.roll(f"{dice_to_roll}d{die_max}^{dice_to_add}")
  return sum(rolls) + base

def mojo_roll(base=0, mojo=1, proficiency=1, legendary_bonus=0, bonus=0, die_max=DEFAULT_DIE_NUMBER):
  dice_to_roll = min(mojo, proficiency)
  dice_to_add = min(mojo, DEFAULT_DICE_ADD_COUNT + legendary_bonus)

  # roll all the dice and sort from lowest to hieghest
  rolls = []
  roll_sum = base+bonus
  for n in range(dice_to_roll):
    roll = np.random.choice(DVALUES[die_max])
    bisect.insort(rolls, roll)


  # # get the last (heighest) value
  for n in range(dice_to_roll-dice_to_add, dice_to_roll):
    roll_sum += rolls[n]
    # if the highest value is the max value then add another roll
    # if rolls[dice_to_roll-1] 10:
    if rolls[n] >= die_max:
      new_roll = np.random.choice(DVALUES[die_max])
      roll_sum += new_roll
  return roll_sum

def damage_roll(mroll, target, dstring, extra=0):
  if mroll < target:
    return 0
  roll_sum = 0
  # for n in range(dcount):
  #   roll_sum += np.random.choice(DVALUES[ddie])
  # return (mroll - target) + roll_sum + extra
  return(sum(dice.roll(dstring)) + (mroll - target) + extra)

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
  samples = 1000

  ax = []
  fig, ax = plt.subplots(nrows=10, sharey=True, figsize=(13,4))

  for m in range(10):
    rolls = []
    vmax = 0
    crit = 0
    hit = 0
    rsum = 0
    for n in range(samples):
      mroll = mojo_roll1(base=base, mojo=m+1, proficiency=proficiency, bonus=bonus)
      # print(mroll)
      rolls.append(mroll)
      rsum+=mroll
      if mroll > 20:
        crit += 1
      if mroll > target:
        hit += 1
      if vmax < mroll:
        vmax = mroll

    print(f"Above {target}: {hit/samples*100}%")
    print(f"Above 20: {crit/samples*100}%")
    print(f"Average roll: {round(rsum/samples, 2)}")
    print(f"Max roll: {vmax}")

    sns.histplot(rolls, ax=ax[m], bins=30+base, binrange=[0, 30+base]).set(title=f'Mojo: {m+1}')
  plt.show()

@characterize.command()
@click.option("-m", "--mojo", default=3, type=int, help="Number of mojo points to use.")
@click.option("-b", "--base", default=0, type=int, help="Attribute Base value.")
@click.option("-p", "--proficiency", default=1, type=int, help="Proficiency.")
@click.option("-o", "--bonus", default=0, type=int, help="What die to roll.")
@click.option("-t", "--target", default=15, type=int, help="Target AC (after defensive bonus).")
@click.option("-a", "--armor", default=15, type=int, help="Target AC (after defensive bonus).")
@click.option("-d", "--ddie", default=1, type=int, help="Damage Die to roll.")
@click.option("-c", "--dcount", default=1, type=int, help="Damage Dice count to roll.")
@click.option("-e", "--extra", default=0, type=int, help="Extra Damage addition.")
def damage(
  mojo,
  base,
  proficiency,
  bonus,
  target,
  armor,
  ddie,
  dcount,
  extra,
):
  vmax = 0
  damage_sum = 0
  hit = 0
  samples = 10000
  print(f"Executing Damage Modeling. After running {samples} random rolls:")
  print(f"An attacking character with combat base of {base} and proficiency of {proficiency}. Using {mojo} mojo.")
  print(f"The algorithm is rolling {max(mojo, proficiency)} dice and adding {DEFAULT_DICE_ADD_COUNT} d{DEFAULT_DIE_NUMBER} dice. {mojo}({DEFAULT_DICE_ADD_COUNT})d{DEFAULT_DIE_NUMBER}")
  print(f"Damage is {dcount}d{ddie} with an extra bonus of {extra}")
  print(f"Hit success and damage calculated for an AC of {target} on the defending character.")
  rolls = []
  for n in range(samples):
    mroll = mojo_roll(base=base, mojo=mojo, proficiency=proficiency, bonus=bonus)
    damage = damage_roll1(target=target, mroll=mroll, ddie=ddie, dcount=dcount, extra=extra)
    rolls.append(damage)
    if mroll > target:
      hit += 1
      damage_sum += damage
    if vmax < damage:
      vmax = damage

  print(f"The Attacking Character hit AC:{target} {hit/samples*100}% of the time.")
  print(f"Damage: When the attack is successfull the average damage is {round(damage_sum/hit, 2)} with a maximum of {vmax}")

  # fig, (ax1) = plt.subplots(ncols=1, sharey=True, figsize=(13,4))
  # sns.histplot(rolls, ax=ax1, binrange=[0, max(rolls)])
  # plt.show()

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
  print(mojo_roll1(base=base, mojo=mojo, proficiency=proficiency, bonus=bonus))


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
    rolls.append(mojo_roll1(base=base, proficiency=proficiency, mojo=mojo, bonus=bonus))
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
  print(mojo_roll(base=base, proficiency=proficiency, mojo=mojo, bonus=bonus))

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
    mroll = mojo_roll1(base=base1, mojo=mojo1, proficiency=proficiency1, bonus=bonus1)
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
    mroll = mojo_roll1(base=base2, mojo=mojo2, proficiency=proficiency2, bonus=bonus2)
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
