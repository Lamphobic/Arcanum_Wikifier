# -*- coding: UTF-8 -*-
"""
Original Author: Harrygiel
Contributors: Lamphobic
Purpose: Main driver of the Arcanium Wikifier
"""


import os, json, sys
import lib.wikilib as wiki
import lib.task as task
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
	
	global online_update
	global only_generate_main_pages
	global test_update
	global no_graph
	global diff_only_up
	
	online_update = False
	only_generate_main_pages = False
	test_update = False
	no_graph = True
	diff_only_up = False
	
	mains = [
		"tasks",
		"dungeons",
		"furnitures",
		"homes",
		"monsters",
		"potions",
		"skills",
		"spells",
		"resources",
		"classes",
		"upgrade"
		]
			
	global file_names
	global page_names
	file_names = []
	page_names = []
	
	global id_name_map
	id_name_map = {}
	lists = {
		"task": task.get_full_task_list(),
		"dungeon": dungeon.get_full_dungeon_list(),
		"furniture": furniture.get_full_furniture_list(),
		"home": home.get_full_home_list(),
		"monster": monster.get_full_monster_list(),
		"potion": potion.get_full_potion_list(),
		"resource": resource.get_full_resource_list(),
		"skill": skill.get_full_skill_list(),
		"spell": spell.get_full_spell_list(),
		"class": tom_class.get_full_tom_class_list(),
		"upgrade": upgrade.get_full_upgrade_list()
		}
	for l in lists:
		for e in lists[l]:
			id_name_map[e['id']] = e
	
	
	"""
	col = {}
	tmp = {}
	sorted_l = sorted(id_name_map.keys())
	for e in sorted_l:
		name = str(id_name_map[e]['name'])
		if tmp.get(name):
			col[e] = name
			col[tmp[name]] = name
		else:
			tmp[name] = e
	for e in sorted(col.keys(), key=lambda id: str(id_name_map[id]['name'])):
		#print(e + ': ' + id_name_map[e]['name'] + ', ' + id_name_map[e]['type'])
		print("'" + e + "': '" + id_name_map[e]['name'] + "',")
	
	with open('id map.txt', "w", encoding="UTF-8") as page:
		sorted_l = sorted(id_name_map.keys())
		for e in sorted_l:
			page.write(e + ': ' + id_name_map[e]['name'] + ', ' + id_name_map[e]['type'] + '\n')
	"""
	
	
	help_switch = {
		"tasks": None,
		"dungeons": None,
		"furnitures": None,
		"homes": None,
		"monsters": None,
		"potions": None,
		"skills": None,
		"spells": None,
		"resources": None,
		"classes": None,
		"upgrades": None,
		"all": None,
		"-on": None,
		"-test": None,
		"-main": None,
		"-diff": None,
		"-nograph": None,
		"-help": flg_help,
		"-h": flg_help,
		"-?": flg_help,
		"help": flg_help,
		"?": flg_help
	}
	
	for arg in argv[1:]:
		func = help_switch.get(arg.lower(), flg_help)
		if func is not None:
			func()
	
	flags_switch = {
		"-on": flg_on,
		"-test": flg_test,
		"-main": flg_main_only,
		"-nograph": flg_no_graph,
		"-diff": flg_differences_only,
		"-help": None,
		"-h": None,
		"-?": None,
		"help": None,
		"?": None
	}
	
	for arg in argv[1:]:
		func = flags_switch.get(arg.lower())
		if func is not None:
			func()
	
	switch = {
		"tasks": gen_tasks,
		"dungeons": gen_dungeons,
		"furnitures": gen_furnitures,
		"homes": gen_homes,
		"monsters": gen_monsters,
		"potions": gen_potions,
		"skills": gen_skills,
		"spells": gen_spells,
		"resources": gen_resources,
		"classes": gen_classes,
		"upgrades": gen_upgrades,
		"all": gen_all,
		"-on": None,
		"-test": None,
		"-main": None,
		"-nograph": None,
		"-diff": None,
		"-help": None,
		"-h": None,
		"-?": None,
		"help": None,
		"?": None
	}
	
	if len(argv) == 1:
		flg_help()
	
	for arg in argv[1:]:
		func = switch.get(arg.lower(), flg_help)
		if func is not None:
			func()
		
	print(file_names)
	print(page_names)

	if online_update == True:
		print("Automatically uploading:")
		for i in range(0,len(file_names)):
			if not test_update or page_names[i].lower() in mains:
				if page_names[i] is "Classes":
					print("can't upload classes yet: the manual page is better")
				else:
					if test_update:
						wiki.bot_update("Test"+page_names[i], file_names[i])
					else:
						wiki.bot_update(page_names[i], file_names[i])

