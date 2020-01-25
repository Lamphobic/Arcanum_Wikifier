# -*- coding: UTF-8 -*-
"""
Original Author: Harrygiel
Contributors: Lamphobic
Purpose: Produce all pages directly related to furnitures.
"""

import os, json, sys, datetime, re

import lib.extractlib as lib
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
import lib.wikilib as wiki

def furniture_info(furniture_json):
#Get every information of a furniture:
#ID, name, description, tags, base maximum, cost, bonus, requirement

	furniture = {}
	furniture['type'] = 'furniture'
	furniture['id'] = furniture_json.get('id')
	if furniture_json.get('name') is not None:
		furniture['name'] = furniture_json.get('name').title()
	else:
		furniture['name'] = furniture['id'].title()

	furniture['sym'] = furniture_json.get('sym')



	furniture['desc'] = str(furniture_json.get('desc')).capitalize()

	if furniture_json.get('tags') is not None:
		furniture['tags'] = furniture_json.get('tags').split(",")
	else:
		furniture['tags'] = []

	if furniture_json.get('repeat') is True:
		furniture['base_max'] = None
	elif furniture_json.get('max') is not None:
		furniture['base_max'] = furniture_json.get('max')
	else:
		furniture['base_max'] = 1

	if furniture_json.get('cost') is not None:
		furniture['cost'] = furniture_json.get('cost')
	else:
		furniture['cost'] = {}

	if furniture_json.get('mod') is not None:
		furniture['mod'] = furniture_json.get('mod')
	else:
		furniture['mod'] = {}

	if furniture_json.get('require') is not None:
		furniture['require'] = furniture_json.get('require')
	elif furniture_json.get('need') is not None:
		furniture['require'] = furniture_json.get('need')
	else: 
		furniture['require'] = "Nothing"
	
	furniture['requirements'] = {}
	furniture['requirements']['>'] = {}
	furniture['requirements']['<'] = {}
	requirements = furniture['requirements']
	if furniture_json.get('require') is not None:
		require = furniture_json.get('require')
		if isinstance(require, list):
			for e in require:
				requirements['>'][e] = 1
		else:
			require = require.replace('(', '').replace(')', '').replace('g.', '')
			for e in re.split('&&|\|\|', require):
				if '+' in e:
					reg = '>=|<=|>|<'
					cmp_sign = str(re.search(reg, e).group())
					tmp = re.split(reg, e)
					tmpl = tmp[0].split('+')
					for ent in tmpl:
						if '>=' == cmp_sign:
							requirements['>'][ent] = int(tmp[1])
						elif '>' == cmp_sign:
							requirements['>'][ent] = int(tmp[1]) + 1
						else:
							requirements['<'][ent] = int(tmp[1])
							
				elif bool(re.search('>=|>', e)):
					if '>=' in e:
						s = e.split('>=')
						requirements['>'][s[0]] = int(s[1])
					else:
						s = e.split('>')
						requirements['>'][s[0]] = int(s[1]) + 1
				elif bool(re.search('<=|<', e)):
					s = re.split('<=|<', e)
					requirements['<'][s[0]] = int(s[1])
				else:
					requirements['>'][e] = 1
		
	lib.name_exceptions(furniture)

	return furniture


def get_full_furniture_list():
	result_list = lib.get_json("data/", "furniture")
	furniture_list = list()
	for json_value in result_list:
		furniture_list.append(furniture_info(json_value))
	return furniture_list


