# -*- coding: UTF-8 -*-
"""
Original Author: Harrygiel
Contributors: Lamphobic
Purpose: Produce all pages directly related to tasks.
"""

import os, json, sys, datetime
import lib.extractlib as lib
import lib.wikilib as wiki

def potion_info(potion_json):
#Get every information of a potion:
#ID, name, flavor, level, unlock cost, brewing cost, effect

	potion = {}
	potion['type'] = 'potions'
	potion['id'] = potion_json.get('id')
	if potion_json.get('name') is not None:
		potion['name'] = potion_json.get('name').title()
	else:
		potion['name'] = potion['id'].title()

	potion['sym'] = potion_json.get('sym')


	potion['flavor'] = potion_json.get('flavor')

	if potion_json.get('level') is not None:
		potion['level']  = potion_json.get('level')
	else:
		potion['level']  = 1

	if potion_json.get('buy') is not None:
		potion['unlk_cost']  = potion_json.get('buy')
	else:
		potion['unlk_cost']  = {}

	if potion_json.get('cost') is not None:
		potion['brewing_cost']  = potion_json.get('cost')
	else:
		potion['brewing_cost']  = {}


	if potion_json.get('use') is not None:
		potion['effect']  = potion_json.get('use')
	else:
		potion['effect']  = {}
		
	potion['mod'] = {}
	if potion_json.get('use') is not None and not isinstance(potion_json.get('use'), str) :
		if potion_json.get('use').get('effect') is not None:
			potion['mod'] = potion_json.get('use').get('effect')
		elif potion_json.get('use').get('mod') is not None:
			potion['mod'] = potion_json.get('use').get('mod')
		else:
			if isinstance(potion_json.get('use'), dict):
				potion['mod'] = potion_json.get('use')
		
	return potion



def get_full_potion_list():
	result_list = lib.get_json("data/", "potions")
	potion_list = list()
	for json_value in result_list:
		potion_list.append(potion_info(json_value))
	return potion_list

#ID, name, flavor, size, tags, cost, effect, requirement

def generate_wiki():
	table_keys = ['Name', 'Description', 'Level', 'Unlock cost', 'Brewing cost', 'Effects'] 
	table_lines = []
	result_list = lib.get_json("data/", "potions")
	for json_value in result_list:
		potion_json = potion_info(json_value)
		table_line = []
		# NAME part
		if potion_json.get('sym') is not None:
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
			if potion_json['effect'].get('dot') is not None:
				tmp_cell += "Give the following effect for " + str(potion_json['effect'].get('dot').get('duration')) + " seconds: <br/>"
				effect_json = {}
				if potion_json['effect'].get('dot').get('mod') is not None:
					effect_json = {**effect_json, **potion_json['effect'].get('dot').get('mod')}
				if potion_json['effect'].get('dot').get('effect') is not None:
					effect_json = {**effect_json, **potion_json['effect'].get('dot').get('effect')}
				for mod_key in effect_json:
					tmp_cell += (str(mod_key) + ": " + str(effect_json[mod_key]) + '<br/>')
			else:
				for mod_key in potion_json['effect']:
					tmp_cell += (str(mod_key) + ": " + str(potion_json['effect'][mod_key]) + '<br/>')
					
		table_line.append(str(tmp_cell))

		table_lines.append(table_line)

	with open("potions.txt", "w", encoding="UTF-8") as wiki_dump:
		wiki_dump.write('This page has been automatically updated the ' + str(datetime.datetime.now()) + "\n")
		wiki_dump.write("\n==Full List==\n")
		wiki_dump.write(wiki.make_table(table_keys, table_lines).replace(".max", " max").replace(".rate", " rate"))

	return "potions.txt"