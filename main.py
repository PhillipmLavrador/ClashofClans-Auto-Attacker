from cocapi import Cocapi
import time

client_1 = Cocapi()
troops = {"giant" : 11, "barbarian" : 37, "archer" : 128}
spells = {"lightning": 11}
dark_elixir = 6000
loot = 1200000
while True:
    client_1.train_troops(troops)
    client_1.brew_spells(spells)
    client_1.wait_for_troops()
    loot_finds = client_1.look_for_loot(dark_elixir_goal=dark_elixir, loot_goal=loot)
    if loot_finds[1] >= dark_elixir:
        client_1.lightning_dark_collector()
    if loot_finds[0] >= loot:
        client_1.attack(troops=troops, king=True, queen=True, warden=True, champion=False)
    client_1.wait_till_base()