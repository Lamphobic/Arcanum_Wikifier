# -*- coding: utf-8 -*-
"""
Original Author: Harrygiel
Contributors: Lamphobic
Purpose: Produce all pages directly related to actions.
"""

import os, json, datetime, re
import lib.extractlib as lib



def wiki_dump_encounter(file, encounters):
	if isinstance(encounters, str):
		file.write("None")
	elif isinstance(encounters[0], str):
		file.write(str(encounters[1])  + " x " + str(encounters[0]) + "  ")
	else:
		for encounter in encounters:
			if isinstance(encounter[0], list):
				for monsters in encounter:
					file.write(str(monsters[1]) + " x " + str(monsters[0]) + "  ")
			else:
				file.write(str(encounter[1]) + " x " + str(encounter[0]) + "  ")
			file.write("<br/>")



def parse_encounter(encounter_list):
	if isinstance(encounter_list, dict):
		#Special spawn
		return encounter_list
	else:
		if isinstance(encounter_list,str):
			return [encounter_list, 1]
		else:
			tmp = []
			for encounter_array in encounter_list:
				if  isinstance(encounter_array,str):
					tmp.append([encounter_array, 1])
				else:
					for monster in encounter_array:
						if [monster,lib.ANYTHING] in tmp:
							tmp[tmp.index([monster,lib.ANYTHING])][1] += 1
						else:
							tmp.append([monster, 1])
			return tmp

'''
		"enemies":{
			"level":"8~25",
			"scale":true,
			"range":2

'''

def dungeon_info(dungeon_json):
#Get every information of a dungeon:
#ID, name, level, length, requirement, consumption, reward, encounters, boss
	dungeon = {}
	dungeon['type'] = 'dungeon'
	dungeon['id'] = dungeon_json.get('id')

	if dungeon_json.get('name') is not None:
		dungeon['name'] = dungeon_json.get('name').title()
	else:
		dungeon['name'] = dungeon['id'].title()

	if dungeon_json.get('sym') is not None:
		dungeon['sym']  = dungeon_json.get('sym')
		dungeon['name'] = dungeon['sym'] + dungeon['name']

	dungeon['level']  = dungeon_json.get('level')
	dungeon['length'] = dungeon_json.get('length')
	dungeon['require'] = dungeon_json.get('require') #### TO CHANGE
	
	dungeon['requirements'] = {}
	dungeon['requirements']['>'] = {}
	dungeon['requirements']['<'] = {}
	requirements = dungeon['requirements']
	if dungeon_json.get('require') is not None:
		require = dungeon_json.get('require')
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
	
	dungeon['mod'] = {}

	if dungeon_json.get('run') is not None:
		dungeon['consume'] = dungeon_json.get('run')
	else: 
		dungeon['consume'] = "Nothing"

	if dungeon_json.get('result') is not None:
		dungeon['mod'] = dungeon_json.get('result')
		dungeon['reward'] = dungeon_json.get('result')
	else: 
		dungeon['reward'] = "Nothing"

	if dungeon_json.get('enemies') is not None:
		dungeon['encounters'] = parse_encounter(dungeon_json.get('enemies'))
	else:
		dungeon['encounters'] = "None"

	if dungeon_json.get('boss') is not None:
		dungeon['boss'] = parse_encounter(dungeon_json.get('boss'))
	else:
		dungeon['boss'] = "None"

	return dungeon



def get_full_dungeon_list():
	result_list = lib.get_json("data/", "dungeons")
	dungeon_list = []
	for json_value in result_list:
		dungeon_list.append(dungeon_info(json_value))
	return dungeon_list


def generate_wiki():
	result_list = lib.get_json("data/", "dungeons")
	path_to_json = "data/"
	target_name = "dungeons"

	with open("dungeons.txt", "w", encoding="UTF-8") as wiki_dump:
		wiki_dump.write('This page has been automatically updated the ' + str(datetime.datetime.now()) + "\n")
		wiki_dump.write('{| class="wikitable sortable"\n')
		wiki_dump.write('|-\n')
		wiki_dump.write('! Name !! data-sort-type="number"|Level !! data-sort-type="number"|Length !! Requirement !! Consumption !! Reward !! Encounters !! Boss\n')

		for json_value in result_list:
			dungeon_json = dungeon_info(json_value)

			wiki_dump.write('|-\n')
			# NAME part
			wiki_dump.write('| <span id="' + str(dungeon_json['id']) + '">' +  str(dungeon_json['name']) + '</span> ||')

			wiki_dump.write(str(dungeon_json['level']) + ' || ')
			wiki_dump.write(str(dungeon_json['length']) + ' || ')
			wiki_dump.write(str(dungeon_json['require']) + ' || ')

			if isinstance(dungeon_json['consume'], str):
				wiki_dump.write(str(dungeon_json['consume']))
			else:
				for json_key in dungeon_json['consume']:
					wiki_dump.write(str(json_key) + ": " + str(dungeon_json['consume'][json_key]) + "<br/>")
			wiki_dump.write(' || ')

			if isinstance(dungeon_json['reward'], str):
				wiki_dump.write(str(dungeon_json['reward']))
			else:
				for json_key in dungeon_json['reward']:
					wiki_dump.write(str(json_key) + ": " + str(dungeon_json['reward'][json_key]) + "<br/>")
			wiki_dump.write(' || ')

			if isinstance(dungeon_json['encounters'], dict):
				for encounter_key in dungeon_json['encounters']:
					wiki_dump.write(str(encounter_key) + ": " + str(dungeon_json['encounters'][encounter_key]) + "<br/>")
			else:
				wiki_dump_encounter(wiki_dump, dungeon_json['encounters'])
			wiki_dump.write(' || ')

			if isinstance(dungeon_json['boss'], dict):
				for encounter_key in dungeon_json['boss']:
					wiki_dump.write(str(encounter_key) + ": " + str(dungeon_json['boss'][encounter_key]) + "<br/>")
			else:
				wiki_dump_encounter(wiki_dump, dungeon_json['boss'])

			wiki_dump.write('\n')
		wiki_dump.write('|}')

		return "dungeons.txt"