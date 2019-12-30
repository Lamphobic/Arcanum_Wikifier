# -*- coding: UTF-8 -*-

import os, json, sys
import lib.extractlib as lib

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
	result_list = lib.get_json("data/", "furniture")
	with open("furnitures.txt", "w", encoding="UTF-8") as wiki_dump:
		wiki_dump.write('{| class="wikitable sortable"\n')
		wiki_dump.write('|-\n')
		wiki_dump.write('! Name !! Description !! Tags !! Base maximum !! Cost !! Bonus !! Requirement \n')

		for json_value in result_list:
			furniture_json = furniture_info(json_value)

			wiki_dump.write('|-\n')
			# NAME part
			if furniture_json.get('sym') != None:
				wiki_dump.write('| <span id="' + str(furniture_json['id']) + '">' + furniture_json['sym'] + '[[' +  str(furniture_json['name']) + ']]</span> ||')
			else:
				wiki_dump.write('| <span id="' + str(furniture_json['id']) + '">[[' +  str(furniture_json['name']) + ']]</span> ||')

			wiki_dump.write(str(furniture_json['desc']) + ' || ')

			for tag in furniture_json['tags']:
				wiki_dump.write(str(tag) + "<br/>")
			wiki_dump.write(' || ')

			wiki_dump.write(str(furniture_json['base_max'] ) + ' || ')

			for mod_key in furniture_json['cost']:
				wiki_dump.write(str(mod_key) + ": " + str(furniture_json['cost'][mod_key]) + '<br/>')
			wiki_dump.write(' || ')
			
			for mod_key in furniture_json['mod']:
				wiki_dump.write(str(mod_key) + ": " + str(furniture_json['mod'][mod_key]) + '<br/>')

			wiki_dump.write(' || ')

			wiki_dump.write(str(furniture_json['require'].replace("&&", "<br/>").replace("||", "<br/>OR<br/>")))

			wiki_dump.write('\n')
		wiki_dump.write('|}')
