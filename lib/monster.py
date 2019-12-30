# -*- coding: UTF-8 -*-

import os, json, sys
import lib.extractlib as lib
import lib.dungeon as dungeon



def get_attack_info(attack_json):
	return_text = ""
	if attack_json.get('name') != None:
		return_text += (str(attack_json.get('name')) + ": " + str(attack_json.get('dmg')) + ' ' + str(attack_json.get('kind')) + ' damage')
		if attack_json.get('leech') != None:
			return_text += (" that leech " + str(attack_json.get('leech')) + " life per seconds")
	if attack_json.get('dot') != None:
		dot_json = attack_json.get('dot')
		return_text += (' and apply ' + str(dot_json.get('name')) + ': ' + str(dot_json.get('dmg')) + ' ' + str(dot_json.get('kind')) + ' damage for ' + str(dot_json.get('duration')) + 'seconds')
		if attack_json.get('leech') != None:
			return_text += (" that leech " + str(attack_json.get('leech')) + " life per seconds")
	return_text += (".<br/>")
	return return_text



def get_encounter_info(monster_json, dungeon_encounter, dungeon_json):
	spawn_list = []
	if isinstance(dungeon_encounter, dict):
		#Special spawn rule (ex: catacrypt)
		if dungeon_encounter.get('level') != None:
			range_level = dungeon_encounter.get('level').split("~")
			if int(monster_json['level']) >= int(range_level[0]) and int(monster_json['level']) <= int(range_level[1]):
				spawn_list.append(dungeon_json['name'])
		#Multiple boss
		else:
			for encounter_key in dungeon_encounter:
				if monster_json['id'] == dungeon_encounter[encounter_key]:
					spawn_list.append(dungeon_json['name'])
	else:
		if isinstance(dungeon_encounter[0],str):
			if monster_json['id'] == dungeon_encounter[0]:
				spawn_list.append(dungeon_json['name'])
		else:
			encounter_list = dungeon.parse_encounter(dungeon_encounter)
			if  isinstance(encounter_list[0],str):
				if monster_json['id'] == encounter_list[0]:
					spawn_list.append(dungeon_json['name'])
			else:
				for encounter_item in encounter_list:
					if monster_json['id'] == encounter_item[0]:
						spawn_list.append(dungeon_json['name'])
	return spawn_list



def get_spawn_info(monster_json):
	spawn_list = []
	dungeons_list = dungeon.get_full_dungeon_list()

	for dungeon_json in dungeons_list:
		if dungeon_json.get('encounters') != None:
			result_list = get_encounter_info(monster_json, dungeon_json.get('encounters'), dungeon_json)
			if result_list:
				spawn_list += result_list

		if dungeon_json.get('boss') != None:
			result_list = get_encounter_info(monster_json, dungeon_json.get('boss'), dungeon_json)
			if result_list:
				spawn_list += result_list
	return spawn_list



