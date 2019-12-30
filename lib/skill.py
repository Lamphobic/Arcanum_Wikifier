# -*- coding: UTF-8 -*-

import os, json, sys
import lib.extractlib as lib
import lib.wikilib as wiki

def skill_info(skill_json):
#Get every information of a skill:
#ID, name, description, tags, cost, consumption, bonus, reward, requirement, need, level scaling
	skill = {}
	skill['id'] = skill_json.get('id')
	if skill_json.get('name') != None:
		skill['name'] = skill_json.get('name')
	else:
		skill['name'] = skill['id']

	skill['sym']  = skill_json.get('sym')

	skill['desc']     = skill_json.get('desc')

	if skill_json.get('tags') != None:
		skill['tags'] = skill_json.get('tags').split(",")
	else:
		skill['tags'] = []

	if skill_json.get('buy') != None:
		skill['cost']  = skill_json.get('buy')
	else:
		skill['cost']  = {}

	if skill_json.get('run') != None:
		skill['consumption']  = skill_json.get('run')
	else:
		skill['consumption']  = {}

	if skill_json.get('mod') != None:
		skill['bonus']  = skill_json.get('mod')
	else:
		skill['bonus']  = {}

	if skill_json.get('result') != None:
		skill['reward']  = skill_json.get('result')
	else:
		skill['reward']  = {}

	if skill_json.get('need') != None:
		skill['need']  = skill_json.get('need')
	else:
		skill['need']  = {}

	if skill_json.get('level') != None:
		skill['level_scaling']  = skill_json.get('level')
	else:
		skill['level_scaling']  = "1"

	if skill_json.get('require') != None:
		skill['require'] = skill_json.get('require')
	else: 
		skill['require'] = "Nothing"

	return skill



def get_full_skill_list():
	result_list = lib.get_json("data/", "skill")
	skill_list
	for json_value in result_list:
		skill_list.append(skill_info(json_value))
	return skill_list



def skill_wiki():
	table_keys = ['Name', 'Description', 'tags', 'Cost', 'Consumption', 'Stat Bonus', 'Reward', 'Requirement', 'Need', 'Level Scaling'] 
	table_lines = []
	result_list = lib.get_json("data/", "skills")
	for json_value in result_list:
		skill_json = skill_info(json_value)
		table_line = []
		# NAME part
		if skill_json.get('sym') != None:
			table_line.append('| <span id="' + str(skill_json['id']) + '">' + skill_json['sym'] + '[[' +  str(skill_json['name']) + ']]</span>')
		else:
			table_line.append('| <span id="' + str(skill_json['id']) + '">[[' +  str(skill_json['name']) + ']]</span>')

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

		table_lines.append(table_line)

	with open("skills.txt", "w", encoding="UTF-8") as wiki_dump:
		wiki_dump.write("\n==Main School==\n")
		wiki_dump.write("List of the main schools of Theory of Magic\n")
		wiki_dump.write(wiki.make_table(table_keys, table_lines, table_filter=[[2, "'t_school' in cell"]]))

		wiki_dump.write("\n==Elemental School==\n")
		wiki_dump.write("List of the elemental schools of Theory of Magic\n")
		wiki_dump.write(wiki.make_table(table_keys, table_lines, table_filter=[[2, "'elemental' in cell"]]))

		wiki_dump.write("\n==Evil only==\n")
		wiki_dump.write("List of skill who need you to be evil\n")
		wiki_dump.write(wiki.make_table(table_keys, table_lines, table_filter=[[7, "'g.evil>0' in cell and not('OR' in cell)"]]))

		wiki_dump.write("\n==Good only==\n")
		wiki_dump.write("List of skill who need you to be good\n")
		wiki_dump.write(wiki.make_table(table_keys, table_lines, table_filter=[[7, "'g.evil<=0' in cell and not('OR' in cell)"]]))

		wiki_dump.write("\n==Full List==\n")
		wiki_dump.write(wiki.make_table(table_keys, table_lines))
