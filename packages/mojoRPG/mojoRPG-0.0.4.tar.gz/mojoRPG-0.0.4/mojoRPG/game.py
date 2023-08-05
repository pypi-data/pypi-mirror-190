import click
import numpy as np
from .character import Character
from .mojocore import Die, Mojo

@click.group()
def cli():
  pass

@cli.command()
@click.option("--mojo1", default=3, type=int, help="Number of mojo points to start with.")
@click.option("--oMojo1", default=3, type=int, help="Number of mojo points to use on offense.")
@click.option("--dMojo1", default=1, type=int, help="Number of mojo points to use on defense.")
@click.option("--askill1", default=1, type=int, help="Attack Skill")
@click.option("--dskill1", default=1, type=int, help="Defense Skill")
@click.option("--proficiency1", default=10, type=int, help="Proficiency.")
@click.option("--bonus1", default=0, type=int, help="What die to roll.")
@click.option(
    "--armor1", default=0, type=int, help="Target AC (after defensive bonus)."
)
@click.option("--ddsides1", default=6, type=int, help="Damage die to roll.")
@click.option("--ddcount1", default=1, type=int, help="Number of damage dice to roll.")
@click.option("--extra1", default=0, type=int, help="Extra Damage addition.")
@click.option("--hp1", default=50, type=int, help="Extra Damage addition.")
@click.option("--mojo2", default=3, type=int, help="Number of mojo points to start with.")
@click.option("--oMojo2", default=3, type=int, help="Number of mojo points to use on offense.")
@click.option("--dMojo2", default=1, type=int, help="Number of mojo points to use on defense.")
@click.option("--askill2", default=1, type=int, help="Attack Skill")
@click.option("--dskill2", default=1, type=int, help="Defense Skill")
@click.option("--proficiency2", default=10, type=int, help="Proficiency.")
@click.option("--bonus2", default=0, type=int, help="What die to roll.")
@click.option(
    "--armor2", default=0, type=int, help="Target AC (after defensive bonus)."
)
@click.option("--ddsides2", default=6, type=int, help="Damage die to roll.")
@click.option("--ddcount2", default=1, type=int, help="Number of damage dice to roll.")
@click.option("--extra2", default=0, type=int, help="Extra Damage addition.")
@click.option("--hp2", default=50, type=int, help="Extra Damage addition.")
@click.option("-a/-m", "--auto/--manual", default=False, help="Auto answer prompts.")
def fight(
    mojo1,
    omojo1,
    dmojo1,
    askill1,
    dskill1,
    proficiency1,
    bonus1,
    armor1,
    ddsides1,
    ddcount1,
    extra1,
    hp1,
    mojo2,
    omojo2,
    dmojo2,
    askill2,
    dskill2,
    proficiency2,
    bonus2,
    armor2,
    ddsides2,
    ddcount2,
    extra2,
    hp2,
    auto,
):
    player1 = Character(
        name="Fred",
        offense_skill=askill1,
        defense_skill=dskill1,
        armor=armor1,
        ddsides=ddsides1,
        ddcount=ddcount1,
        hit_points = hp1,
        mojo = mojo1,
        oMojo = omojo1,
        dMojo = dmojo1,
    )
    player2 = Character(
        name="Bob",
        offense_skill=askill2,
        defense_skill=dskill2,
        armor=armor2,
        ddsides=ddsides2,
        ddcount=ddcount2,
        hit_points = hp2,
        mojo = mojo2,
        oMojo = omojo2,
        dMojo = dmojo2,
    )
    player1.print()
    player2.print()
    player1.rollInitiative()
    player2.rollInitiative()

    # move this to mojo core
    queue = []
    if player1.initiative > player2.initiative:
      queue.append((player1, player2))
      queue.append((player2, player1))
    else:
      queue.append((player2, player1))
      queue.append((player1, player2))

    round_num = 0
    while player1.hp > 0 and player2.hp > 0:
      round_num += 1
      print(f"============ Round: {round_num} ============ {player1.name} (hp:{player1.hp} mojo:{player1.mojo}) {player2.name} (hp:{player2.hp} mojo:{player2.mojo})")
      for o, d in queue:
        if o.mojo <= 0:
          print(f"{o.name} has no mojo left for this round, skipping turn")
        else:
          print(f"It is {o.name}'s turn. You have {o.mojo} mojo. Enter offensive mojo to use:", end=' ')
          if auto:
            oMojoToUse = o.default_offense_mojo
          else:
            oMojoToUse = int(input() or o.default_offense_mojo)
          if oMojoToUse == 0:
            continue
          print(f"{d.name} is defending. You have {d.mojo} mojo. Enter deffensive mojo to use:", end=' ')
          if auto:
            dMojoToUse = d.default_defense_mojo
          else:
            dMojoToUse = int(input() or d.default_defense_mojo)
          o.attack(d, oMojoToUse, dMojoToUse)
        if d.hp <= 0:
          break
      player1.endRound()
      player2.endRound()

    for p in [player1, player2]:
      print(f"==== {p.name} Stats ==== (hp:{p.hp} mojo:{p.mojo})")
      attack_rolls = [actions["attack"]["value"] for actions in p.actions]
      max_attack_roll = max(attack_rolls)
      average_attack_roll = sum(attack_rolls)/len(attack_rolls)
      print(f"Max Attack Roll:{max_attack_roll} Average Attack Roll:{round(average_attack_roll, 2)}")

      overHits = [actions["attack"]["overHit"] for actions in p.actions]
      overHit_count = np.count_nonzero(overHits)
      average_overHit = overHit_count/len(overHits)*100
      print(f"Hits:{overHit_count} out of {len(overHits)} Average:{round(average_overHit, 2)}%")

      overDamages = [actions["attack"]["overDamage"] for actions in p.actions]
      overDamage_count = np.count_nonzero(overDamages)
      average_overDamage = overDamage_count/len(overDamages)*100
      print(f"Damaging Blows:{overDamage_count} out of {len(overDamages)} Average:{round(average_overDamage, 2)}%")

      damages_rolls = [actions["damage"]["value"] for actions in p.actions]
      max_damage_roll = max(damages_rolls)
      average_damage_roll = sum(damages_rolls)/len(damages_rolls)
      print(f"Max Damage Roll:{max_damage_roll} Average Damage Roll:{round(average_damage_roll, 2)}")

      total_damages = [actions["total_damage"] for actions in p.actions]
      max_total_damage = max(total_damages)
      average_total_damage = round(sum(total_damages)/len(total_damages), 2)
      average_hit_damage = round(sum(total_damages)/overDamage_count, 2)
      print(f"Max Total Damage:{max_total_damage} Average Total Damage:{average_total_damage} Average Damage on hit:{average_hit_damage}")


if __name__ == "__main__":
    cli()
