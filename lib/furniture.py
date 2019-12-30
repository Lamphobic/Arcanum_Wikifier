# -*- coding: UTF-8 -*-

import os, json, sys
import lib.extractlib as lib
import lib.wikilib as wiki

def furniture_info(furniture_json):
#Get every information of a furniture:
#ID, name, description, tags, base maximum, cost, bonus, requirement

	furniture = {}
	furniture['id'] = furniture_json.get('id')
	if furniture_json.get('name') != None:
		furniture['name'] = furniture_json.get('name')
	else:
		furniture['name'] = furniture['id']

	furniture['sym']  = furniture_json.get('sym')



	furniture['desc']     = furniture_json.get('desc')

	if furniture_json.get('tags') != None:
		furniture['tags'] = furniture_json.get('tags').split(",")
	else:
		furniture['tags'] = []

	if furniture_json.get('repeat') == True:
		furniture['base_max'] = None
	elif furniture_json.get('max') != None:
		furniture['base_max'] = furniture_json.get('max')
	else:
		furniture['base_max'] = 1

	if furniture_json.get('cost') != None:
		furniture['cost']  = furniture_json.get('cost')
	else:
		furniture['cost']  = {}

	if furniture_json.get('mod') != None:
		furniture['mod']  = furniture_json.get('mod')
	else:
		furniture['mod']  = {}

	if furniture_json.get('require') != None:
		furniture['require'] = furniture_json.get('require')
	else: 
		furniture['require'] = "Nothing"

	return furniture



def get_full_furniture_list():
	result_list = lib.get_json("data/", "furniture")
	furniture_list
	for json_value in result_list:
		furniture_list.append(furniture_info(json_value))
	return furniture_list



def furniture_wiki():
	table_keys = ['Name', 'Description', 'Tags', 'Base maximum', 'Cost', 'Bonus', 'Requirement'] 
	table_lines = []
	result_list = lib.get_json("data/", "furniture")
	for json_value in result_list:
		furniture_json = furniture_info(json_value)
		table_line = []
		# NAME part
		if furniture_json.get('sym') != None:
			table_line.append('| <span id="' + str(furniture_json['id']) + '">' + furniture_json['sym'] + '[[' +  str(furniture_json['name']).capitalize() + ']]</span>')
		else:
			table_line.append('| <span id="' + str(furniture_json['id']) + '">[[' +  str(furniture_json['name']).capitalize() + ']]</span>')

		# Description part
		table_line.append(str(furniture_json['desc']))

		# Tags part
		tmp_cell = ""
		for tag in furniture_json['tags']:
			tmp_cell += str(tag) + "<br/>"
		table_line.append(str(tmp_cell))

		# Base maximum part
		table_line.append(str(furniture_json['base_max'] ))

		# Cost part
		tmp_cell = ""
		for mod_key in furniture_json['cost']:
			tmp_cell += (str(mod_key) + ": " + str(furniture_json['cost'][mod_key]) + '<br/>')
		table_line.append(str(tmp_cell))
		
		# Bonus part
		tmp_cell = ""
		for mod_key in furniture_json['mod']:
			tmp_cell += (str(mod_key) + ": " + str(furniture_json['mod'][mod_key]) + '<br/>')
		table_line.append(str(tmp_cell))

		# Requirement part
		table_line.append(str(furniture_json['require'].replace("&&", "<br/>").replace("||", "<br/>OR<br/>")))

		table_lines.append(table_line)

	with open("furnitures.txt", "w", encoding="UTF-8") as wiki_dump:
		wiki_dump.write("Furniture is a type of item that can be placed in your home at the cost of floor space. They provide various benefits, but the most important, nonobvious benefit is the tags on furniture, since certain furniture tags can unlock certain actions or skills.\n")

		wiki_dump.write("\n==Gold==\n")
		wiki_dump.write("Increases maximum gold, and sometimes other valuable resources such as gems.:\n")
		wiki_dump.write(wiki.make_table(table_keys, table_lines, table_filter=[[5, "'gold.max' in cell"]]).replace(".max", " max").replace(".rate", " rate"))

		wiki_dump.write("\n==Research==\n")
		wiki_dump.write("Increases at least one of maximum scrolls, maximum codices, maximum starcharts, maximum tomes or maximum rune stone, giving you more research:\n")
		wiki_dump.write(wiki.make_table(table_keys, table_lines, table_filter=[[5, "'scrolls.max' in cell or 'codices.max' in cell or 'tomes.max' in cell or 'runestones.max' in cell or 't_runes.max' in cell or 'starcharts.max' in cell"]]).replace(".max", " max").replace(".rate", " rate"))

		wiki_dump.write("\n==Source==\n")
		wiki_dump.write("List of every item used to be able to discover or use a skill:\n")
		wiki_dump.write(wiki.make_table(table_keys, table_lines, table_filter=[[2, "'source' in cell"], [0, "'loom' in cell"]]).replace(".max", " max").replace(".rate", " rate"))

		wiki_dump.write("\n==Skill max==\n")
		wiki_dump.write("List of every item used to get a higher skill level:\n")
		wiki_dump.write(wiki.make_table(table_keys, table_lines, table_filter=[[5, "'lore.max' in cell"]]).replace(".max", " max").replace(".rate", " rate"))

		wiki_dump.write("\n==Full List==\n")
		wiki_dump.write(wiki.make_table(table_keys, table_lines).replace(".max", " max").replace(".rate", " rate"))
