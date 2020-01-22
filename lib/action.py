# -*- coding: UTF-8 -*-
"""
Original Author: Harrygiel
Contributors: Lamphobic
Purpose: Produce all pages directly related to actions.
"""

import os, json, sys, datetime, re

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


def get_effect_info(effect_json):
	return_txt = ""
	is_treated = False
	for effect_key in effect_json:
		if isinstance(effect_json[effect_key], str):
			return_txt += str(effect_json[effect_key] + '<br/>')
		elif isinstance(effect_json[effect_key], list):
			return_txt += str(', '.join(effect_json[effect_key])) + '<br/>'
		else:
			for effect_name in effect_json[effect_key]:
				if not isinstance(effect_json[effect_key][effect_name], dict):
					return_txt += str(effect_name) + ": " + str(effect_json[effect_key][effect_name]) + "<br/>"
				else:
					for mod_entry in effect_json[effect_key][effect_name]:
						return_txt += str(effect_name) + '.' + str(mod_entry) + ": " + str(effect_json[effect_key][effect_name][mod_entry]) + "<br/>"
	return return_txt[:-5]

	
def action_info(action_json):
#Get every information of a action:
#ID, name, description, cost, length, repeatable, effect, upgrade, require
	action = {}
	action['type'] = 'actions'
	action['id'] = action_json.get('id')
	if action_json.get('name') is not None:
		action['name'] = action_json.get('name').title()
	else:
		action['name'] = action['id'].title()

	action['sym'] = action_json.get('sym')

	action['desc'] = str(action_json.get('desc')).capitalize()

	action['cost'] = {}
	if action_json.get('cost') is not None:
		if isinstance(action_json.get('cost'), int):
			action['cost']['gold'] = action_json.get('cost')
		elif isinstance(action_json.get('cost'), str):
			action['cost']['give'] = action_json.get('cost')
		else:
			action['cost'] = action_json.get('cost')

	action['run'] = {}
	if action_json.get('run') is not None:
		if isinstance(action_json.get('run'), int):
			action['run']['gold'] = action_json.get('run')
		elif isinstance(action_json.get('run'), str):
			action['run']['give'] = action_json.get('run')
		else:
			action['run'] = action_json.get('run')

	if action_json.get('length') is not None:
		action['length'] = action_json.get('length')
	elif action_json.get('perpetual'):
		action['length'] = "Perpetual"
	else:
		action['length'] = "Instant"

	if action_json.get('repeat') is not None:
		action['repeat'] = action_json.get('repeat')
	else:
		action['repeat'] = True
		
	
	action['mod'] = {}
	action['effect'] = {}
	action['result'] = {}
	
	if action_json.get('effect') is not None:
		if action['length'] is "Instant":
			action['result']['effect'] = action_json.get('effect')
		else:
			action['effect']['effect'] = action_json.get('effect')
		action['mod'].update(action_json.get('effect'))
	
	if action_json.get('mod') is not None:
		action['result']['mod'] = action_json.get('mod')
		action['mod'].update(action_json.get('mod'))
	if action_json.get('result') is not None:
		action['result']['result'] = action_json.get('result')
		if isinstance(action_json.get('result'), dict):
			action['mod'].update(action_json.get('result'))
	
	is_done = False
	action['upgrade'] = {}
	if action_json.get('at') is not None:
		is_done = True
		action['upgrade']['at'] = action_json.get('at')
	if action_json.get('every') is not None:
		is_done = True
		action['upgrade']['every'] = action_json.get('every')
	if is_done is False:
		action['upgrade'] = "Doesn't Upgrade"
	
	action['requirements'] = {}
	action['requirements']['>'] = {}
	action['requirements']['<'] = {}
	requirements = action['requirements']
	if action_json.get('require') is not None:
		require = action_json.get('require')
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
	if action_json.get('need') is not None:
		require = action_json.get('need')
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
	
	if action_json.get('require') is not None:
		action['require'] = action_json.get('require')
	else: 
		action['require'] = "Nothing"
	
	if action_json.get('need') is not None:
		action['need'] = action_json.get('need')
	else: 
		action['need'] = "Nothing"
	
	return action


def get_full_action_list():
	result_list = lib.get_json("data/", "actions")
	action_list = list()
	for json_value in result_list:
		action_list.append(action_info(json_value))
	return action_list


