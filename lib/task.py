# -*- coding: UTF-8 -*-
"""
Original Author: Harrygiel
Contributors: Lamphobic
Purpose: Produce all pages directly related to tasks.
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

	
def task_info(task_json):
#Get every information of a task:
#ID, name, description, cost, length, repeatable, effect, upgrade, require
	task = {}
	task['type'] = 'tasks'
	task['id'] = task_json.get('id')
	if task_json.get('name') is not None:
		task['name'] = task_json.get('name').title()
	else:
		task['name'] = task['id'].title()

	task['sym'] = task_json.get('sym')

	task['desc'] = str(task_json.get('desc')).capitalize()

	task['cost'] = {}
	if task_json.get('cost') is not None:
		if isinstance(task_json.get('cost'), int):
			task['cost']['gold'] = task_json.get('cost')
		elif isinstance(task_json.get('cost'), str):
			task['cost']['give'] = task_json.get('cost')
		else:
			task['cost'] = task_json.get('cost')

	task['run'] = {}
	if task_json.get('run') is not None:
		if isinstance(task_json.get('run'), int):
			task['run']['gold'] = task_json.get('run')
		elif isinstance(task_json.get('run'), str):
			task['run']['give'] = task_json.get('run')
		else:
			task['run'] = task_json.get('run')

	if task_json.get('length') is not None:
		task['length'] = task_json.get('length')
	elif task_json.get('perpetual'):
		task['length'] = "Perpetual"
	else:
		task['length'] = "Instant"

	if task_json.get('repeat') is not None:
		task['repeat'] = task_json.get('repeat')
	else:
		task['repeat'] = True
		
	
	task['mod'] = {}
	task['effect'] = {}
	task['result'] = {}
	
	if task_json.get('effect') is not None:
		if task['length'] is "Instant":
			task['result']['effect'] = task_json.get('effect')
		else:
			task['effect']['effect'] = task_json.get('effect')
		task['mod'].update(task_json.get('effect'))
	
	if task_json.get('mod') is not None:
		task['result']['mod'] = task_json.get('mod')
		task['mod'].update(task_json.get('mod'))
	if task_json.get('result') is not None:
		task['result']['result'] = task_json.get('result')
		if isinstance(task_json.get('result'), dict):
			task['mod'].update(task_json.get('result'))
	
	is_done = False
	task['upgrade'] = {}
	if task_json.get('at') is not None:
		is_done = True
		task['upgrade']['at'] = task_json.get('at')
	if task_json.get('every') is not None:
		is_done = True
		task['upgrade']['every'] = task_json.get('every')
	if is_done is False:
		task['upgrade'] = "Doesn't Upgrade"
	
	task['requirements'] = {}
	task['requirements']['>'] = {}
	task['requirements']['<'] = {}
	requirements = task['requirements']
	if task_json.get('require') is not None:
		require = task_json.get('require')
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
	if task_json.get('need') is not None:
		require = task_json.get('need')
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
	
	if task_json.get('require') is not None:
		task['require'] = task_json.get('require')
	else: 
		task['require'] = "Nothing"
	
	if task_json.get('need') is not None:
		task['need'] = task_json.get('need')
	else: 
		task['need'] = "Nothing"
		
	lib.name_exceptions(task)
	
	return task


def get_full_task_list():
	result_list = lib.get_json("data/", "tasks")
	task_list = list()
	for json_value in result_list:
		task_list.append(task_info(json_value))
	return task_list


def generate_individual_act_page(task_json, id_name_map):
	name = res['name'] + ".txt"
	exist = False
	if diff_only and os.path.exists(name):
		name = 'test' + name
		exist = True
	with open(name, "w", encoding="UTF-8") as page:
		page.write('This page has been automatically updated at ' + str(datetime.datetime.now()) + "<br>\n<br>\n")
		page.write(task_json['name'] + ' is part of [[' + task_json['type'].title() + '|\"' + task_json['type'].title() + '\"]]\n')
		#Desc
		if task_json['desc']:
			page.write('==Description==\n' + task_json['desc'] + '\n')
		#Start Cost
		tmp_cell = ""
		if bool(task_json['cost']) is not False:
			page.write('==Cost to Start==\n')
			if isinstance(task_json['cost'],str):
				tmp_cell += ('*' + str(task_json['cost'])+ '\n')
			elif isinstance(task_json['cost'], int):
				tmp_cell += ("*Gold: " + str(task_json['cost'])+ '\n')
			else:
				for mod_key in task_json['cost']:
					tmp_cell += ('*' + str(mod_key) + ": " + str(task_json['cost'][mod_key]) + '\n')
		page.write(str(tmp_cell))
		
		#Ongoing Cost
		tmp_cell = ""
		if bool(task_json['run']) is not False:
			page.write('==Ongoing Cost==\n')
			if isinstance(task_json['run'],str):
				tmp_cell += ('*' + str(task_json['run'])+ '\n')
			elif isinstance(task_json['run'], int):
				tmp_cell += ("*Gold: " + str(task_json['run'])+ '\n')
			else:
				for mod_key in task_json['run']:
					tmp_cell += ('*' + str(mod_key) + ": " + str(task_json['run'][mod_key]) + '\n')
		page.write(str(tmp_cell))
		
		#Length
		page.write('==Time Length==\n')
		page.write(str(task_json['length']) + '\n')
		
		#Repeatable
		page.write('==Repeatable==\n')
		page.write(str(task_json['repeat']) + '\n')
		
		#Ongoing Effect
		tmp_cell = ""
		if bool(task_json['effect']) is not False:
			page.write('==Ongoing Effect==\n')
			tmp_cell += str(get_effect_info(task_json['effect']))
			tmp_cell = '*' + tmp_cell.replace('<br/>', '\n*') + '\n'
		page.write(str(tmp_cell))
		
		#Result
		tmp_cell = ""
		if bool(task_json['result']) is not False:
			page.write('==Result==\n')
			tmp_cell += str(get_effect_info(task_json['result']))
			tmp_cell = '*' + tmp_cell.replace('<br/>', '\n*') + '\n'
		page.write(tmp_cell)
		
		#Upgrade
		tmp_cell = ""
		if task_json['upgrade'] != 'Doesn\'t Upgrade':
			page.write('==Upgrades==\n')
			if isinstance(task_json['upgrade'],str):
				tmp_cell += (str(task_json['upgrade']))
			else:
				if task_json['upgrade'].get('at') is not None:
					for level_key in task_json['upgrade'].get('at'):
						tmp_cell += ("After " + str(level_key) + " uses:<br/>")
						level_json = task_json['upgrade']['at'].get(level_key)
						for result_key in level_json:
							tmp_cell += "*" + str(result_key) + ": " + str(level_json[result_key]) + "<br/>"
				if task_json['upgrade'].get('every') is not None:
					for level_key in task_json['upgrade'].get('every'):
						tmp_cell += ("Every " + str(level_key) + " uses:<br/>")
						level_json = task_json['upgrade']['every'].get(level_key)
						for result_key in level_json:
							tmp_cell += "*" + str(result_key) + ": " + str(level_json[result_key]) + "<br/>"
			tmp_cell = tmp_cell[:-5].replace('<br/>', '\n') + '\n'
			page.write(str(tmp_cell))
		
		#Unlock Requirements
		if task_json['require'] != "Nothing" and task_json['need'] != "Nothing":
			page.write('==Unlock Requirements==\n')
		if task_json['require'] != "Nothing":
			if isinstance(task_json['require'], str):
				page.write('*' + str(task_json['require'].replace("&&", "\n*").replace("||", "OR")) + '\n')
			else:
				for e in task_json['require']:
					page.write('*' + str(e.replace("&&", "\n*").replace("||", "OR")) + '\n')
		if task_json['need'] != 'Nothing':
			if isinstance(task_json['need'], list):
				for e in task_json['need']:
					page.write('*' + str(e) + '\n')
			else:
				page.write('*' + str(task_json['need']) + '\n')
				
		#Need
		if task_json['need'] != 'Nothing':
			page.write('==task Requirements==\n')
			if isinstance(task_json['need'], list):
				for e in task_json['need']:
					page.write('*' + str(e) + '\n')
			else:
				page.write('*' + str(task_json['need']) + '\n')
		
		baffected = False
		affected_by = list()
		match_id = task_json['id'].lower()
		
		#Affected By
		for l in lists:
			affected_by = list()
			for e in lists[l]:
				if e['mod']:
					for mod_key in e['mod']:
						match_mod = str(mod_key).lower().split('.')
						if match_id in match_mod:
							if match_id != str(mod_key).lower():
								match_mod = [x if x != match_id else task_json['name'] for x in match_mod]
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
	
	table_keys = ['Name', 'Description', 'Start Cost', 'Ongoing Cost', 'Length', 'Repeatable', 'Ongoing Effect', 'Result', 'Upgrades', 'Unlock Requirements', 'task Requirements'] 
	table_lines = []
	result_list = lib.get_json("data/", "tasks")
	result_list = sorted(result_list, key=lambda srt: srt.get('id').title() if srt.get('name') is None else srt.get('name').title()) #Presorts results by name.
	for json_value in result_list:
		task_json = task_info(json_value)
		table_line = []
		# NAME part
		if task_json.get('sym') is not None:
			table_line.append('| <span id="' + str(task_json['id']) + '">' + task_json['sym'] + '[[' +  str(task_json['name']) + ']]</span>')
		else:
			table_line.append('| <span id="' + str(task_json['id']) + '">[[' +  str(task_json['name']) + ']]</span>')

		# Description part
		table_line.append(str(task_json['desc']))

		#Start Cost
		tmp_cell = ""
		if bool(task_json['cost']) is not False:
			if isinstance(task_json['cost'],str):
				tmp_cell += (str(task_json['cost']))
			elif isinstance(task_json['cost'], int):
				tmp_cell += ("Gold: " + str(task_json['cost']))
			else:
				for mod_key in task_json['cost']:
					tmp_cell += (str(mod_key) + ": " + str(task_json['cost'][mod_key]) + '<br/>')
		table_line.append(str(tmp_cell))

		#Ongoing Cost
		tmp_cell = ""
		if bool(task_json['run']) is not False:
			if isinstance(task_json['run'],str):
				tmp_cell += (str(task_json['run']))
			elif isinstance(task_json['run'], int):
				tmp_cell += ("Gold: " + str(task_json['run']))
			else:
				for mod_key in task_json['run']:
					tmp_cell += (str(mod_key) + ": " + str(task_json['run'][mod_key]) + '<br/>')
		table_line.append(str(tmp_cell))

		# Length part
		table_line.append(str(task_json['length']))

		# Repeatable part
		table_line.append(str(task_json['repeat']))

		# Ongoing Effect part
		tmp_cell = ""
		if bool(task_json['effect']) is not False:
			tmp_cell += str(get_effect_info(task_json['effect']))
		table_line.append(tmp_cell)
		
		# Result part
		tmp_cell = ""
		if bool(task_json['result']) is not False:
			tmp_cell += str(get_effect_info(task_json['result']))
		table_line.append(tmp_cell)

		# Upgrade part 
		tmp_cell = ""
		if isinstance(task_json['upgrade'],str):
			tmp_cell += (str(task_json['upgrade']))
		else:
			if task_json['upgrade'].get('at') is not None:
				for level_key in task_json['upgrade'].get('at'):
					tmp_cell += ("After " + str(level_key) + " uses:<br/>")
					level_json = task_json['upgrade']['at'].get(level_key)
					for result_key in level_json:
						tmp_cell += "-" + str(result_key) + ": " + str(level_json[result_key]) + "<br/>"
			if task_json['upgrade'].get('every') is not None:
				for level_key in task_json['upgrade'].get('every'):
					tmp_cell += ("Every " + str(level_key) + " uses:<br/>")
					level_json = task_json['upgrade']['every'].get(level_key)
					for result_key in level_json:
						tmp_cell += "-" + str(result_key) + ": " + str(level_json[result_key]) + "<br/>"
		table_line.append(str(tmp_cell))

		# Requirement part
		table_line.append(lib.recurs_json_to_str(task_json['require']).replace("&&", "<br/>").replace("||", "<br/>OR<br/>"))

		# Need part
		table_line.append(lib.recurs_json_to_str(task_json['need']).replace("&&", "<br/>").replace("||", "<br/>OR<br/>"))
		
		# Add line to lines
		table_lines.append(table_line)
		
		if not main_only:
			if generate_individual_res_page(resource_json, diff_only):
				ret.append(resource_json['name'])

	with open("tasks.txt", "w", encoding="UTF-8") as wiki_dump:
		wiki_dump.write('This page has been automatically updated the ' + str(datetime.datetime.now()) + "<br/>\n__FORCETOC__\n")

		wiki_dump.write("\n==Instant tasks==\n")
		wiki_dump.write(wiki.make_table(table_keys, table_lines, table_filter=[[4, "'Instant' in cell"]]))

		wiki_dump.write("\n==Time consuming tasks==\n")
		wiki_dump.write(wiki.make_table(table_keys, table_lines, table_filter=[[4, "'Instant' not in cell"]]))

		wiki_dump.write("\n==One time tasks==\n")
		wiki_dump.write(wiki.make_table(table_keys, table_lines, table_filter=[[5, "'False' in cell"]]))

		wiki_dump.write("\n==Full List==\n")
		wiki_dump.write(wiki.make_table(table_keys, table_lines))

	return ret