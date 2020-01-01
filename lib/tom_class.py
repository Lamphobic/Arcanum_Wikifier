# -*- coding: UTF-8 -*-

import os, json, sys
import lib.extractlib as lib
import lib.wikilib as wiki
import graphviz

def find_link(tom_class_list, class_graph):
	#Find requirement link and create a graphical edge to show them
	edge_list = []
	for source_item in tom_class_list:
		for tom_class_item in tom_class_list:
			if source_item['id'] in tom_class_item['require'] and not(source_item['id']+"<" in tom_class_item['require']) and not(source_item['id']+"=0" in tom_class_item['require']) and source_item['name'].capitalize() != tom_class_item['name'].capitalize():
				class_graph.edge(str(source_item['name'].capitalize()), str(tom_class_item['name'].capitalize()))
				edge_list.append([str(source_item['name'].capitalize()), str(tom_class_item['name'].capitalize())])
	#Find node from the same tier list used as requirement, and link them with an invisible line to shorten the distance between them. It allow class without oclasses' requirement to be pushed on the border and make the graph more pretty
	for tom_class_item in tom_class_list:
		for edge_name in edge_list:
			if edge_name[0] == str(tom_class_item['name'].capitalize()):
				for neighbour_item in tom_class_list:
					for tag1 in tom_class_item['tags']:
						for tag2 in neighbour_item['tags']:
							if tag1 == tag2:
								class_graph.edge(str(neighbour_item['name'].capitalize()), str(tom_class_item['name'].capitalize()), style='invis')

def tom_class_graph(tom_class_list=None):
	if tom_class_list == None:
		tom_class_list = []
		for json_value in result_list:
			tom_class_json = tom_class_info(json_value)
			tom_class_list.append(tom_class_json)

	class_graph = graphviz.Digraph(engine='dot')
	class_graph.attr(rankdir='TB', newrank="true", ranksep="2", constraint='false', fontsize="20")

	#############Apprenticeship_tier#############
	apprentice_subgraph = class_graph.subgraph(name='clusterA')
	class_graph.node('Apprenticeship_tier')
	with apprentice_subgraph as s:
		s.attr(rank='same')
		s.node('Apprenticeship')

	with class_graph.subgraph() as s:
		s.attr(rank='same')
		s.node('Apprenticeship')
		class_graph.node('Apprenticeship_tier')

	#############Job_tier#############
	job_subgraph = class_graph.subgraph(name='clusterJ')
	class_graph.node('Job_tier')
	with job_subgraph as s:
		s.attr(rank='same')
		for tom_class_item in tom_class_list:
			for tag in tom_class_item['tags']:
				if tag == "t_job":
					s.node(tom_class_item['name'].capitalize())
					class_graph.edge("Apprenticeship", str(tom_class_item['name'].capitalize()))

	with class_graph.subgraph() as s:
		s.attr(rank='same')
		for tom_class_item in tom_class_list:
			for tag in tom_class_item['tags']:
				if tag == "t_job":
					s.node(tom_class_item['name'].capitalize())
		class_graph.node('Job_tier')

	class_graph.edge('Apprenticeship_tier', 'Job_tier')

	#############Neophyte_tier#############
	neophyte_subgraph = class_graph.subgraph(name='clusterN')
	class_graph.node('Neophyte_tier')
	with neophyte_subgraph as s:
		s.attr(rank='same')
		s.node('Neophyte')
		for tom_class_item in tom_class_list:
			for tag in tom_class_item['tags']:
				if tag == "t_job":
					class_graph.edge(str(tom_class_item['name'].capitalize()), "Neophyte")

	with class_graph.subgraph() as s:
		s.attr(rank='same')
		s.node('Neophyte')
		s.node('Neophyte_tier')

	class_graph.edge('Job_tier', 'Neophyte_tier')

	#############tier i#############
	tier_subgraph = {}
	for i in range(0,7):
		tier_subgraph[i] = class_graph.subgraph(name='cluster' + str(i))
		class_graph.node('Tier' + str(i))
		with tier_subgraph[i] as s:

			if i>0:
				class_graph.edge(str('Tier' + str(i-1)), str('Tier' + str(i)))
			for tom_class_item in tom_class_list:
				for tag in tom_class_item['tags']:
					if tag == "t_tier"+ str(i):
						if "g.evil>0" in tom_class_item['require'] or "g.warlock>0" in tom_class_item['require'] or "g.reanimator>=1" in tom_class_item['require']:
							s.node(tom_class_item['name'].capitalize(), fillcolor='red', style='filled')
						elif "g.evil<=0" in tom_class_item['require'] or "g.evil==0" in tom_class_item['require']:
							s.node(tom_class_item['name'].capitalize(), fillcolor='cyan', style='filled')
						else:
							s.node(tom_class_item['name'].capitalize())

		with class_graph.subgraph() as s:
			s.attr(rank='same')
			s.node('Tier' + str(i))
			s.subgraph(name='cluster' + str(i))

			for tom_class_item in tom_class_list:
				for tag in tom_class_item['tags']:
					if tag == "t_tier"+ str(i):
						s.node(tom_class_item['name'].capitalize())


	class_graph.edge('Neophyte_tier', 'Tier0')

	find_link(tom_class_list, class_graph)

	class_graph.render(format="png", view=True)