def generate_individual_act_page(action_json, id_name_map):
	with open(action_json['name']+".txt", "w", encoding="UTF-8") as page:
		page.write('This page has been automatically updated at ' + str(datetime.datetime.now()) + "<br>\n<br>\n")
		page.write(action_json['name'] + ' is part of [[' + action_json['type'].title() + '|\"' + action_json['type'].title() + '\"]]\n')
		#Desc
		if action_json['desc']:
			page.write('==Description==\n' + action_json['desc'] + '\n')
		#Start Cost
		tmp_cell = ""
		if bool(action_json['cost']) is not False:
			page.write('==Cost to Start==\n')
			if isinstance(action_json['cost'],str):
				tmp_cell += ('*' + str(action_json['cost'])+ '\n')
			elif isinstance(action_json['cost'], int):
				tmp_cell += ("*Gold: " + str(action_json['cost'])+ '\n')
			else:
				for mod_key in action_json['cost']:
					tmp_cell += ('*' + str(mod_key) + ": " + str(action_json['cost'][mod_key]) + '\n')
		page.write(str(tmp_cell))
		
		#Ongoing Cost
		tmp_cell = ""
		if bool(action_json['run']) is not False:
			page.write('==Ongoing Cost==\n')
			if isinstance(action_json['run'],str):
				tmp_cell += ('*' + str(action_json['run'])+ '\n')
			elif isinstance(action_json['run'], int):
				tmp_cell += ("*Gold: " + str(action_json['run'])+ '\n')
			else:
				for mod_key in action_json['run']:
					tmp_cell += ('*' + str(mod_key) + ": " + str(action_json['run'][mod_key]) + '\n')
		page.write(str(tmp_cell))
		
		#Length
		page.write('==Time Length==\n')
		page.write(str(action_json['length']) + '\n')
		
		#Repeatable
		page.write('==Repeatable==\n')
		page.write(str(action_json['repeat']) + '\n')
		
		#Ongoing Effect
		tmp_cell = ""
		if bool(action_json['effect']) is not False:
			page.write('==Ongoing Effect==\n')
			tmp_cell += str(get_effect_info(action_json['effect']))
			tmp_cell = '*' + tmp_cell.replace('<br/>', '\n*') + '\n'
		page.write(str(tmp_cell))
		
		#Result
		tmp_cell = ""
		if bool(action_json['result']) is not False:
			page.write('==Result==\n')
			tmp_cell += str(get_effect_info(action_json['result']))
			tmp_cell = '*' + tmp_cell.replace('<br/>', '\n*') + '\n'
		page.write(tmp_cell)
		
		#Upgrade
		tmp_cell = ""
		if action_json['upgrade'] != 'Doesn\'t Upgrade':
			page.write('==Upgrades==\n')
			if isinstance(action_json['upgrade'],str):
				tmp_cell += (str(action_json['upgrade']))
			else:
				if action_json['upgrade'].get('at') is not None:
					for level_key in action_json['upgrade'].get('at'):
						tmp_cell += ("After " + str(level_key) + " uses:<br/>")
						level_json = action_json['upgrade']['at'].get(level_key)
						for result_key in level_json:
							tmp_cell += "*" + str(result_key) + ": " + str(level_json[result_key]) + "<br/>"
				if action_json['upgrade'].get('every') is not None:
					for level_key in action_json['upgrade'].get('every'):
						tmp_cell += ("Every " + str(level_key) + " uses:<br/>")
						level_json = action_json['upgrade']['every'].get(level_key)
						for result_key in level_json:
							tmp_cell += "*" + str(result_key) + ": " + str(level_json[result_key]) + "<br/>"
			tmp_cell = tmp_cell[:-5].replace('<br/>', '\n') + '\n'
			page.write(str(tmp_cell))
		
		#Unlock Requirements
		if action_json['require'] != "Nothing" and action_json['need'] != "Nothing":
			page.write('==Unlock Requirements==\n')
		if action_json['require'] != "Nothing":
			if isinstance(action_json['require'], str):
				page.write('*' + str(action_json['require'].replace("&&", "\n*").replace("||", "OR")) + '\n')
			else:
				for e in action_json['require']:
					page.write('*' + str(e.replace("&&", "\n*").replace("||", "OR")) + '\n')
		if action_json['need'] != 'Nothing':
			if isinstance(action_json['need'], list):
				for e in action_json['need']:
					page.write('*' + str(e) + '\n')
			else:
				page.write('*' + str(action_json['need']) + '\n')
				
		#Need
		if action_json['need'] != 'Nothing':
			page.write('==Action Requirements==\n')
			if isinstance(action_json['need'], list):
				for e in action_json['need']:
					page.write('*' + str(e) + '\n')
			else:
				page.write('*' + str(action_json['need']) + '\n')
		
		baffected = False
		affected_by = list()
		match_id = action_json['id'].lower()
		
		#Affected By
		for l in lists:
			affected_by = list()
			for e in lists[l]:
				if e['mod']:
					for mod_key in e['mod']:
						match_mod = str(mod_key).lower().split('.')
						if match_id in match_mod:
							if match_id != str(mod_key).lower():
								match_mod = [x if x != match_id else action_json['name'] for x in match_mod]
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
	
