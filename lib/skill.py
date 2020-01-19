# -*- coding: UTF-8 -*-
"""
Original Author: Harrygiel
Contributors: Lamphobic
Purpose: Produce all pages directly related to skills.
"""

import os, json, sys, datetime

import lib.extractlib as lib
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
import lib.wikilib as wiki

def skill_info(skill_json):
#Get every information of a skill:
#ID, name, description, tags, cost, consumption, bonus, reward, requirement, need, level scaling
	skill = {}
	skill['id'] = skill_json.get('id')
	if skill_json.get('name') is not None:
		skill['name'] = skill_json.get('name').title()
	else:
		skill['name'] = skill['id'].title()

	skill['sym']  = skill_json.get('sym')

	skill['desc']     = skill_json.get('desc')

	if skill_json.get('tags') is not None:
		skill['tags'] = skill_json.get('tags').split(",")
	else:
		skill['tags'] = []

	if skill_json.get('buy') is not None:
		skill['cost']  = skill_json.get('buy')
	else:
		skill['cost']  = {}

	if skill_json.get('run') is not None:
		skill['consumption']  = skill_json.get('run')
	else:
		skill['consumption']  = {}

	if skill_json.get('mod') is not None:
		skill['bonus']  = skill_json.get('mod')
		skill['mod']  = skill_json.get('mod')
	else:
		skill['bonus']  = {}
		skill['mod']  = {}

	if skill_json.get('result') is not None:
		skill['reward']  = skill_json.get('result')
	else:
		skill['reward']  = {}

	if skill_json.get('need') is not None:
		skill['need']  = skill_json.get('need')
	else:
		skill['need']  = {}

	if skill_json.get('level') is not None:
		skill['level_scaling']  = skill_json.get('level')
	else:
		skill['level_scaling']  = "1"

	if skill_json.get('require') is not None:
		skill['require'] = skill_json.get('require')
	else: 
		skill['require'] = "Nothing"

	return skill



def get_full_skill_list():
	result_list = lib.get_json("data/", "skills")
	skill_list = list()
	for json_value in result_list:
		skill_list.append(skill_info(json_value))
	return skill_list


def generate_individual_skl_page(res):
	pass

def generate_wiki(main_only=False):
	global lists
	lists = {
		"action": action.get_full_action_list(),
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
	ret = list()
	
	table_keys = ['Name', 'Description', 'tags', 'Cost', 'Consumption', 'Stat Bonus', 'Reward', 'Requirement', 'Need', 'Level Scaling'] 
	table_lines = []
	result_list = lib.get_json("data/", "skills")
	for json_value in result_list:
		skill_json = skill_info(json_value)
		table_line = []
		# NAME part
		if skill_json.get('sym') is not None:
			table_line.append('| <span id="' + str(skill_json['id']) + '">' + skill_json['sym'] + '[[' +  str(skill_json['name']).capitalize() + ']]</span>')
		else:
			table_line.append('| <span id="' + str(skill_json['id']) + '">[[' +  str(skill_json['name']).capitalize() + ']]</span>')

		# Description part
		table_line.append(str(skill_json['desc']))

		# Tags part
		tmp_cell = ""
		for tag in skill_json['tags']:
			tmp_cell += str(tag) + "<br/>"
		table_line.append(str(tmp_cell))

		# Cost part
		tmp_cell = ""
		for mod_key in skill_json['cost']:
			tmp_cell += (str(mod_key) + ": " + str(skill_json['cost'][mod_key]) + '<br/>')
		table_line.append(str(tmp_cell))

		# consumption part
		tmp_cell = ""
		for mod_key in skill_json['consumption']:
			tmp_cell += (str(mod_key) + ": " + str(skill_json['consumption'][mod_key]) + '<br/>')
		table_line.append(str(tmp_cell))

		# bonus part
		tmp_cell = ""
		for mod_key in skill_json['bonus']:
			tmp_cell += (str(mod_key) + ": " + str(skill_json['bonus'][mod_key]) + '<br/>')
		table_line.append(str(tmp_cell))

		# reward part
		tmp_cell = ""
		for mod_key in skill_json['reward']:
			tmp_cell += (str(mod_key) + ": " + str(skill_json['reward'][mod_key]) + '<br/>')
		table_line.append(str(tmp_cell))

		# Requirement part
		table_line.append(str(skill_json['require'].replace("&&", "<br/>").replace("||", "<br/>OR<br/>")))

		# need part
		if isinstance(skill_json['need'], str):
			table_line.append(skill_json['need'])
		else:
			tmp_cell = ""
			for need_val in skill_json['need']:
				tmp_cell += (str(need_val) + '<br/>')
			table_line.append(str(tmp_cell))

		#level scaling part
		table_line.append(str(skill_json['level_scaling']))
		
		# Add line to lines
		table_lines.append(table_line)
		
		if not main_only:
			generate_individual_skl_page(skill_json)
			ret.append(resource_json['name'])

	with open("skills.txt", "w", encoding="UTF-8") as wiki_dump:
		wiki_dump.write('This page has been automatically updated the ' + str(datetime.datetime.now()) + "\n")
		wiki_dump.write("\n==Main School==\n")
		wiki_dump.write("List of the main schools of Theory of Magic\n")
		wiki_dump.write(wiki.make_table(table_keys, table_lines, table_filter=[[2, "'t_school' in cell"]]).replace(".max", " max").replace(".rate", " rate"))

		wiki_dump.write("\n==Elemental School==\n")
		wiki_dump.write("List of the elemental schools of Theory of Magic\n")
		wiki_dump.write(wiki.make_table(table_keys, table_lines, table_filter=[[2, "'elemental' in cell"]]).replace(".max", " max").replace(".rate", " rate"))

		wiki_dump.write("\n==Evil only==\n")
		wiki_dump.write("List of skill who need you to be evil\n")
		wiki_dump.write(wiki.make_table(table_keys, table_lines, table_filter=[[7, "'g.evil>0' in cell and not('OR' in cell)"]]).replace(".max", " max").replace(".rate", " rate"))

		wiki_dump.write("\n==Good only==\n")
		wiki_dump.write("List of skill who need you to be good\n")
		wiki_dump.write(wiki.make_table(table_keys, table_lines, table_filter=[[7, "'g.evil<=0' in cell and not('OR' in cell)"]]).replace(".max", " max").replace(".rate", " rate"))

		wiki_dump.write("\n==Full List==\n")
		wiki_dump.write(wiki.make_table(table_keys, table_lines).replace(".max", " max").replace(".rate", " rate"))

		return ret