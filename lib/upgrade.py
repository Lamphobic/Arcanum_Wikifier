# -*- coding: UTF-8 -*-

import os, json, sys, datetime
import lib.extractlib as lib
import lib.wikilib as wiki

def extract_effect_key(effect_json):
	return_txt = ""
	if effect_json != None:
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
	upgrade['id'] = upgrade_json.get('id')
	if upgrade_json.get('name') != None:
		upgrade['name'] = upgrade_json.get('name')
	else:
		upgrade['name'] = upgrade['id']

	upgrade['sym']      = upgrade_json.get('sym')

	upgrade['desc']     = upgrade_json.get('desc')

	if upgrade_json.get('tags') != None:
		upgrade['tags'] = upgrade_json.get('tags').split(",")
	else:
		upgrade['tags'] = []

	if upgrade_json.get('cost') != None:
		upgrade['cost']  = upgrade_json.get('cost')
	else:
		upgrade['cost']  = {}

	if upgrade_json.get('max') != None:
		upgrade['max']  = upgrade_json.get('max')
	else:
		upgrade['max']  = "1"

	upgrade['effect']  = {}
	if upgrade_json.get('effect') != None:
		upgrade['effect']['effect']  = upgrade_json.get('effect')
	if upgrade_json.get('result') != None:
		upgrade['effect']['result']  = upgrade_json.get('result')
	if upgrade_json.get('mod') != None:
		upgrade['effect']['mod']  = upgrade_json.get('mod')

	if upgrade_json.get('require') != None:
		upgrade['require'] = upgrade_json.get('require')
	else: 
		upgrade['require'] = "Nothing"

	if upgrade_json.get('need') != None:
		upgrade['need'] = upgrade_json.get('need')
	else: 
		upgrade['need'] = "Nothing"

	return upgrade



def get_full_upgrade_list():
	result_list = lib.get_json("data/", "upgrade")
	upgrade_list
	for json_value in result_list:
		upgrade_list.append(upgrade_info(json_value))
	return upgrade_list

def generate_wiki():
	table_keys = ['Name', 'Description', 'Tags', 'Cost', 'Max', 'Effect', 'Requirement', 'Need to have'] 
	table_lines = []
	school_set = set()
	result_list = lib.get_json("data/", "upgrades")
	for json_value in result_list:
		upgrade_json = upgrade_info(json_value)
		table_line = []
		# NAME part
		if upgrade_json.get('sym') != None:
			table_line.append('| <span id="' + str(upgrade_json['id']) + '">' + upgrade_json['sym'] + '[[' +  str(upgrade_json['name']).capitalize() + ']]</span>')
		else:
			table_line.append('| <span id="' + str(upgrade_json['id']) + '">[[' +  str(upgrade_json['name']).capitalize() + ']]</span>')

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

		# Description part
		table_line.append(str(upgrade_json['max']))

		# Effect part
		table_line.append(str(get_effect_info(upgrade_json['effect'])))

		# Requirement part
		table_line.append(lib.recurs_json_to_str(upgrade_json['require']).replace("&&", "<br/>").replace("||", "<br/>OR<br/>"))

		# Need part
		table_line.append(lib.recurs_json_to_str(upgrade_json['need']).replace("&&", "<br/>").replace("||", "<br/>OR<br/>"))

		table_lines.append(table_line)

	with open("upgrades.txt", "w", encoding="UTF-8") as wiki_dump:
		wiki_dump.write('This page has been automatically updated the ' + str(datetime.datetime.now()) + "<br/>\n__FORCETOC__\n")

		wiki_dump.write("\n==Full List==\n")
		wiki_dump.write(wiki.make_table(table_keys, table_lines))

	return "upgrades.txt"