def generate_individual_frn_page(furniture_json, diff_only=False):
	name = furniture_json['name'] + ".txt"
	exist = False
	if diff_only and os.path.exists(name):
		name = 'test' + name
		exist = True
	with open(name, "w", encoding="UTF-8") as page:
		page.write("This page has been automatically generated.<br>\n<br>\n")
		page.write(furniture_json['name'] + ' is part of [[' + furniture_json['type'].title() + '|\"' + furniture_json['type'].title() + '\"]]\n')
		#Desc
		if furniture_json['desc']:
			page.write('==Description==\n' + furniture_json['desc'] + '\n')
		#Tags
		if furniture_json['tags']:
			page.write('==Tags==\n' + ' '.join(furniture_json['tags']) + '\n')
		#Base Max
		if str(furniture_json['base_max']) == None:
			page.write('==Base Max==\n' + str(furniture_json['base_max']) + '\n')
		#Cost
		page.write('==Cost==\n')
		tmp_cell = ""
		for mod_key in furniture_json['cost']:
			tmp_cell += ('*' + str(mod_key) + ": " + str(furniture_json['cost'][mod_key]) + '\n')
		page.write(str(tmp_cell))
		#Effects
		if furniture_json['mod']:
			page.write('==Effects==\n')
			for mod_key in furniture_json['mod']:
				page.write('*' + str(mod_key) + ": " + str(furniture_json['mod'][mod_key]) + '\n')
		#Unlock Requirements
		if furniture_json['require'] != "Nothing":
			page.write('==Unlock Requirements==\n')
		if furniture_json['require'] != "Nothing":
			if isinstance(furniture_json['require'], str):
				page.write('*' + str(furniture_json['require'].replace("&&", "\n*").replace("||", "OR")) + '\n')
			else:
				for e in furniture_json['require']:
					page.write('*' + str(e.replace("&&", "\n*").replace("||", "OR")) + '\n')
		
		baffected = False
		bunlock = False
		affected_by = list()
		unlock = {}
		match_id = furniture_json['id'].lower()
		
		#Build Unlocks
		for l in lists:
			unlock = {}
			for e in lists[l]:
				if 'requirements' in e:
					if e['requirements']['<'] or e['requirements']['>']:
						for req_key in e['requirements']['<']:
							match_req = str(req_key).lower()
							if match_id in match_req.split('.'):
								unlock[str(e['requirements']['<'][match_req]) + ' or less ' + '.'.join([x if x != match_id else furniture_json['name'] for x in match_req.split('.')]) + ': [[' + e['type'].title() + '#' + e['id'] + '|' + e['name'] + ']]'] = e['requirements']['<'][match_req]
						for req_key in e['requirements']['>']:
							match_req = str(req_key)
							if match_id in match_req.split('.'):
								unlock[str(e['requirements']['>'][match_req]) + ' or more ' + '.'.join([x if x != match_id else furniture_json['name'] for x in match_req.split('.')]) + ': [[' + e['type'].title() + '#' + e['id'] + '|' + e['name'] + ']]'] = e['requirements']['>'][match_req]
			sorted_l = sorted(unlock, key=unlock.get)
			if unlock:
				if not bunlock:
					page.write('==Unlocks==\n')
					bunlock = True
				page.write(('===' + l + '===\n').title())
				for e in sorted_l:
					page.write('*' + e + '\n')
		
		#Build Affected By
		for l in lists:
			affected_by = list()
			for e in lists[l]:
				if e['mod']:
					for mod_key in e['mod']:
						match_mod = str(mod_key).lower().split('.')
						if match_id in match_mod:
							if match_id != str(mod_key).lower():
								match_mod = [x if x != match_id else furniture_json['name'] for x in match_mod]
								affected_by.append('[[' + e['type'].title() + '#' + e['id'] + '|' + e['name'] + ']]: ' + '.'.join(match_mod) + ": " + str(e['mod'][mod_key]))
			affected_by = list(set(affected_by))
			affected_by.sort()
			if affected_by:
				if not baffected:
					page.write('==Affected By==\n')
					baffected = True
				page.write(('===' + l + '===\n').title())
				for e in affected_by:
					page.write('* ' + e + '\n')
		
		
	if diff_only and exist:
		if not filecmp.cmp(name, name[4:], shallow=False): #are they the same
			#they are not the same
			#remove old file
			os.remove(name[4:])
			#rename new file
			os.rename(name, name[4:])
		else:
			#they are the same
			#remove new file
			os.remove(name)
			return False
	return True


