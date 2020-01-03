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

def action_info(action_json):
#Get every information of a action:
#ID, name, description, cost, length, effect, upgrade, require
	action = {}
	action['id'] = action_json.get('id')
	if action_json.get('name') != None:
		action['name'] = action_json.get('name')
	else:
		action['name'] = action['id']

	action['sym']      = action_json.get('sym')

	action['desc']     = action_json.get('desc')

	if action_json.get('cost') != None:
		action['cost']  = action_json.get('cost')
	else:
		action['cost']  = {}

	if action_json.get('length') != None:
		action['length']  = action_json.get('length')
	else:
		action['length']  = "Instant"

	action['effect']  = {}
	if action_json.get('effect') != None:
		action['effect']['effect']  = action_json.get('effect')
	if action_json.get('result') != None:
		action['effect']['result']  = action_json.get('result')

	if action_json.get('at') != None:
		action['upgrade'] = action_json.get('at')
	else: 
		action['upgrade'] = "No"		

	if action_json.get('require') != None:
		action['require'] = action_json.get('require')
	else: 
		action['require'] = "Nothing"

	return action



def get_full_action_list():
	result_list = lib.get_json("data/", "action")
	action_list
	for json_value in result_list:
		action_list.append(action_info(json_value))
	return action_list

def generate_wiki():
	table_keys = ['Name', 'Description', 'Use cost', 'Length', 'Effect', 'Upgrade', 'Requirement'] 
	table_lines = []
	school_set = set()
	result_list = lib.get_json("data/", "actions")
	for json_value in result_list:
		action_json = action_info(json_value)
		table_line = []
		# NAME part
		if action_json.get('sym') != None:
			table_line.append('| <span id="' + str(action_json['id']) + '">' + action_json['sym'] + '[[' +  str(action_json['name']).capitalize() + ']]</span>')
		else:
			table_line.append('| <span id="' + str(action_json['id']) + '">[[' +  str(action_json['name']).capitalize() + ']]</span>')

		# Description part
		table_line.append(str(action_json['desc']))

		# cost part
		tmp_cell = ""
		if isinstance(action_json['cost'],str):
			tmp_cell += (str(action_json['cost']))
		elif isinstance(action_json['cost'], int):
			tmp_cell += ("Gold: " + str(action_json['cost']))
		else:
			for mod_key in action_json['cost']:
				tmp_cell += (str(mod_key) + ": " + str(action_json['cost'][mod_key]) + '<br/>')
		table_line.append(str(tmp_cell))

		# Length part
		table_line.append(str(action_json['length']))

		# Effect part
		table_line.append(str(get_effect_info(action_json['effect'])))

		# Upgrade part 
		tmp_cell = ""
		if isinstance(action_json['upgrade'],str):
			tmp_cell += (str(action_json['upgrade']))
		else:
			for level_key in action_json['upgrade']:
				tmp_cell += ("After " + str(level_key) + "use:<br/>")
				level_json = action_json['upgrade'][level_key]
				for result_key in level_json:
					tmp_cell += str(result_key) + ": " + str(level_json[result_key]) + "<br/>"
		table_line.append(str(tmp_cell))

		# Requirement part
		table_line.append(lib.recurs_json_to_str(action_json['require']).replace("&&", "<br/>").replace("||", "<br/>OR<br/>"))
		
		table_lines.append(table_line)

	with open("actions.txt", "w", encoding="UTF-8") as wiki_dump:
		wiki_dump.write('This page has been automatically updated the ' + str(datetime.datetime.now()) + "<br/>\n__FORCETOC__\n")

		wiki_dump.write("\n==Instant actions==\n")
		wiki_dump.write(wiki.make_table(table_keys, table_lines, table_filter=[[3, "'Instant' in cell"]]))

		wiki_dump.write("\n==Time consuming actions==\n")
		wiki_dump.write(wiki.make_table(table_keys, table_lines, table_filter=[[3, "not('Instant' in cell)"]]))

		wiki_dump.write("\n==Full List==\n")
		wiki_dump.write(wiki.make_table(table_keys, table_lines))

	return "actions.txt"