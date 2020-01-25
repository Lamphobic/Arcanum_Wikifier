# -*- coding: UTF-8 -*-
"""
Original Author: Harrygiel
Contributors: Lamphobic
Purpose: Produce all pages directly related to upgrades.
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

def extract_effect_key(effect_json):
	return_txt = ""
	if effect_json is not None:
		if (effect_json,str):
			return_txt += str(effect_json)
		else:
			for mod_list in effect_json:
				return_txt += str(mod_list) + ": " + str(extract_effect_key(effect_json[mod_list])) + "<br/>"
	return return_txt

def get_effect_info(effect_json):
	return_txt = ""
	is_treated = False
	for effect_key in effect_json:
		if isinstance(effect_json[effect_key], str):
			return_txt += str(effect_json[effect_key])
		else:
			if isinstance(effect_json[effect_key], list):
				for effect_item in effect_json[effect_key]:
					return_txt += str(effect_item) + ", "
				return_txt = return_txt[:-2]
			else:
				for effect_name in effect_json[effect_key]:
					return_txt += str(effect_name) + ": " + str(extract_effect_key(effect_json[effect_key][effect_name])) + "<br/>"
	return return_txt

def upgrade_info(upgrade_json):
#Get every information of a upgrade:
#ID, name, description, cost, max, effect, require, need
	upgrade = {}
	upgrade['type'] = 'upgrades'
	upgrade['id'] = upgrade_json.get('id')
	if upgrade_json.get('name') is not None:
		upgrade['name'] = upgrade_json.get('name').title()
	else:
		upgrade['name'] = upgrade['id'].title()

	upgrade['sym'] = upgrade_json.get('sym')

	upgrade['desc'] = str(upgrade_json.get('desc')).capitalize()

	if upgrade_json.get('tags') is not None:
		upgrade['tags'] = upgrade_json.get('tags').split(",")
	else:
		upgrade['tags'] = []

	if upgrade_json.get('cost') is not None:
		upgrade['cost'] = upgrade_json.get('cost')
	else:
		upgrade['cost'] = {}

	if upgrade_json.get('max') is not None:
		upgrade['max'] = upgrade_json.get('max')
	else:
		upgrade['max'] = "1"

	upgrade['mod'] = list()
	upgrade['effect']  = {}
	if upgrade_json.get('effect') is not None:
		upgrade['effect']['effect']  = upgrade_json.get('effect')
	if upgrade_json.get('result') is not None:
		upgrade['effect']['result']  = upgrade_json.get('result')
	if upgrade_json.get('mod') is not None:
		upgrade['effect']['mod']  = upgrade_json.get('mod')
		upgrade['mod'] = upgrade_json.get('mod')
		
	upgrade['requirements'] = {}
	upgrade['requirements']['>'] = {}
	upgrade['requirements']['<'] = {}
	requirements = upgrade['requirements']
	if upgrade_json.get('require') is not None:
		require = upgrade_json.get('require')
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
	if upgrade_json.get('need') is not None:
		require = upgrade_json.get('need')
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
							requirements[ent] = int(tmp[1])
						elif '>' == cmp_sign:
							requirements[ent] = int(tmp[1]) + 1
						else:
							requirements[ent] = int(tmp[1])
							
				elif bool(re.search('>=|>', e)):
					if '>=' in e:
						s = e.split('>=')
						requirements['>'][s[0]] = int(s[1])
					else:
						s = e.split('>')
						requirements['>'][s[0]] = int(s[1]) + 1
				elif '<=' in e:
					s = e.split('<=')
					requirements[s[0]] = int(s[1])
				elif '<' in e:
					s = e.split('<')
					requirements['<'][s[0]] = int(s[1]) - 1
				else:
					requirements['>'][e] = 1
					
	
	if upgrade_json.get('require') is not None:
		upgrade['require'] = upgrade_json.get('require')
	else: 
		upgrade['require'] = "Nothing"

	if upgrade_json.get('need') is not None:
		upgrade['need'] = upgrade_json.get('need')
	else: 
		upgrade['need'] = "Nothing"
		
	lib.name_exceptions(upgrade)

	return upgrade


def get_full_upgrade_list():
	result_list = lib.get_json("data/", "upgrades")
	upgrade_list = list()
	for json_value in result_list:
		upgrade_list.append(upgrade_info(json_value))
	return upgrade_list


def generate_individual_upg_page(upgrade_json, diff_only=False):
	name = upgrade_json['name'] + ".txt"
	exist = False
	if diff_only and os.path.exists(name):
		name = 'test' + name
		exist = True
	with open(name, "w", encoding="UTF-8") as page:
		page.write("This page has been automatically generated.<br>\n<br>\n")
		page.write(upgrade_json['name'] + ' is part of [[' + upgrade_json['type'].title() + '|\"' + upgrade_json['type'].title() + '\"]]\n')
		
		#Desc
		if upgrade_json['desc']:
			page.write('==Description==\n' + upgrade_json['desc'] + '\n')
			
		#Tags
		if upgrade_json['tags']:
			page.write('==Tags==\n' + ' '.join(upgrade_json['tags']) + '\n')
			
		#Base Max
		if str(upgrade_json['max']) == None:
			page.write('==Base Max==\n' + str(upgrade_json['max']) + '\n')
			
		#Cost
		page.write('==Cost==\n')
		tmp_cell = ""
		for mod_key in upgrade_json['cost']:
			tmp_cell += ('*' + str(mod_key) + ": " + str(upgrade_json['cost'][mod_key]) + '\n')
		page.write(str(tmp_cell))
		
		#Effects
		if upgrade_json['mod']:
			page.write('==Effects==\n')
			for mod_key in upgrade_json['mod']:
				page.write('*' + str(mod_key) + ": " + str(upgrade_json['mod'][mod_key]) + '\n')
		
		#Unlock Requirements
		if upgrade_json['require'] != "Nothing" and upgrade_json['need'] != "Nothing":
			page.write('==Unlock Requirements==\n')
		if upgrade_json['require'] != "Nothing":
			if isinstance(upgrade_json['require'], str):
				page.write('*' + str(upgrade_json['require'].replace("&&", "\n*").replace("||", "OR")) + '\n')
			else:
				for e in upgrade_json['require']:
					page.write('*' + str(e.replace("&&", "\n*").replace("||", "OR")) + '\n')
		if upgrade_json['need'] != 'Nothing':
			if isinstance(upgrade_json['need'], list):
				for e in upgrade_json['need']:
					page.write('*' + str(e) + '\n')
			else:
				page.write('*' + str(upgrade_json['need']) + '\n')
				
		#Need
		if upgrade_json['need'] != 'Nothing':
			page.write('==task Requirements==\n')
			if isinstance(upgrade_json['need'], list):
				for e in upgrade_json['need']:
					page.write('*' + str(e) + '\n')
			else:
				page.write('*' + str(upgrade_json['need']) + '\n')
		
		baffected = False
		bunlock = False
		affected_by = list()
		unlock = {}
		match_id = upgrade_json['id'].lower()
		
		#Build Unlocks
		for l in lists:
			unlock = {}
			for e in lists[l]:
				if 'requirements' in e:
					if e['requirements']['<'] or e['requirements']['>']:
						for req_key in e['requirements']['<']:
							match_req = str(req_key).lower()
							if match_id in match_req.split('.'):
								unlock[str(e['requirements']['<'][match_req]) + ' or less ' + '.'.join([x if x != match_id else upgrade_json['name'] for x in match_req.split('.')]) + ': [[' + e['type'].title() + '#' + e['id'] + '|' + e['name'] + ']]'] = e['requirements']['<'][match_req]
						for req_key in e['requirements']['>']:
							match_req = str(req_key)
							if match_id in match_req.split('.'):
								unlock[str(e['requirements']['>'][match_req]) + ' or more ' + '.'.join([x if x != match_id else upgrade_json['name'] for x in match_req.split('.')]) + ': [[' + e['type'].title() + '#' + e['id'] + '|' + e['name'] + ']]'] = e['requirements']['>'][match_req]
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
								match_mod = [x if x != match_id else upgrade_json['name'] for x in match_mod]
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
	
	table_keys = ['Name', 'Description', 'Tags', 'Cost', 'Base Max', 'Effect', 'Unlock Requirement', 'Need'] 
	table_lines = []
	school_set = set()
	result_list = lib.get_json("data/", "upgrades")
	result_list = sorted(result_list, key=lambda srt: upgrade_info(srt).get('name')) #Presorts results by name.
	for json_value in result_list:
		upgrade_json = upgrade_info(json_value)
		table_line = []
		# NAME part
		if upgrade_json.get('sym') is not None:
			table_line.append('| <span id="' + str(upgrade_json['id']) + '">' + upgrade_json['sym'] + '[[' +  str(upgrade_json['name']) + ']]</span>')
		else:
			table_line.append('| <span id="' + str(upgrade_json['id']) + '">[[' +  str(upgrade_json['name']) + ']]</span>')

		# Description part
		table_line.append(str(upgrade_json['desc']))

		# Tags part
		tmp_cell = ""
		for tag in upgrade_json['tags']:
			tmp_cell += str(tag) + "<br/>"
		table_line.append(str(tmp_cell))

		# cost part
		tmp_cell = ""
		if isinstance(upgrade_json['cost'],str):
			tmp_cell += (str(upgrade_json['cost']))
		elif isinstance(upgrade_json['cost'], int):
			tmp_cell += ("Gold: " + str(upgrade_json['cost']))
		else:
			for mod_key in upgrade_json['cost']:
				tmp_cell += (str(mod_key) + ": " + str(upgrade_json['cost'][mod_key]) + '<br/>')
		table_line.append(str(tmp_cell))

		# Max part
		table_line.append(str(upgrade_json['max']))

		# Effect part
		table_line.append(str(get_effect_info(upgrade_json['effect'])))

		# Requirement part
		table_line.append(lib.recurs_json_to_str(upgrade_json['require']).replace("&&", "<br/>").replace("||", "<br/>OR<br/>").replace("+"," + "))

		# Need part
		table_line.append(lib.recurs_json_to_str(upgrade_json['need']).replace("&&", "<br/>").replace("||", "<br/>OR<br/>").replace("+"," + "))

		# Add line to lines
		table_lines.append(table_line)
		
		if not main_only:
			if generate_individual_upg_page(upgrade_json, diff_only):
				ret.append(upgrade_json['name'])

	with open("upgrades.txt", "w", encoding="UTF-8") as wiki_dump:
		wiki_dump.write('This page has been automatically updated the ' + str(datetime.datetime.now()) + "<br/>\n__FORCETOC__\n")

		wiki_dump.write("\n==Distance Upgrades==\n")
		wiki_dump.write(wiki.make_table(table_keys, table_lines, table_filter=[[5, "'dist' in cell"]]))

		wiki_dump.write("\n==Space Upgrades==\n")
		wiki_dump.write(wiki.make_table(table_keys, table_lines, table_filter=[[5, "'space' in cell"]]))

		wiki_dump.write("\n==Another Group?==\n")

		wiki_dump.write("\n==Full List==\n")
		wiki_dump.write(wiki.make_table(table_keys, table_lines))
	ret.append('Upgrades')
	return ret