# -*- coding: UTF-8 -*-
"""
Original Author: Harrygiel
Contributors: Lamphobic
Purpose: Produce all pages directly related to resources.
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

def resource_info(resource_json):
#Get every information of a resource:
#ID, name, description, tags, base maximum, hidden, bonus

	resource = {}
	resource['id'] = resource_json.get('id')
	if resource_json.get('name') is not None:
		resource['name'] = resource_json.get('name').title()
	else:
		resource['name'] = resource['id'].title()

	resource['sym'] = resource_json.get('sym')

	resource['desc'] = resource_json.get('desc')

	if resource_json.get('tags') is not None:
		resource['tags'] = resource_json.get('tags').split(",")
	else:
		resource['tags'] = []

	resource['base_max'] = resource_json.get('max')

	if resource_json.get('hide') is True:
			resource['hidden'] = "Yes"
	else:
		resource['hidden'] = "No"

	if resource_json.get('mod') is not None:
		resource['mod'] = resource_json.get('mod')
	else:
		resource['mod'] = {}

	return resource


def get_full_resource_list():
	result_list = lib.get_json("data/", "resources")
	resource_list = list()
	for json_value in result_list:
		resource_list.append(resource_info(json_value))
	return resource_list


def generate_individual_res_page(res):
	with open(res['name']+".txt", "w", encoding="UTF-8") as res_page:
		res_page.write('This page has been automatically updated at ' + str(datetime.datetime.now()) + "\n")
		if res['desc'] is not None:
			res_page.write('===Description===\n' + res['desc'] + '\n')
		if res['tags']:
			res_page.write('===Tags===\n' + ' '.join(res['tags']) + '\n')
		res_page.write('===Base Max===\n' + str(res['base_max']) + '\n')
		res_page.write('===Is Hidden===\n' + res['hidden'] + '\n')
		if res['mod']:
			res_page.write('===Affects===\n')
			for mod_key in res['mod']:
				res_page.write('*' + str(mod_key) + ": " + str(res['mod'][mod_key]) + '\n')
		affected_by = list()
		for l in lists: #for each list of entries
			for e in l: #for each entry in this list
				if e['mod']: #if this entry has any mods
					for mod_key in e['mod']: #for each mod in the mods of this entry
						if res['name'].lower() in str(mod_key).lower().split('.'): #if this mod references this resource
							affected_by.append('[[' + e['name'] + ']]: ' + str(mod_key) + ": " + str(e['mod'][mod_key]))
						elif res['id'].lower() in str(mod_key).lower().split('.'):
							affected_by.append('[[' + e['name'] + ']]: ' + str(mod_key) + ": " + str(e['mod'][mod_key]))
		affected_by.sort()
		if affected_by:
			res_page.write('===Affected By===\n')
			for e in affected_by:
				res_page.write('* ' + e + '\n')


def generate_wiki():
	global lists
	lists = [
		action.get_full_action_list(),
		dungeon.get_full_dungeon_list(),
		furniture.get_full_furniture_list(),
		home.get_full_home_list(),
		monster.get_full_monster_list(),
		potion.get_full_potion_list(),
		resource.get_full_resource_list(),
		skill.get_full_skill_list(),
		spell.get_full_spell_list(),
		tom_class.get_full_tom_class_list(),
		upgrade.get_full_upgrade_list()
		]
	ret = list()
	result_list = lib.get_json("data/", "resources")
	with open("resources.txt", "w", encoding="UTF-8") as wiki_dump:
		wiki_dump.write('This page has been automatically updated at ' + str(datetime.datetime.now()) + "\n")
		wiki_dump.write('{| class="wikitable sortable"\n')
		wiki_dump.write('|-\n')
		wiki_dump.write('! Name !! Description !! Tags !! Base maximum !! Is hidden !! Bonus \n')

		for json_value in result_list:
			resource_json = resource_info(json_value)

			wiki_dump.write('|-\n')
			# NAME part
			if resource_json.get('sym') is not None:
				wiki_dump.write('| <span id="' + str(resource_json['id']) + '">' + resource_json['sym'] + '[[' +  str(resource_json['name']) + ']]</span> ||')
			else:
				wiki_dump.write('| <span id="' + str(resource_json['id']) + '">[[' +  str(resource_json['name']) + ']]</span> ||')

			wiki_dump.write(str(resource_json['desc']) + ' || ')

			for tag in resource_json['tags']:
				wiki_dump.write(str(tag) + "<br/>")
			wiki_dump.write(' || ')

			wiki_dump.write(str(resource_json['base_max'] ) + ' || ')

			wiki_dump.write(str(resource_json['hidden'] ) + ' || ')

			for mod_key in resource_json['mod']:
				wiki_dump.write( str(mod_key) + ": " + str(resource_json['mod'][mod_key]) + '<br/>')
			wiki_dump.write('\n')
			generate_individual_res_page(resource_json)
			ret.append(resource_json['name'])
		wiki_dump.write('|}')

		return ret
