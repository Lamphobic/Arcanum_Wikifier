# -*- coding: UTF-8 -*-
"""
Original Author: Harrygiel
Contributors: Lamphobic
Purpose: Produce all pages directly related to spells.
"""

import os, json, sys, datetime
import lib.extractlib as lib
import lib.wikilib as wiki

def extract_effect_key(effect_json):
	return_txt = ""
	if effect_json is not None:
		if (effect_json,str):
			return_txt += str(effect_json)
		else:
			for mod_list in effect_json:
				return_txt += str(mod_list) + ": " + str(extract_effect_key(effect_json[mod_list]))
	return return_txt

def get_effect_info(effect_json):
	return_txt = ""
	is_treated = False
	for effect_key in effect_json:
		if effect_key is"dot":
			is_treated = True
			if effect_json[effect_key].get("name") is not None:
				return_txt += str(effect_json[effect_key].get("name")) + ": "
			if effect_json[effect_key].get("duration") is not None:
				return_txt += "for " + str(effect_json[effect_key].get("duration")) + " sec: "

				return_txt += extract_effect_key(effect_json[effect_key].get("mod"))
				return_txt += extract_effect_key(effect_json[effect_key].get("effect"))
		if effect_key is"attack":
			is_treated = True
			if effect_json[effect_key].get("name") is not None:
				return_txt += str(effect_json[effect_key].get("name")) + ": "
			if effect_json[effect_key].get("dmg") is not None:
				return_txt += "Deal " + str(effect_json[effect_key].get("dmg")) + " damage"
				if effect_json[effect_key].get("dot") is not None:
					return_txt += " and "
			if effect_json[effect_key].get("damage") is not None:
				return_txt += "Deal " + str(effect_json[effect_key].get("damage")) + " damage"
				if effect_json[effect_key].get("dot") is not None:
					return_txt += " and "
			if effect_json[effect_key].get("dot") is not None:
				return_txt += extract_effect_key(effect_json[effect_key].get("dot"))
		if effect_key is"effect":
			is_treated = True
			if isinstance(effect_json[effect_key], str):
				return_txt += str(effect_json[effect_key])
			else:
				if isinstance(effect_json[effect_key], list):
					for effect_item in effect_json[effect_key]:
						return_txt += str(effect_item) + ", "
					return_txt = return_txt[:-2]
				else:
					for effect_name in effect_json[effect_key]:
						return_txt += str(effect_name) + ": " + str(extract_effect_key(effect_json[effect_key][effect_name]))
		if not(is_treated):
			print("get_effect_info: error: " + effect_key)
	return return_txt

def spell_info(spell_json):
#Get every information of a spell:
#ID, name, flavor, school, level, unlocking cost, use cost, effect, upgrade, require
	spell = {}
	spell['id'] = spell_json.get('id')
	if spell_json.get('name') is not None:
		spell['name'] = spell_json.get('name').title()
	else:
		spell['name'] = spell['id'].title()

	spell['sym']      = spell_json.get('sym')

	spell['flavor']     = spell_json.get('flavor')

	if spell_json.get('school') is not None:
		spell['school']  = spell_json.get('school')
	else:
		spell['school']  = {}

	spell['level']     = spell_json.get('level')

	if spell_json.get('buy') is not None:
		spell['unlk_cost']  = spell_json.get('buy')
	else:
		spell['unlk_cost']  = {}

	if spell_json.get('cost') is not None:
		spell['use_cost']  = spell_json.get('cost')
	else:
		spell['use_cost']  = {}

	spell['effect']  = {}
	if spell_json.get('attack') is not None:
		spell['effect']['attack']  = spell_json.get('attack')
	if spell_json.get('dot') is not None:
		spell['effect']['dot']  = spell_json.get('dot')
	if spell_json.get('effect') is not None:
		spell['effect']['effect']  = spell_json.get('effect')

	if spell_json.get('at') is not None:
		spell['upgrade'] = spell_json.get('at')
	else: 
		spell['upgrade'] = "No"		

	if spell_json.get('require') is not None:
		spell['require'] = spell_json.get('require')
	else: 
		spell['require'] = "Nothing"
	spell['mod'] = {}
	if spell_json.get('dot') is not None:
		if spell_json.get('dot').get('mod') is not None:
			spell['mod'].update(spell_json.get('dot').get('mod'))
	if spell_json.get('dot') is not None:
		if spell_json.get('dot').get('effect') is not None:
			if isinstance(spell_json.get('dot').get('effect'), dict):
				spell['mod'].update(spell_json.get('dot').get('effect'))
	if spell_json.get('effect') is not None:
		if isinstance(spell_json.get('effect'), dict):
			spell['mod'].update(spell_json.get('effect'))
	return spell



