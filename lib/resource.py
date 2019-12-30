# -*- coding: UTF-8 -*-

import os, json, sys
import lib.extractlib as lib

def resource_info(resource_json):
#Get every information of a resource:
#ID, name, description, tags, base maximum, hidden, bonus

	resource = {}
	resource['id'] = resource_json.get('id')
	if resource_json.get('name') != None:
		resource['name'] = resource_json.get('name')
	else:
		resource['name'] = resource['id']

	resource['sym']  = resource_json.get('sym')



	resource['desc']    = resource_json.get('desc')

	if resource_json.get('tags') != None:
		resource['tags'] = resource_json.get('tags').split(",")
	else:
		resource['tags'] = []

	resource['base_max']    = resource_json.get('max')

	if resource_json.get('hide') == True:
			resource['hidden'] = "Yes"
	else:
		resource['hidden'] = "No"

	if resource_json.get('mod') != None:
		resource['mod'] = resource_json.get('mod')
	else:
		resource['mod'] = {}

	return resource



def get_full_resource_list():
	result_list = lib.get_json("data/", "resources")
	resource_list
	for json_value in result_list:
		resource_list.append(resource_info(json_value))
	return resource_list



def resource_wiki():
	result_list = lib.get_json("data/", "resources")
	with open("resources.txt", "w", encoding="UTF-8") as wiki_dump:
		wiki_dump.write('{| class="wikitable sortable"\n')
		wiki_dump.write('|-\n')
		wiki_dump.write('! Name !! Description !! Tags !! Base maximum !! Is hidden !! Bonus \n')

		for json_value in result_list:
			resource_json = resource_info(json_value)

			wiki_dump.write('|-\n')
			# NAME part
			if resource_json.get('sym') != None:
				wiki_dump.write('| <span id="' + str(resource_json['id']) + '">' + resource_json['sym'] + '[[' +  str(resource_json['name']) + ']]</span> ||')
			else:
				wiki_dump.write('| <span id="' + str(resource_json['id']) + '">[[' +  str(resource_json['name']) + ']]</span> ||')

			wiki_dump.write(str(resource_json['desc']) + ' || ')

			for tag in resource_json['tags']:
				wiki_dump.write(str(tag) + "<br/>")
			wiki_dump.write(' || ')

			wiki_dump.write(str(resource_json['base_max'] ) + ' || ')

			wiki_dump.write(str(resource_json['hidden'] ) + ' || ')

			for mod_key in resource_json['mod']:
				wiki_dump.write( str(mod_key) + ": " + str(resource_json['mod'][mod_key]) + '<br/>')
			wiki_dump.write('\n')
		wiki_dump.write('|}')
