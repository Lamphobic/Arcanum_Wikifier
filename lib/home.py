# -*- coding: UTF-8 -*-

import os, json, sys, datetime
import lib.extractlib as lib
import lib.wikilib as wiki

def home_info(home_json):
#Get every information of a home:
#ID, name, flavor, size, tags, cost, effect, requirement

	home = {}
	home['id'] = home_json.get('id')
	if home_json.get('name') != None:
		home['name'] = home_json.get('name')
	else:
		home['name'] = home['id']

	home['sym'] = home_json.get('sym')



	home['flavor'] = home_json.get('flavor')

	home['size'] = home_json.get('mod').get("space.max")

	if home_json.get('tags') != None:
		home['tags'] = home_json.get('tags').split(",")
	else:
		home['tags'] = []

	if home_json.get('cost') != None:
		home['cost']  = home_json.get('cost')
	else:
		home['cost']  = {}

	if home_json.get('mod') != None:
		home['mod']  = home_json.get('mod')
	else:
		home['mod']  = {}

	if home_json.get('require') != None:
		home['require'] = home_json.get('require')
	else: 
		home['require'] = "Nothing"

	return home



def get_full_home_list():
	result_list = lib.get_json("data/", "home")
	home_list
	for json_value in result_list:
		home_list.append(home_info(json_value))
	return home_list

#ID, name, flavor, size, tags, cost, effect, requirement

def generate_wiki():
	table_keys = ['Name', 'Description', 'Size', 'Tags', 'Cost', 'Effects', 'Requirement'] 
	table_lines = []
	result_list = lib.get_json("data/", "homes")
	for json_value in result_list:
		home_json = home_info(json_value)
		table_line = []
		# NAME part
		if home_json.get('sym') != None:
			table_line.append('| <span id="' + str(home_json['id']) + '">' + home_json['sym'] + '[[' +  str(home_json['name']).capitalize() + ']]</span>')
		else:
			table_line.append('| <span id="' + str(home_json['id']) + '">[[' +  str(home_json['name']).capitalize() + ']]</span>')

		# Description part
		table_line.append(str(home_json['flavor']))

		# Size part
		table_line.append(str(home_json['size'] ))

		# Tags part
		tmp_cell = ""
		for tag in home_json['tags']:
			tmp_cell += str(tag) + "<br/>"
		table_line.append(str(tmp_cell))

		# Cost part
		tmp_cell = ""
		if isinstance(home_json['cost'],int):
			tmp_cell += "Gold: " + str(home_json['cost'])
		else:
			for mod_key in home_json['cost']:
				tmp_cell += (str(mod_key) + ": " + str(home_json['cost'][mod_key]) + '<br/>')
		table_line.append(str(tmp_cell))
		
		# Effects part
		tmp_cell = ""
		for mod_key in home_json['mod']:
			tmp_cell += (str(mod_key) + ": " + str(home_json['mod'][mod_key]) + '<br/>')
		table_line.append(str(tmp_cell))

		# Requirement part
		if isinstance(home_json['require'],list):
			tmp_cell = ""
			for requirement in home_json['require']:
				tmp_cell += str(requirement) + '<br/>'
			table_line.append(str(tmp_cell))
		else:
			table_line.append(str(home_json['require'].replace("&&", "<br/>").replace("||", "<br/>OR<br/>")))

		table_lines.append(table_line)

	with open("homes.txt", "w", encoding="UTF-8") as wiki_dump:
		wiki_dump.write('This page has been automatically updated the ' + str(datetime.datetime.now()) + "\n")
		wiki_dump.write("\n==Full List==\n")
		wiki_dump.write(wiki.make_table(table_keys, table_lines).replace(".max", " max").replace(".rate", " rate"))

	return "homes.txt"