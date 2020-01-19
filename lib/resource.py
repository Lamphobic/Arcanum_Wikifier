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
import lib.wikilib as wiki

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
			res_page.write('==Description==\n' + res['desc'] + '\n')
		if res['tags']:
			res_page.write('==Tags==\n' + ' '.join(res['tags']) + '\n')
		res_page.write('==Base Max==\n' + str(res['base_max']) + '\n')
		res_page.write('==Is Hidden==\n' + res['hidden'] + '\n')
		if res['mod']:
			res_page.write('==Affects==\n')
			for mod_key in res['mod']:
				res_page.write('*' + str(mod_key) + ": " + str(res['mod'][mod_key]) + '\n')
		baffected = False;
		bsource = False;
		affected_by = list()
		sources = list()
		matchid = res['id'].lower()
		#Build Sources
		for l in lists: #for each list of entries
			sources = list()
			for e in lists[l]: #for each entry in this list
				if e['mod']: #if this entry has any mods
					for mod_key in e['mod']: #for each mod in the mods of this entry
						matchmod = str(mod_key).lower().split('.')
						if matchid in matchmod: #if this mod references this resource by id
							if matchid == str(mod_key).lower():
								sources.append('<span id="' + str(e['id']) + '">[[' + e['name'] + ']]: ' + str(mod_key) + ": " + str(e['mod'][mod_key]))
			sources.sort()
			if sources:
				if not bsource:
					res_page.write('==Sources==\n')
					bsource = True
				res_page.write(('===' + l + '===\n').title())
				for e in sources:
					res_page.write('* ' + e + '\n')
		#Build Affected By
		for l in lists: #for each list of entries
			affected_by = list()
			for e in lists[l]: #for each entry in this list
				if e['mod']: #if this entry has any mods
					for mod_key in e['mod']: #for each mod in the mods of this entry
						matchmod = str(mod_key).lower().split('.')
						if matchid in matchmod: #if this mod references this resource by id
							if matchid != str(mod_key).lower():
								affected_by.append('<span id="' + str(e['id']) + '">[[' + e['name'] + ']]: ' + str(mod_key) + ": " + str(e['mod'][mod_key]))
			affected_by.sort()
			if affected_by:
				if not baffected:
					res_page.write('==Affected By==\n')
					baffected = True
				res_page.write(('===' + l + '===\n').title())
				for e in affected_by:
					res_page.write('* ' + e + '\n')


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
	
	table_keys = ['Name','Description','Tags','Base Maximum','Bonus']
	table_lines = []
	result_list = lib.get_json("data/", "resources")
	result_list = sorted(result_list, key=lambda res: res.get('id').title() if res.get('name') is None else res.get('name').title()) #Presorts results by name.
	for json_value in result_list:
		resource_json = resource_info(json_value)
		
		table_line = []
		
		
		if resource_json.get('sym') is not None:
			table_line.append('| <span id="' + str(resource_json['id']) + '">' + resource_json['sym'] + '[[' +  str(resource_json['name']) + ']]</span>')
		else:
			table_line.append('| <span id="' + str(resource_json['id']) + '">[[' +  str(resource_json['name']) + ']]</span>')
			
		# Description part
		table_line.append(str(resource_json['desc']))
		
		# Tags part
		cell = "";
		for tag in resource_json['tags']:
			cell += (str(tag) + "<br/>")
		table_line.append(cell)
		
		# Base Maximum part
		table_line.append(str(resource_json['base_max']))
		
		# Bonus part
		cell = ""
		for mod_key in resource_json['mod']:
			cell += (str(mod_key) + ": " + str(resource_json['mod'][mod_key]) + '<br/>')
		table_line.append(cell)
		
		# Add line to lines
		table_lines.append(table_line)
		
		if not main_only:
			generate_individual_res_page(resource_json)
			ret.append(resource_json['name'])
			
	with open("resources.txt", "w", encoding="UTF-8") as wiki_dump:
		wiki_dump.write('This page has been automatically updated at ' + str(datetime.datetime.now()) + "<br/>\n__FORCETOC__\n")
		
		wiki_dump.write("\n==General Resources==\n")
		wiki_dump.write(wiki.make_table(table_keys, table_lines,table_filter=[[2, "'magicgems' not in cell and 'manas' not in cell and 't_runes' not in cell"]]))
		
		wiki_dump.write("\n==Magic Gems==\n")
		wiki_dump.write(wiki.make_table(table_keys, table_lines,table_filter=[[2, "'magicgems' in cell"]]))
		
		wiki_dump.write("\n==Runes==\n")
		wiki_dump.write(wiki.make_table(table_keys, table_lines,table_filter=[[2, "'t_runes' in cell"]]))
		
		wiki_dump.write("\n==Manas==\n")
		wiki_dump.write(wiki.make_table(table_keys, table_lines,table_filter=[[2, "'manas' in cell"]]))
		
		wiki_dump.write("\n==Full List==\n")
		wiki_dump.write(wiki.make_table(table_keys, table_lines))

	return ret