def get_full_spell_list():
	result_list = lib.get_json("data/", "spells")
	spell_list = list()
	for json_value in result_list:
		spell_list.append(spell_info(json_value))
	return spell_list

def generate_wiki():
	table_keys = ['Name', 'Flavor', 'School', 'Level', 'Unlocking cost', 'Use cost', 'Effect', 'Upgrade', 'Requirement'] 
	table_lines = []
	school_set = set()
	result_list = lib.get_json("data/", "spells")
	for json_value in result_list:
		spell_json = spell_info(json_value)
		table_line = []
		# NAME part
		if spell_json.get('sym') is not None:
			table_line.append('| <span id="' + str(spell_json['id']) + '">' + spell_json['sym'] + '[[' +  str(spell_json['name']).capitalize() + ']]</span>')
		else:
			table_line.append('| <span id="' + str(spell_json['id']) + '">[[' +  str(spell_json['name']).capitalize() + ']]</span>')

		# Description part
		table_line.append(str(spell_json['flavor']))

		# School part
		tmp_cell = ""
		if isinstance(spell_json['school'],str):
			tmp_cell += str(spell_json['school'])
			school_set.add(str(spell_json['school']))
		else:
			for school in spell_json['school']:
				tmp_cell += str(school) + "<br/>"
				school_set.add(str(school))
		table_line.append(str(tmp_cell))

		# Level part
		table_line.append(str(spell_json['level']))

		# unlk_cost part
		tmp_cell = ""
		for mod_key in spell_json['unlk_cost']:
			tmp_cell += (str(mod_key) + ": " + str(spell_json['unlk_cost'][mod_key]) + '<br/>')
		table_line.append(str(tmp_cell))

		# use_cost part
		tmp_cell = ""
		for mod_key in spell_json['use_cost']:
			tmp_cell += (str(mod_key) + ": " + str(spell_json['use_cost'][mod_key]) + '<br/>')
		table_line.append(str(tmp_cell))

		# Effect part
		table_line.append(str(get_effect_info(spell_json['effect'])))

		# Upgrade part 
		tmp_cell = ""
		if isinstance(spell_json['upgrade'],str):
			tmp_cell += (str(spell_json['upgrade']))
		else:
			for level_key in spell_json['upgrade']:
				tmp_cell += ("After " + str(level_key) + "use:<br/>")
				level_json = spell_json['upgrade'][level_key]
				for result_key in level_json:
					tmp_cell += str(result_key) + ": " + str(level_json[result_key]) + "<br/>"
		table_line.append(str(tmp_cell))

		# Requirement part
		table_line.append(lib.recurs_json_to_str(spell_json['require']).replace("&&", "<br/>").replace("||", "<br/>OR<br/>"))
		
		table_lines.append(table_line)

	with open("spells.txt", "w", encoding="UTF-8") as wiki_dump:
		wiki_dump.write('This page has been automatically updated the ' + str(datetime.datetime.now()) + "\n")

		for school_type in school_set:
			wiki_dump.write("\n=="+ str(school_type).capitalize() + "==\n")
			wiki_dump.write(wiki.make_table(table_keys, table_lines, table_filter=[[2, "'" + str(school_type) + "' in cell"]]))

		wiki_dump.write("\n==Full List==\n")
		wiki_dump.write(wiki.make_table(table_keys, table_lines))

	return "spells.txt"