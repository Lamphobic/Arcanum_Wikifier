# -*- coding: UTF-8 -*-
"""
Original Author: Harrygiel
Contributors: Lamphobic
Purpose: Produce all pages directly related to homes.
"""

import os, json, sys, datetime, re
import lib.extractlib as lib
import lib.wikilib as wiki

def home_info(home_json):
#Get every information of a home:
#ID, name, flavor, size, tags, cost, effect, requirement

	home = {}
	home['type'] = 'homes'
	home['id'] = home_json.get('id')
	if home_json.get('name') is not None:
		home['name'] = home_json.get('name').title()
	else:
		home['name'] = home['id'].title()

	home['sym'] = home_json.get('sym')



	home['flavor'] = home_json.get('flavor')

	home['size'] = home_json.get('mod').get("space.max")

	if home_json.get('tags') is not None:
		home['tags'] = home_json.get('tags').split(",")
	else:
		home['tags'] = []

	if home_json.get('cost') is not None:
		home['cost']  = home_json.get('cost')
	else:
		home['cost']  = {}
	
	if home_json.get('mod') is not None:
		home['mod']  = home_json.get('mod')
	else:
		home['mod']  = {}
	
	if home_json.get('require') is not None:
		home['require'] = home_json.get('require')
	else: 
		home['require'] = "Nothing"
	
	home['requirements'] = {}
	home['requirements']['>'] = {}
	home['requirements']['<'] = {}
	requirements = home['requirements']
	if home_json.get('require') is not None:
		require = home_json.get('require')
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
		
	lib.name_exceptions(home)

	return home



def get_full_home_list():
	result_list = lib.get_json("data/", "homes")
	home_list = list()
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
		if home_json.get('sym') is not None:
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