def gen_tasks():
	act = task.generate_wiki(id_name_map, main_only=only_generate_main_pages)
	file_names.append("tasks.txt")
	page_names.append("Tasks")
	file_names.extend([(e + '.txt') for e in act])
	page_names.extend(['_'.join(e.split(' ')) for e in act])

def gen_dungeons():
	file_names.append(dungeon.generate_wiki())
	page_names.append("Dungeons")

def gen_furnitures():
	file_names.append(furniture.generate_wiki())
	page_names.append("Furnitures")

def gen_homes():
	file_names.append(home.generate_wiki())
	page_names.append("Homes")

def gen_monsters():
	file_names.append(monster.generate_wiki())
	page_names.append("Monsters")

def gen_potions():
	file_names.append(potion.generate_wiki())
	page_names.append("Potions")

def gen_skills():
	skl = skill.generate_wiki(id_name_map, main_only=only_generate_main_pages, diff_only=diff_only_up)
	file_names.append("skills.txt")
	page_names.append("Skills")
	file_names.extend([(e + '.txt') for e in skl])
	page_names.extend(['_'.join(e.split(' ')) for e in skl])

def gen_spells():
	file_names.append(spell.generate_wiki())
	page_names.append("Spells")

def gen_resources():
	res = resource.generate_wiki(id_name_map, main_only=only_generate_main_pages, diff_only=diff_only_up)
	file_names.append("resources.txt")
	page_names.append("Resources")
	file_names.extend([(e + '.txt') for e in res])
	page_names.extend(['_'.join(e.split(' ')) for e in res])

def gen_classes():
	cls = tom_class.generate_wiki(id_name_map, main_only=only_generate_main_pages, no_graph_gen=no_graph)
	file_names.append("classes.txt")
	page_names.append("Classes")
	file_names.extend([(e + '.txt') for e in cls])
	page_names.extend(['_'.join(e.split(' ')) for e in cls])

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
	gen_tasks()
	
def flg_on(): #Fully working
	global online_update
	online_update = True
	print("Automatic upload turned on.")
	
def flg_test(): #Fully working
	global test_update
	test_update = True
	print("Uploading to only test pages.")
	
def flg_main_only(): #Partially working
	global only_generate_main_pages
	only_generate_main_pages = True
	print("Generating main pages only.")
	
def flg_no_graph(): #Fully working
	global no_graph
	no_graph = True
	print("Not generating class graph.")
	
def flg_differences_only(): #not working
	global diff_only_up
	diff_only_up = True
	print("Not uploading unchanged files.")
	
def flg_help():
	print("python (3.8) jtw.py [OPTIONS] tasks|dungeons|furnitures|homes|monsters|potions|skills|spells|resources|classes|upgrades|all")
	print("Options")
	print("-on")
	print("\tSets the bot to upload the newly generated pages online.")
	print("-test")
	print("\tIf -on is set, when uploading, uploads only main pages, and uploads them to a test pages. Block uploading of non-main pages.")
	print("-main")
	print("\tProduces only main listing files under the various topics.")
	print("-nograph")
	print("\tDoes not generate graph for classes.")
	print("-diff")
	print("\tNot yet implemented. When -on is active, uploads only files that are different from a previous run of this script.")
	print("-help, -h, help, -?, ?")
	print("\tView this help page.")
	
	exit()
	
				
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