def monster_info(monster_json):
#Get every information of a monster:
#ID, name, level, HP, Defense bonus, regen, To hit bonus, speed bonus, IsUnique, attack (json or string value), immunity (array), loot modifier (array), spawning area (array)
	monster = {}
	monster['id'] = monster_json.get('id')
	if monster_json.get('name') != None:
		monster['name'] = monster_json.get('name')
	else:
		monster['name'] = monster['id']

	if monster_json.get('sym') != None:
		monster['sym']  = monster_json.get('sym')
		monster['name'] = monster['sym'] + monster['name']

	monster['level']    = monster_json.get('level')
	monster['hp']       = monster_json.get('hp')
	monster['defense']  = monster_json.get('defense')
	monster['regen']    = monster_json.get('regen')
	monster['tohit']    = monster_json.get('tohit')
	monster['speed']    = monster_json.get('speed')

	if monster_json.get('unique') == True:
			monster['unique'] = "Yes"
	else:
		monster['unique'] = "No"

	if monster_json.get('attack') != None:
		monster['attack'] = monster_json.get('attack')
	#if flat damage
	elif monster_json.get('damage') != None:
		if monster_json.get('damage') == 0:
			monster['attack'] = "None"
		else:
			monster['attack'] = "flat: " + monster_json.get('damage')
	else:
		monster['attack'] = "None"

	if monster_json.get('immune') != None:
		monster['immunity'] = monster_json.get('immune').split(',')
	else:
		monster['immunity'] = "None"

	monster['loot'] = []
	if monster_json.get('loot') != None:
		loot_json = monster_json.get('loot')
		if isinstance(loot_json,str):
			monster['loot'].append(loot_json)
		else:
			if isinstance(loot_json,dict):
				for loot_key in loot_json:
					if loot_key == "max":
						monster['loot'].append("max item level: " + str(loot_json[loot_key]))
					elif isinstance(loot_json[loot_key],dict):

						monster['loot'].append("special loot: " + loot_key.get("name"))
					else:
						monster['loot'].append(str(loot_key) + ": " + str(loot_json[loot_key]))
			elif isinstance(loot_json,list):
				for loot_object in loot_json:
					if isinstance(loot_object,dict):
						monster['loot'].append("special loot: " + loot_object.get("pct") + " chance of getting " + loot_object.get("name"))
					else:
						monster['loot'].append(str(loot_object))
			else:
				print("ERROR")
				print(loot_json)
	else:
		monster['loot'].append("None")

	return monster



def get_full_monster_list():
	result_list = lib.get_json("data/", "monsters")
	monster_list
	for json_value in result_list:
		monster_list.append(monster_info(json_value))
	return monster_list



def monster_wiki():
	result_list = lib.get_json("data/", "monsters")
	with open("monsters.txt", "w", encoding="UTF-8") as wiki_dump:
		wiki_dump.write('{| class="wikitable sortable"\n')
		wiki_dump.write('|-\n')
		wiki_dump.write('! Name !! data-sort-type="number"|Level !! data-sort-type="number"|HP !! data-sort-type="number"|Defense bonus !! data-sort-type="number"|Regen !! data-sort-type="number"|To hit bonus ')
		wiki_dump.write('!! data-sort-type="number"|Speed bonus !! Unique !! Attack !! Immunity !! Loot modifier !! Spawning area\n')

		for json_value in result_list:
			monster_json = monster_info(json_value)
			wiki_dump.write('|-\n')
			# NAME part
			wiki_dump.write('| <span id="' + str(monster_json['id']) + '">' +  str(monster_json['name']) + '</span> ||')

			wiki_dump.write(str(monster_json['level']) + ' || ')
			wiki_dump.write(str(monster_json['hp']) + ' || ')
			wiki_dump.write(str(monster_json['defense']) + ' || ')
			wiki_dump.write(str(monster_json['regen']) + ' || ')
			wiki_dump.write(str(monster_json['tohit']) + ' || ')
			wiki_dump.write(str(monster_json['speed']) + ' || ')
			wiki_dump.write(str(monster_json['unique']) + ' || ')

			#DAMAGE part
			if isinstance(monster_json['attack'], str):
				wiki_dump.write(str(monster_json['attack']))
			else:
				#if more than 1 attack
				if isinstance(monster_json['attack'], list):
					for attack_json in monster_json['attack']:
						wiki_dump.write(get_attack_info(attack_json))
						wiki_dump.write('<br/>')
				#if 1 attack
				elif isinstance(monster_json['attack'], dict):
					wiki_dump.write(get_attack_info(monster_json['attack']))
			wiki_dump.write('|| ')

			#IMMUNE part
			if isinstance(monster_json['immunity'],str):
				wiki_dump.write(monster_json['immunity'])
			else:
				for immunity_name in monster_json['immunity']:
					wiki_dump.write(str(immunity_name) + '<br/>')
			wiki_dump.write(' || ')
			
			
			#LOOT part
			for loot_name in monster_json['loot']:
				wiki_dump.write(str(loot_name) + '<br/>')
			wiki_dump.write(' || ')

			#SPAWNING AREA part
			spawn_list = get_spawn_info(monster_json)
			for spawn_name in spawn_list:
				wiki_dump.write(str(spawn_name) + '<br/>')

			wiki_dump.write('\n')
		wiki_dump.write('|}')