def generate_wiki(id_name_map, main_only=False, diff_only=False):
	global lists
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
	ret = list()
	
	table_keys = ['Name', 'Description', 'Tags', 'Base maximum', 'Cost', 'Bonus', 'Unlock Requirements'] 
	table_lines = []
	result_list = lib.get_json("data/", "furniture")
	result_list = sorted(result_list, key=lambda srt: furniture_info(srt).get('name')) #Presorts results by name.
	for json_value in result_list:
		furniture_json = furniture_info(json_value)
		table_line = []
		# NAME part
		if furniture_json.get('sym') is not None:
			table_line.append('| <span id="' + str(furniture_json['id']) + '">' + furniture_json['sym'] + '[[' +  str(furniture_json['name']) + ']]</span>')
		else:
			table_line.append('| <span id="' + str(furniture_json['id']) + '">[[' +  str(furniture_json['name']) + ']]</span>')

		# Description part
		table_line.append(str(furniture_json['desc']))

		# Tags part
		tmp_cell = ""
		for tag in furniture_json['tags']:
			tmp_cell += str(tag) + "<br/>"
		table_line.append(str(tmp_cell))

		# Base maximum part
		table_line.append(str(furniture_json['base_max'] ))

		# Cost part
		tmp_cell = ""
		for mod_key in furniture_json['cost']:
			tmp_cell += (str(mod_key) + ": " + str(furniture_json['cost'][mod_key]) + '<br/>')
		table_line.append(str(tmp_cell))
		
		# Bonus part
		tmp_cell = ""
		for mod_key in furniture_json['mod']:
			tmp_cell += (str(mod_key) + ": " + str(furniture_json['mod'][mod_key]) + '<br/>')
		table_line.append(str(tmp_cell))

		# Requirement part
		if isinstance(furniture_json['require'],list):
			tmp_cell = ""
			for requirement in furniture_json['require']:
				tmp_cell += str(requirement) + '<br/>'
			table_line.append(str(tmp_cell))
		else:
			table_line.append(str(furniture_json['require'].replace("&&", "<br/>").replace("||", "<br/>OR<br/>").replace("+"," + ")))

		# Add line to lines
		table_lines.append(table_line)
		
		if not main_only:
			if generate_individual_frn_page(furniture_json, diff_only):
				ret.append(furniture_json['name'])

	with open("Furniture.txt", "w", encoding="UTF-8") as wiki_dump:
		wiki_dump.write('This page has been automatically updated the ' + str(datetime.datetime.now()) + "<br/>\n")
		wiki_dump.write("Furniture is a type of item that can be placed in your home at the cost of floor space. They provide various benefits, but the most important, nonobvious benefit is the tags on furniture, since certain furniture tags can unlock certain tasks or skills.\n")

		wiki_dump.write("\n==Gold==\n")
		wiki_dump.write("Increases maximum gold, and sometimes other valuable resources such as gems.:\n")
		wiki_dump.write(wiki.make_table(table_keys, table_lines, table_filter=[[5, "'gold.max' in cell"]]))

		wiki_dump.write("\n==Research==\n")
		wiki_dump.write("Increases at least one of maximum scrolls, maximum codices, maximum starcharts, maximum tomes or maximum rune stone, giving you more research:\n")
		wiki_dump.write(wiki.make_table(table_keys, table_lines, table_filter=[[5, "'scrolls.max' in cell or 'codices.max' in cell or 'tomes.max' in cell or 'runestones.max' in cell or 't_runes.max' in cell or 'starcharts.max' in cell"]]))

		wiki_dump.write("\n==Source==\n")
		wiki_dump.write("List of every item used to be able to discover or use a skill:\n")
		wiki_dump.write(wiki.make_table(table_keys, table_lines, table_filter=[[2, "'source' in cell"], [0, "'loom' in cell"]]))

		wiki_dump.write("\n==Skill max==\n")
		wiki_dump.write("List of every item used to get a higher skill level:\n")
		wiki_dump.write(wiki.make_table(table_keys, table_lines, table_filter=[[5, "'lore.max' in cell"]]))

		wiki_dump.write("\n==Full List==\n")
		wiki_dump.write(wiki.make_table(table_keys, table_lines))
	ret.append('Furniture')
	return ret