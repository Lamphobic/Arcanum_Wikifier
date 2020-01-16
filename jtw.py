# -*- coding: UTF-8 -*-
"""
Original Author: Harrygiel
Contributors: Lamphobic
Purpose: Main driver of the Arcanium Wikifier
"""


import os, json, sys
import lib.wikilib as wiki
import lib.action as action
import lib.dungeon as dungeon
import lib.furniture as furniture
import lib.home as home
import lib.monster as monster
import lib.potion as potion
import lib.resource as resource
import lib.skill as skill
import lib.spell as spell
import lib.tom_class as tom_class
import lib.upgrade as upgrade

'''{{{{}}}}
TODO
*use the good files, not all the files
spell: blade and bladelore collide. json problem ?
{{{}}}'''

def main(argv):
	print(argv)
	online_update=False

	for arg in argv[1:]:
		if "-on" in arg.lower():
			online_update=True
			
	global file_names
	global page_names
	file_names = []
	page_names = []
	
	switch = {
		"actions": gen_actions,
		"dungeons": gen_dungeons,
		"furnitures": gen_furnitures,
		"homes": gen_homes,
		"monsters": gen_monsters,
		"potions": gen_potions,
		"skills": gen_skills,
		"spells": gen_spells,
		"resources": gen_resources,
		"classes": gen_classes,
		"all": gen_all,
		"-on": on
	}
	
	if len(argv) == 1:
		print("python (3.8) jtw.py actions|dungeons|furnitures|homes|monsters|homes|potions|skills|spells|resources|classes|all")
	
	for arg in argv[1:]:
		func = switch.get(arg.lower(), lambda: print("python (3.8) jtw.py actions|dungeons|furnitures|homes|monsters|potions|skills|spells|resources|classes|all"))
		func()

	if online_update==True:
		print("Automatically uploading:")
		for i in range(0,len(file_names)):
			if page_names[i] is "Classes":
				print("can't upload classes yet: the manual page is better")
			else:
				wiki.bot_update(page_names[i], file_names[i])

def gen_actions():
	file_names.append(action.generate_wiki())
	page_names.append("Actions")

def gen_dungeons():
	file_names.append(dungeon.generate_wiki())
	page_names.append("Dungeons")

def gen_furnitures():
	file_names.append(furniture.generate_wiki())
	page_names.append("Furnitures")

def gen_homes():
	file_names.append(homes.generate_wiki())
	page_names.append("Homes")

def gen_monsters():
	file_names.append(monster.generate_wiki())
	page_names.append("Monsters")

def gen_potions():
	file_names.append(potion.generate_wiki())
	page_names.append("Potions")

def gen_skills():
	file_names.append(skill.generate_wiki())
	page_names.append("Skills")

def gen_spells():
	file_names.append(spell.generate_wiki())
	page_names.append("Spells")

def gen_resources():
	res = resource.generate_wiki()
	file_names.append("resources.txt")
	page_names.append("Resources")
	file_names.extend(res)
	sez = ['_'.join(e.split(' ')) for e in list.copy(res)]
	page_names.extend(sez)

def gen_classes():
	file_names.append(tom_class.generate_wiki())
	page_names.append("Classes")

def gen_upgrades():
	file_names.append(upgrade.generate_wiki())
	page_names.append("Upgrades")

def gen_all():
	gen_upgrades()
	gen_classes()
	gen_resources()
	gen_spells()
	gen_skills()
	gen_potions()
	gen_monsters()
	gen_homes()
	gen_furnitures()
	gen_dungeons()
	gen_actions()
	
def on():
	pass
	
				
main(sys.argv)
print(file_names)
print(page_names)
'''
Partially finished
'''
#resource.resource_wiki()

'''
Missing (in order of importance):

Locales
'''

'''
TMP
'''
#monster.monster_csv()