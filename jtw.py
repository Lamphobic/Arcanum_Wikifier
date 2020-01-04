# -*- coding: UTF-8 -*-

import os, json, sys
import lib.wikilib as wiki
import lib.monster as monster
import lib.dungeon as dungeon
import lib.resource as resource
import lib.furniture as furniture
import lib.skill as skill
import lib.spell as spell
import lib.home as home
import lib.potion as potion
import lib.tom_class as tom_class
import lib.action as action
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
	file_names = []
	page_names = []
	for arg in argv[1:]:
		if "monsters" in arg.lower():
			file_names.append(monster.generate_wiki())
			page_names.append("Monsters")
		elif "dungeons" in arg.lower():
			file_names.append(dungeon.generate_wiki())
			page_names.append("Dungeons")
		elif "furnitures" in arg.lower():
			file_names.append(furniture.generate_wiki())
			page_names.append("Furniture")
		elif "skills" in arg.lower():
			file_names.append(skill.generate_wiki())
			page_names.append("Skills")
		elif "spells" in arg.lower():
			file_names.append(spell.generate_wiki())
			page_names.append("Spells")
		elif "homes" in arg.lower():
			file_names.append(home.generate_wiki())
			page_names.append("Homes")
		elif "potions" in arg.lower():
			file_names.append(potion.generate_wiki())
			page_names.append("Potions(item)")
		elif "classes" in arg.lower():
			file_names.append(tom_class.generate_wiki())
			page_names.append("Classes")
		elif "actions" in arg.lower():
			file_names.append(action.generate_wiki())
			page_names.append("Actions")
		elif "upgrades" in arg.lower():
			file_names.append(upgrade.generate_wiki())
			page_names.append("Test")
		elif "all" in arg.lower():
			file_names.append(monster.generate_wiki())
			page_names.append("Monsters")
			file_names.append(dungeon.generate_wiki())
			page_names.append("Dungeons")
			file_names.append(furniture.generate_wiki())
			page_names.append("Furniture")
			file_names.append(skill.generate_wiki())
			page_names.append("Skills")
			file_names.append(spell.generate_wiki())
			page_names.append("Spells")
			file_names.append(home.generate_wiki())
			page_names.append("Homes")
			file_names.append(potion.generate_wiki())
			page_names.append("Potions(item)")
			file_names.append(tom_class.generate_wiki())
			page_names.append("Classes")
			file_names.append(action.generate_wiki())
			page_names.append("Actions")
		elif "-on" in arg.lower():
			pass
		else:
			print("python (3.8) jtw.py all|monsters|dungeons|furnitures|skills|spells|homes|potions|classes")
			break

	if online_update==True:
		print("Automatically uploading:")
		for i in range(0,len(file_names)):
			if page_names[i] == "Classes":
				print("can't upload classes yet: the manual page is better")
			else:
				wiki.bot_update(page_names[i], file_names[i])

main(sys.argv)

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