def generate_wiki(id_name_map, main_only=False):
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
	
	table_keys = ['Name', 'Description', 'Start Cost', 'Ongoing Cost', 'Length', 'Repeatable', 'Ongoing Effect', 'Result', 'Upgrades', 'Unlock Requirements', 'Action Requirements'] 
	table_lines = []
	school_set = set()
	result_list = lib.get_json("data/", "actions")
	result_list = sorted(result_list, key=lambda srt: srt.get('id').title() if srt.get('name') is None else srt.get('name').title()) #Presorts results by name.
	for json_value in result_list:
		action_json = action_info(json_value)
		table_line = []
		# NAME part
		if action_json.get('sym') is not None:
			table_line.append('| <span id="' + str(action_json['id']) + '">' + action_json['sym'] + '[[' +  str(action_json['name']) + ']]</span>')
		else:
			table_line.append('| <span id="' + str(action_json['id']) + '">[[' +  str(action_json['name']) + ']]</span>')

		# Description part
		table_line.append(str(action_json['desc']))

		#Start Cost
		tmp_cell = ""
		if bool(action_json['cost']) is not False:
			if isinstance(action_json['cost'],str):
				tmp_cell += (str(action_json['cost']))
			elif isinstance(action_json['cost'], int):
				tmp_cell += ("Gold: " + str(action_json['cost']))
			else:
				for mod_key in action_json['cost']:
					tmp_cell += (str(mod_key) + ": " + str(action_json['cost'][mod_key]) + '<br/>')
		table_line.append(str(tmp_cell))

		#Ongoing Cost
		tmp_cell = ""
		if bool(action_json['run']) is not False:
			if isinstance(action_json['run'],str):
				tmp_cell += (str(action_json['run']))
			elif isinstance(action_json['run'], int):
				tmp_cell += ("Gold: " + str(action_json['run']))
			else:
				for mod_key in action_json['run']:
					tmp_cell += (str(mod_key) + ": " + str(action_json['run'][mod_key]) + '<br/>')
		table_line.append(str(tmp_cell))

		# Length part
		table_line.append(str(action_json['length']))

		# Repeatable part
		table_line.append(str(action_json['repeat']))

		# Ongoing Effect part
		tmp_cell = ""
		if bool(action_json['effect']) is not False:
			tmp_cell += str(get_effect_info(action_json['effect']))
		table_line.append(tmp_cell)
		
		# Result part
		tmp_cell = ""
		if bool(action_json['result']) is not False:
			tmp_cell += str(get_effect_info(action_json['result']))
		table_line.append(tmp_cell)

		# Upgrade part 
		tmp_cell = ""
		if isinstance(action_json['upgrade'],str):
			tmp_cell += (str(action_json['upgrade']))
		else:
			if action_json['upgrade'].get('at') is not None:
				for level_key in action_json['upgrade'].get('at'):
					tmp_cell += ("After " + str(level_key) + " uses:<br/>")
					level_json = action_json['upgrade']['at'].get(level_key)
					for result_key in level_json:
						tmp_cell += "-" + str(result_key) + ": " + str(level_json[result_key]) + "<br/>"
			if action_json['upgrade'].get('every') is not None:
				for level_key in action_json['upgrade'].get('every'):
					tmp_cell += ("Every " + str(level_key) + " uses:<br/>")
					level_json = action_json['upgrade']['every'].get(level_key)
					for result_key in level_json:
						tmp_cell += "-" + str(result_key) + ": " + str(level_json[result_key]) + "<br/>"
		table_line.append(str(tmp_cell))

		# Requirement part
		table_line.append(lib.recurs_json_to_str(action_json['require']).replace("&&", "<br/>").replace("||", "<br/>OR<br/>"))

		# Need part
		table_line.append(lib.recurs_json_to_str(action_json['need']).replace("&&", "<br/>").replace("||", "<br/>OR<br/>"))
		
		# Add line to lines
		table_lines.append(table_line)
		
		if not main_only:
			generate_individual_act_page(action_json, id_name_map)
			ret.append(action_json['name'])

	with open("actions.txt", "w", encoding="UTF-8") as wiki_dump:
		wiki_dump.write('This page has been automatically updated the ' + str(datetime.datetime.now()) + "<br/>\n__FORCETOC__\n")

		wiki_dump.write("\n==Instant actions==\n")
		wiki_dump.write(wiki.make_table(table_keys, table_lines, table_filter=[[4, "'Instant' in cell"]]))

		wiki_dump.write("\n==Time consuming actions==\n")
		wiki_dump.write(wiki.make_table(table_keys, table_lines, table_filter=[[4, "'Instant' not in cell"]]))

		wiki_dump.write("\n==One time actions==\n")
		wiki_dump.write(wiki.make_table(table_keys, table_lines, table_filter=[[5, "'False' in cell"]]))

		wiki_dump.write("\n==Full List==\n")
		wiki_dump.write(wiki.make_table(table_keys, table_lines))

	return ret