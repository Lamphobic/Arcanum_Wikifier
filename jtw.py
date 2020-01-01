# -*- coding: UTF-8 -*-

import os, json, sys
import lib.monster as monster
import lib.dungeon as dungeon
import lib.resource as resource
import lib.furniture as furniture
import lib.skill as skill
import lib.spell as spell
import lib.home as home
import lib.potion as potion
import lib.tom_class as tom_class

'''{{{{}}}}
TODO
*use the good files, not all the files
spell: blade and bladelore collide. json problem ?
{{{}}}'''

for arg in sys.argv[1:]:
	if "monsters" in arg.lower():
		monster.monster_wiki()
	elif "dungeons" in arg.lower():
		dungeon.dungeon_wiki()
	elif "furnitures" in arg.lower():
		furniture.furniture_wiki()
	elif "skills" in arg.lower():
		skill.skill_wiki()
	elif "spells" in arg.lower():
		spell.spell_wiki()
	elif "homes" in arg.lower():
		home.home_wiki()
	elif "potions" in arg.lower():
		potion.potion_wiki()
	elif "classes" in arg.lower():
		tom_class.tom_class_wiki()
	elif "all" in arg.lower():
		monster.monster_wiki()
		dungeon.dungeon_wiki()
		furniture.furniture_wiki()
		skill.skill_wiki()
		spell.spell_wiki()
		home.home_wiki()
		potion.potion_wiki()
		tom_class.tom_class_wiki()
	else:
		print("python (3.8) jtw.py all|monsters|dungeons|furnitures|skills|spells|homes|potions|classes")

'''
Finished
'''
#monster.monster_wiki()
#dungeon.dungeon_wiki()
#furniture.furniture_wiki()
#skill.skill_wiki()
#spell.spell_wiki()
#home.home_wiki()
#potion.potion_wiki()
#tom_class.tom_class_wiki()
'''
Partially finished
'''
#resource.resource_wiki()

'''
Missing (in order of importance):

Actions
Upgrades
Locales
'''

'''
TMP
'''
#monster.monster_csv()