def tom_class_info(tom_class_json):
#Get every information of a tom_class:
#ID, name, description, tags, cost, effect, requirement

	tom_class = {}
	tom_class['id'] = tom_class_json.get('id')
	if tom_class_json.get('name') != None:
		tom_class['name'] = tom_class_json.get('name')
	else:
		tom_class['name'] = tom_class['id']

	tom_class['sym'] = tom_class_json.get('sym')

	tom_class['desc'] = tom_class_json.get('desc')

	if tom_class_json.get('tags') != None:
		tom_class['tags'] = tom_class_json.get('tags').split(",")
	else:
		tom_class['tags'] = []


	if tom_class_json.get('cost') != None:
		tom_class['cost']  = tom_class_json.get('cost')
	else:
		tom_class['cost']  = {}

	tom_class['effect']  = {}
	if tom_class_json.get('mod') != None:
		if isinstance(tom_class_json.get('mod'),str):
			tom_class['effect'][tom_class_json.get('mod')] = True
		else:
			tom_class['effect']  = {**tom_class['effect'], **tom_class_json.get('mod')}
	if tom_class_json.get('effect') != None:
		if isinstance(tom_class_json.get('effect'),str):
			tom_class['effect'][tom_class_json.get('effect')] = True
		else:
			tom_class['effect']  = {**tom_class['effect'], **tom_class_json.get('effect')}		

	if tom_class_json.get('require') != None:
		tom_class['require'] = tom_class_json.get('require')
	else: 
		tom_class['require'] = "Nothing"

	return tom_class



def get_full_tom_class_list():
	result_list = lib.get_json("data/", "tom_class")
	tom_class_list
	for json_value in result_list:
		tom_class_list.append(tom_class_info(json_value))
	return tom_class_list


def tom_class_wiki():
	table_keys = ['Name', 'Description', 'Tags', 'Cost', 'Benefits', 'Requirement'] 
	table_lines = []
	tom_class_list = []
	result_list = lib.get_json("data/", "classes")
	for json_value in result_list:
		tom_class_json = tom_class_info(json_value)
		tom_class_list.append(tom_class_json)
		table_line = []
		# NAME part
		tmp_cell = ""
		if tom_class_json.get('sym') != None:
			tmp_cell += '| <span id="' + str(tom_class_json['id']) + '">' + tom_class_json['sym'] + '[[' +  str(tom_class_json['name']).capitalize() + ']]'
		else:
			tmp_cell += '| <span id="' + str(tom_class_json['id']) + '">[[' +  str(tom_class_json['name']).capitalize() + ']]'
		if "g.evil>0" in tom_class_json['require'] or "g.warlock>0" in tom_class_json['require'] or "g.reanimator>=1" in tom_class_json['require']:
			tmp_cell += "[[File:VileOnly.png|50px]]"
		if "g.evil<=0" in tom_class_json['require'] or "g.evil==0" in tom_class_json['require']:
			tmp_cell += "[[File:GoodOnly.png|50px]]"
		tmp_cell += '</span>'
		table_line.append(tmp_cell)

		# Description part
		table_line.append(str(tom_class_json['desc']))

		# Tags part
		tmp_cell = ""
		for tag in tom_class_json['tags']:
			tmp_cell += str(tag) + "<br/>"
		table_line.append(str(tmp_cell))

		# Cost part
		tmp_cell = ""
		if isinstance(tom_class_json['cost'],int):
			tmp_cell += "Gold: " + str(tom_class_json['cost'])
		else:
			for mod_key in tom_class_json['cost']:
				tmp_cell += (str(mod_key) + ": " + str(tom_class_json['cost'][mod_key]) + '<br/>')
		table_line.append(str(tmp_cell))

		# Effects part
		tmp_cell = ""
		if isinstance(tom_class_json['effect'],str):
			tmp_cell += "Give the following spell effect: " + str(tom_class_json['effect'])
		else:
			for mod_key in tom_class_json['effect']:
				tmp_cell += (str(mod_key) + ": " + str(tom_class_json['effect'][mod_key]) + '<br/>')
		table_line.append(str(tmp_cell))

		# Requirement part
		if isinstance(tom_class_json['require'],list):
			tmp_cell = ""
			for requirement in tom_class_json['require']:
				tmp_cell += str(requirement) + '<br/>'
			table_line.append(str(tmp_cell))
		else:
			table_line.append(str(tom_class_json['require'].replace("&&", "<br/>").replace("||", "<br/>OR<br/>")))

		table_lines.append(table_line)

	with open("classes.txt", "w", encoding="UTF-8") as wiki_dump:
		wiki_dump.write("\n==Apprenticeship Classe==\n")
		wiki_dump.write(wiki.make_table(table_keys, table_lines, table_filter=[[0, "'Apprentice' in cell"]]).replace(".max", " max").replace(".rate", " rate"))

		wiki_dump.write("\n==Job Classes==\n")
		wiki_dump.write(wiki.make_table(table_keys, table_lines, table_filter=[[2, "'t_job' in cell"]]).replace(".max", " max").replace(".rate", " rate"))
		
		wiki_dump.write("\n==Neophyte Classe==\n")
		wiki_dump.write(wiki.make_table(table_keys, table_lines, table_filter=[[0, "'Neophyte' in cell"]]).replace(".max", " max").replace(".rate", " rate"))

		for i in range(0,7):
			wiki_dump.write("\n==Tier " + str(i) + " Classes==\n")
			wiki_dump.write(wiki.make_table(table_keys, table_lines, table_filter=[[2, "'t_tier" + str(i) + "' in cell"]]).replace(".max", " max").replace(".rate", " rate"))

		wiki_dump.write("\n==Full List==\n")
		wiki_dump.write(wiki.make_table(table_keys, table_lines).replace(".max", " max").replace(".rate", " rate"))

	tom_class_graph(tom_class_list)