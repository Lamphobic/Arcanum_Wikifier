# -*- coding: UTF-8 -*-

import os, json, sys
import lib.extractlib as lib
import lib.wikilib as wiki

def potion_info(potion_json):
#Get every information of a potion:
#ID, name, flavor, level, unlock cost, brewing cost, effect

	potion = {}
	potion['id'] = potion_json.get('id')
	if potion_json.get('name') != None:
		potion['name'] = potion_json.get('name')
	else:
		potion['name'] = potion['id']

	potion['sym'] = potion_json.get('sym')


	potion['flavor'] = potion_json.get('flavor')

	if potion_json.get('level') != None:
		potion['level']  = potion_json.get('level')
	else:
		potion['level']  = 1

	if potion_json.get('buy') != None:
		potion['unlk_cost']  = potion_json.get('buy')
	else:
		potion['unlk_cost']  = {}

	if potion_json.get('cost') != None:
		potion['brewing_cost']  = potion_json.get('cost')
	else:
		potion['brewing_cost']  = {}


	if potion_json.get('use') != None:
		potion['effect']  = potion_json.get('use')
	else:
		potion['effect']  = {}

	return potion



def get_full_potion_list():
	result_list = lib.get_json("data/", "potion")
	potion_list
	for json_value in result_list:
		potion_list.append(potion_info(json_value))
	return potion_list

#ID, name, flavor, size, tags, cost, effect, requirement

def potion_wiki():
	table_keys = ['Name', 'Description', 'Level', 'Unlock cost', 'Brewing cost', 'Effects'] 
	table_lines = []
	result_list = lib.get_json("data/", "potions")
	for json_value in result_list:
		potion_json = potion_info(json_value)
		table_line = []
		# NAME part
		if potion_json.get('sym') != None:
			table_line.append('| <span id="' + str(potion_json['id']) + '">' + potion_json['sym'] + '[[' +  str(potion_json['name']).capitalize() + ']]</span>')
		else:
			table_line.append('| <span id="' + str(potion_json['id']) + '">[[' +  str(potion_json['name']).capitalize() + ']]</span>')

		# Description part
		table_line.append(str(potion_json['flavor']))

		# level part
		table_line.append(str(potion_json['level'] ))

		# unlk_cost part
		tmp_cell = ""
		if isinstance(potion_json['unlk_cost'],int):
			tmp_cell += "Gold: " + str(potion_json['unlk_cost'])
		else:
			for mod_key in potion_json['unlk_cost']:
				tmp_cell += (str(mod_key) + ": " + str(potion_json['unlk_cost'][mod_key]) + '<br/>')
		table_line.append(str(tmp_cell))

		# Cost part
		tmp_cell = ""
		if isinstance(potion_json['brewing_cost'],int):
			tmp_cell += "Gold: " + str(potion_json['brewing_cost'])
		else:
			for mod_key in potion_json['brewing_cost']:
				tmp_cell += (str(mod_key) + ": " + str(potion_json['brewing_cost'][mod_key]) + '<br/>')
		table_line.append(str(tmp_cell))

		# Effects part
		tmp_cell = ""
		if isinstance(potion_json['effect'],str):
			tmp_cell += "Give the following spell effect: " + str(potion_json['effect'])
		else:
			if potion_json['effect'].get('dot') != None:
				tmp_cell += "Give the following effect for " + str(potion_json['effect'].get('dot').get('duration')) + " seconds: <br/>"
				effect_json = {}
				if potion_json['effect'].get('dot').get('mod') != None:
					effect_json = {**effect_json, **potion_json['effect'].get('dot').get('mod')}
				if potion_json['effect'].get('dot').get('effect') != None:
					effect_json = {**effect_json, **potion_json['effect'].get('dot').get('effect')}
				for mod_key in effect_json:
					tmp_cell += (str(mod_key) + ": " + str(effect_json[mod_key]) + '<br/>')
			else:
				for mod_key in potion_json['effect']:
					tmp_cell += (str(mod_key) + ": " + str(potion_json['effect'][mod_key]) + '<br/>')
					
		table_line.append(str(tmp_cell))

		table_lines.append(table_line)

	with open("potions.txt", "w", encoding="UTF-8") as wiki_dump:
		wiki_dump.write("\n==Full List==\n")
		wiki_dump.write(wiki.make_table(table_keys, table_lines).replace(".max", " max").replace(".rate", " rate"))
