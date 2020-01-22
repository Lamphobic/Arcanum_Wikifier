# -*- coding: UTF-8 -*-
"""
Original Author: Harrygiel
Contributors: Lamphobic
Purpose: Produce all pages directly related to skills.
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

def skill_info(skill_json):
#Get every information of a skill:
#ID, name, description, tags, cost, consumption, bonus, reward, requirement, need, level scaling
	skill = {}
	skill['type'] = 'skills'
	skill['id'] = skill_json.get('id')
	if skill_json.get('name') is not None:
		skill['name'] = skill_json.get('name').title()
	else:
		skill['name'] = skill['id'].title()

	skill['sym'] = skill_json.get('sym')

	skill['desc'] = str(skill_json.get('desc')).capitalize()

	if skill_json.get('tags') is not None:
		skill['tags'] = skill_json.get('tags').split(",")
	else:
		skill['tags'] = []

	if skill_json.get('buy') is not None:
		skill['cost']  = skill_json.get('buy')
		if skill_json.get('buy').get('sp') is None:
			skill['cost']['sp'] = 1
	else:
		skill['cost'] = {}
		skill['cost']['sp'] = 1

	if skill_json.get('run') is not None:
		skill['consumption']  = skill_json.get('run')
	else:
		skill['consumption']  = {}
	
	skill['mod'] = {}
	if skill_json.get('mod') is not None:
		skill['bonus'] = skill_json.get('mod')
		is_dict = True
		while is_dict:
			is_dict = False
			newDict = {}
			for e in skill['bonus']:
				if not isinstance(skill['bonus'][e], dict):
					tmp = skill['bonus'][e]
					newDict[e] = tmp
				else:
					is_dict = True
					for en in skill['bonus'][e]:
						newDict[e + '.' + en] = skill['bonus'][e][en]
			skill['bonus'] = dict(newDict)
		skill['mod'].update(skill['bonus'])
	else:
		skill['bonus'] = {}

	if skill_json.get('result') is not None:
		skill['reward'] = skill_json.get('result')
		skill['mod'].update(skill_json.get('result'))
	else:
		skill['reward'] = {}

	if skill_json.get('need') is not None:
		skill['need'] = skill_json.get('need')
	else:
		skill['need'] = {}

	if skill_json.get('level') is not None:
		skill['level_scaling'] = skill_json.get('level')
	else:
		skill['level_scaling'] = "1"

	if skill_json.get('require') is not None:
		skill['require'] = skill_json.get('require')
	else: 
		skill['require'] = "Nothing"
		
	
	
	skill['requirements'] = {}
	skill['requirements']['>'] = {}
	skill['requirements']['<'] = {}
	requirements = skill['requirements']
	if skill_json.get('require') is not None:
		require = skill_json.get('require')
		if isinstance(require, list):
			for e in require:
				if not isinstance(e, dict):
					requirements['>'][e] = 1
				else:
					for ent in e:
						requirements['>'][ent] = e[ent]
		elif isinstance(require, dict):
			for e in require:
				requirements['>'][e] = require[e]
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
	if skill_json.get('need') is not None:
		require = skill_json.get('need')
		if isinstance(require, list):
			for e in require:
				if not isinstance(e, dict):
					requirements['>'][e] = 1
				else:
					for ent in e:
						requirements['>'][ent] = e[ent]
		elif isinstance(require, dict):
			for e in require:
				requirements['>'][e] = require[e]
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

	return skill



def get_full_skill_list():
	result_list = lib.get_json("data/", "skills")
	skill_list = list()
	for json_value in result_list:
		skill_list.append(skill_info(json_value))
	return skill_list


def generate_individual_skl_page(skl):
	with open(skl['name']+".txt", "w", encoding="UTF-8") as skl_page:
		skl_page.write('This page has been automatically updated at ' + str(datetime.datetime.now()) + "<br>\n<br>\n")
		skl_page.write(skl['name'] + ' is part of [[' + skl['type'].title() + '|\"' + skl['type'].title() + '\"]]\n')
		if skl['desc']:
			skl_page.write('==Description==\n' + skl['desc'] + '\n')
		if skl['tags']:
			skl_page.write('==Tags==\n' + ' '.join(skl['tags']) + '\n')
		if skl['cost']:
			skl_page.write('==Purchase Cost==\n')
			for entry_key in skl['cost']:
				skl_page.write('*' + entry_key + ': ' + str(skl['cost'][entry_key]) + '\n')
		if skl['consumption']:
			skl_page.write('==Training Cost==\n')
			for entry_key in skl['consumption']:
				skl_page.write('*' + entry_key + ': ' + str(skl['consumption'][entry_key]) + '\n')
		if skl['bonus']:
			skl_page.write('==Rank Bonuses==\n')
			for entry_key in skl['bonus']:
				skl_page.write('*' + entry_key + ': ' + str(skl['bonus'][entry_key]) + '\n')
		if skl['reward']:
			skl_page.write('==Rewards==\n')
			for entry_key in skl['reward']:
				skl_page.write('*' + entry_key + ': ' + str(skl['reward'][entry_key]) + '\n')
		if skl['require'] != "Nothing" and not skl['need']:
			skl_page.write('==Unlock Requirements==\n')
		if skl['require'] != "Nothing":
			skl_page.write('*' + str(skl['require'].replace("&&", "\n*").replace("||", "OR")) + '\n')
		if skl['need']:
			if isinstance(skl['need'], list):
				for e in skl['need']:
					skl_page.write(str(e) + '\n')
			else:
				skl_page.write(str(skl['need']) + '\n')
		if skl['need']:
			skl_page.write('==Training Requirements==\n')
			if isinstance(skl['need'], list):
				for e in skl['need']:
					skl_page.write(str(e) + '\n')
			else:
				skl_page.write(str(skl['need']) + '\n')
		skl_page.write('==Level Scaling==\n' + str(skl['level_scaling']) + '\n')
		
		baffected = False
		bsource = False
		bunlock = False
		affected_by = list()
		sources = list()
		unlock = {}
		match_id = skl['id'].lower()
		
		#Build Unlocks
		for l in lists:
			unlock = {}
			for e in lists[l]:
				if 'requirements' in e:
					if e['requirements']['<'] or e['requirements']['>']:
						for req_key in e['requirements']['<']:
							match_req = str(req_key).lower()
							if match_id in match_req.split('.'):
								unlock[str(e['requirements']['<'][match_req]) + ' or less ' + '.'.join([x if x != match_id else skl['name'] for x in match_req.split('.')]) + ': [[' + e['type'].title() + '#' + e['id'] + '|' + e['name'] + ']]'] = e['requirements']['<'][match_req]
						for req_key in e['requirements']['>']:
							match_req = str(req_key)
							if match_id in match_req.split('.'):
								unlock[str(e['requirements']['>'][match_req]) + ' or more ' + '.'.join([x if x != match_id else skl['name'] for x in match_req.split('.')]) + ': [[' + e['type'].title() + '#' + e['id'] + '|' + e['name'] + ']]'] = e['requirements']['>'][match_req]
			sorted_l = sorted(unlock, key=unlock.get)
			if unlock:
				if not bunlock:
					skl_page.write('==Unlocks==\n')
					bunlock = True
				skl_page.write(('===' + l + '===\n').title())
				for e in sorted_l:
					skl_page.write('* ' + e + '\n')
		
		#Build Affected By
		for l in lists:
			affected_by = list()
			for e in lists[l]:
				if e['mod']:
					for mod_key in e['mod']:
						match_mod = str(mod_key).lower().split('.')
						if match_id in match_mod:
							if match_id != str(mod_key).lower():
								match_mod = [x if x != match_id else skl['name'] for x in match_mod]
								affected_by.append('[[' + e['type'].title() + '#' + e['id'] + '|' + e['name'] + ']]: ' + '.'.join(match_mod) + ": " + str(e['mod'][mod_key]))
			affected_by = list(set(affected_by))
			affected_by.sort()
			if affected_by:
				if not baffected:
					skl_page.write('==Affected By==\n')
					baffected = True
				skl_page.write(('===' + l + '===\n').title())
				for e in affected_by:
					skl_page.write('* ' + e + '\n')
		
		#Build Alternative Training Sources
		for l in lists: #for each list of entries
			sources = list()
			for e in lists[l]: #for each entry in this list
				if e['mod']: #if this entry has any mods
					for mod_key in e['mod']: #for each mod in the mods of this entry
						match_mod = str(mod_key).lower().split('.')
						if match_id in str(mod_key): #if this mod references this resource by id
							if match_id + '.exp' == str(mod_key).lower():
								sources.append('[[' + e['type'].title() + '#' + e['id'] + '|' + e['name'] + ']]: ' + skl['name'] + ": " + str(e['mod'][mod_key]))
			sources = list(set(sources))
			sources.sort()
			if sources:
				if not bsource:
					skl_page.write('==Alternative Training Sources==\n')
					bsource = True
				skl_page.write(('===' + l + '===\n').title())
				for e in sources:
					skl_page.write('* ' + e + '\n')
		

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
	
	table_keys = ['Name', 'Description', 'tags', 'Purchase Cost', 'Training Cost', 'Rank Bonus', 'Reward', 'Unlock Requirements', 'Training Requirements', 'Level Scaling'] 
	table_lines = []
	result_list = lib.get_json("data/", "skills")
	result_list = sorted(result_list, key=lambda srt: srt.get('id').title() if srt.get('name') is None else srt.get('name').title()) #Presorts results by name.
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
		for cost_key in sorted(skill_json['cost'].keys()):
			tmp_cell += (str(cost_key) + ": " + str(skill_json['cost'][cost_key]) + '<br/>')
		table_line.append(str(tmp_cell))

		# consumption part
		tmp_cell = ""
		for train_cost_key in skill_json['consumption']:
			tmp_cell += (str(train_cost_key) + ": " + str(skill_json['consumption'][train_cost_key]) + '<br/>')
		table_line.append(str(tmp_cell))

		# bonus part
		tmp_cell = ""
		for rank_bonus_key in skill_json['bonus']:
			tmp_cell += (str(rank_bonus_key) + ": " + str(skill_json['bonus'][rank_bonus_key]) + '<br/>')
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
			ret.append(skill_json['name'])

	with open("skills.txt", "w", encoding="UTF-8") as wiki_dump:
		wiki_dump.write('This page has been automatically updated the ' + str(datetime.datetime.now()) + "\n")
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

		return ret