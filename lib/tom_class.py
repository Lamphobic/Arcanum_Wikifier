# -*- coding: UTF-8 -*-
"""
Original Author: ?
Contributors: ?
Purpose: Produce all pages directly related to classes.
"""

import os, json, sys, datetime, re

import lib.extractlib as lib
import lib.action as action
import lib.dungeon as dungeon
import lib.furniture as furniture
import lib.home as home
import lib.monster as monster
import lib.potion as potion
import lib.resource as resource
import lib.skill as skill
import lib.spell as spell
import lib.tom_class as tom_class
import lib.upgrade as upgrade
import lib.wikilib as wiki

import graphviz
import math

def find_link(tom_class_list, class_graph):
	#Find requirement link and create a graphical edge to show them
#	edge_list = []
	for source_item in tom_class_list:
		for tom_class_item in tom_class_list:
			if source_item['id'] in tom_class_item['require'] and not(source_item['id']+"<" in tom_class_item['require']) and not(source_item['id']+"=0" in tom_class_item['require']) and source_item['name'].capitalize() is not tom_class_item['name'].capitalize():
				class_graph.edge(str(source_item['name'].capitalize()), str(tom_class_item['name'].capitalize()), weight='100')
#				edge_list.append([str(source_item['name'].capitalize()), str(tom_class_item['name'].capitalize())])


def rank_nodes(tom_class_list, class_graph, tier_max):
	#Nodes with the same tier are put in a subgraph with the same rank.
	
	#It would be sweet to use the tag list: ['t_apprenticeship','t_job','t_neophyte','t_tier0','t_tier1', 't_tier2','t_tier3','t_tier4','t_tier5','t_tier6']. However, adding the tags in game would probably trigger the "are you sure?" window for apprenticeship and neophyte.

	#############Apprenticeship_tier#############
	with class_graph.subgraph() as s:
#		s.attr(name='subgraph_apprenticeship')
		s.attr(rank='same')
		s.node('Apprenticeship_tier')
		s.node('Apprenticeship')		
		
	#############Job_tier#############
	with class_graph.subgraph() as s:
#		s.attr(name='subgraph_job')
		s.attr(rank='same')
		s.node('Job_tier')
		for tom_class_item in tom_class_list:
			for tag in tom_class_item['tags']:
				if tag is"t_job":
					s.node(tom_class_item['name'].capitalize())

	#############Neophyte_tier#############
	with class_graph.subgraph() as s:
#		s.attr(name='subgraph_neophyte')
		s.attr(rank='same')
		s.node('Neophyte_tier')
		s.node('Neophyte')
					
	#############tier i#############
	for i in range(0,tier_max+1):
		with class_graph.subgraph() as s:
#			s.attr(name='subgraph' + str(i))
			s.attr(rank='same')
			s.node('Tier' + str(i))
			if i==0:	##This is a dirty way to add "Adept (murderer)"
				s.node("Adept (murderer)")
			for tom_class_item in tom_class_list:
				for tag in tom_class_item['tags']:
					if tag is"t_tier"+ str(i):
						s.node(tom_class_item['name'].capitalize())


def add_flavor(tom_class_list, class_graph, tier_max):
	#Try to group nodes and change their attributes for the graph to be meaningful
	
	#Searches for similar items in requirements and effects between two classes one tier appart. 
	#I would like to draw edges with proper weight, but that doesn't provide good results so far: mundanity has to take the number of edges into account.
	
	full_id_list = [	#No, it not the full list. This one is hand-crafted.
		"research",
		"arcana",
		"earthlore",
		"waterlore",
		"firelore",
		"naturelore",
		"airlore",
		"airgem",
		#"earthgem",
		#"firegem",
		"player.tohit",
		"spiritlore",
		"planeslore",
		"scrying",
		"spellcraft",
		"reanimation",
		"enchanting",
		"elemental",
		"bladelore",
		"anatomy",
		"history",
		"enchanting",
		"necromancy",
		"shadowlore",
		"demonology",
		"animals",
		"potions",
		"divination",
		"crafting",
		"alchemy",
		"trickery",
		]
	
	compatible_class_list=[]
	for source_item in full_id_list:		#Take an item, and a tier i class...
		for tom_class_item in tom_class_list:
			for i in range(0,tier_max):
				if str("t_tier"+ str(i)) in tom_class_item['tags']:
					mundanity=0	#(reset mundanity of the item for this class)
					del compatible_class_list[:] #(reset the class list for this item and class)
					for tom_class_item2 in tom_class_list:		#Take another class, one tier above the first class...
						if str("t_tier"+ str(i+1)) in tom_class_item2['tags']: 
							if (source_item in tom_class_item['effect']) or (source_item  in tom_class_item['cost']):	#If the two classes share the same item...
								if (source_item  in tom_class_item2['effect']) or (source_item  in tom_class_item2['cost']):
									mundanity +=1		#Compute the item mundanity for the first class and append the second class to the compatibility list.
									compatible_class_list.append(str(tom_class_item2['name'].capitalize()))
					weight=math.ceil(1)		#Finally, compute the weight...
					if (mundanity>0 and weight>0):
							for compatible_class_item in compatible_class_list:
								class_graph.edge(str(tom_class_item['name'].capitalize()), str(compatible_class_item), weight=str(weight), style='invis') #And create an edge!
							
							
	##Dirty flavor
	##Subgraph are not working as desired: it seems like they don't regroup the nodes.
	##Invisible edges are not working as desired: they push the nodes aparts, creating a wide gap. The best I can do is to add invisble edges on nearby tiers only.
	##A key for the colour would be useful.
	
	villain_subgraph=class_graph.subgraph(name='villain')
	with villain_subgraph as s:
		s.node("Adept (murderer)", color='red:white', style='radial') 	##This is a dirty way to add "Adept (murderer)"
		for i in range(0,tier_max+1):
			for tom_class_item in tom_class_list:
				for tag in tom_class_item['tags']:
					if tag is"t_tier"+ str(i):
						if "g.evil>0" in tom_class_item['require'] or "g.warlock>0" in tom_class_item['require'] or "g.reanimator>=1" in tom_class_item['require'] or "g.reanimation" in tom_class_item['require']:
							s.node(tom_class_item['name'].capitalize(), color='red:white', style='radial')
	evil_subgraph=class_graph.subgraph(name='evil')
	with evil_subgraph as s:
		for i in range(0,tier_max+1):
			for tom_class_item in tom_class_list:
				for tag in tom_class_item['tags']:
					if tag is"t_tier"+ str(i):
						if ("g.evil>0" in tom_class_item['require']  and not("||g.evil>0" in tom_class_item['require'])) or "g.warlock>0" in tom_class_item['require'] or "g.reanimator>=1" in tom_class_item['require'] or "g.reanimation" in tom_class_item['require'] or "phylactory" in tom_class_item['require']:
							s.node(tom_class_item['name'].capitalize(), fillcolor='red', style='filled')
	good_subgraph=class_graph.subgraph(name='good')
	with good_subgraph as s:
		for i in range(0,tier_max+1):
			for tom_class_item in tom_class_list:
				for tag in tom_class_item['tags']:
					if tag is"t_tier"+ str(i):
						if "g.evil<=0" in tom_class_item['require'] or "g.evil==0" in tom_class_item['require']:
							s.node(tom_class_item['name'].capitalize(), fillcolor='cyan', style='filled')	


	
def tom_class_graph(tom_class_list=None):
	if tom_class_list is None:
		tom_class_list = []
		for json_value in result_list:
			tom_class_json = tom_class_info(json_value)
			tom_class_list.append(tom_class_json)
	tier_max=6

	class_graph = graphviz.Digraph(engine='dot')
	class_graph.attr(newrank="false", ranksep="2", fontsize="20", mclimit='10')
#	class_graph.attr(newrank="", ranksep="2", fontsize="20", mclimit='1', packMode="graph")
#	class_graph.attr(newrank="false", ranksep="2", fontsize="20", remincross='true')
	
	# The first node is usually on the top left corner (it is easier than forcing it using 'pos'). Let it be Apprenticeship and make the tier tree.	
	tier_tree = class_graph.subgraph(name='clusterT')
	with tier_tree as s:
		s.edge('Apprenticeship_tier', 'Job_tier')
		s.edge('Job_tier', 'Neophyte_tier')
		s.edge('Neophyte_tier','Tier0')
		for i in range(1,tier_max+1):
			s.edge(str('Tier' + str(i-1)), str('Tier' + str(i)))	
			
	#The links should be processed early, too.
	find_link(tom_class_list, class_graph)
	
	add_flavor(tom_class_list, class_graph, tier_max)
	
	#Let's add some more edges
	
	#############Apprenticeship_tier#############
	#(void)
	
	#############Job_tier#############
	for tom_class_item in tom_class_list:
		for tag in tom_class_item['tags']:
			if tag is"t_job":
				class_graph.edge("Apprenticeship", str(tom_class_item['name'].capitalize()))
		
	#############Neophyte_tier#############
	for tom_class_item in tom_class_list:
		for tag in tom_class_item['tags']:
			if tag is"t_job":
				class_graph.edge(str(tom_class_item['name'].capitalize()), "Neophyte")
					
	#############tier 0#############
	class_graph.edge("Neophyte", 'Adept')
	class_graph.edge("Neophyte", "Adept (murderer)")		#This is a dirty way to add "Adept (murderer)"	
					
	#############tier i#############
# Try to have them linked to the tier tree, so that they are more grouped. Linking a node defines it. 
#	for i in range(1,tier_max+1):		#There is another tier range in the rank_nodes function
#		for tom_class_item in tom_class_list:
#			for tag in tom_class_item['tags']:
#				if tag is"t_tier"+ str(i):
#					class_graph.edge('Tier' + str(i), str(tom_class_item['name'].capitalize()), style='dotted', weight='1')

#Another idea, to center the graph, would be to link all nodes of a rank to the ones above and under.
#The 'pack' attribute is probably the solution.

	rank_nodes(tom_class_list, class_graph, tier_max)

	class_graph.render(format="png", view=True)

def tom_class_info(tom_class_json):
#Get every information of a tom_class:
#ID, name, description, tags, cost, effect, requirement

	tom_class = {}
	tom_class['id'] = tom_class_json.get('id')
	if tom_class_json.get('name') is not None:
		tom_class['name'] = tom_class_json.get('name').title()
	else:
		tom_class['name'] = tom_class['id'].title()

	tom_class['sym'] = tom_class_json.get('sym')

	tom_class['desc'] = tom_class_json.get('desc')

	if tom_class_json.get('tags') is not None:
		tom_class['tags'] = tom_class_json.get('tags').split(",")
	else:
		tom_class['tags'] = []


	if tom_class_json.get('cost') is not None:
		tom_class['cost']  = tom_class_json.get('cost')
	else:
		tom_class['cost']  = {}
	
	tom_class['mod'] = {}
	tom_class['effect']  = {}
	if tom_class_json.get('mod') is not None:
		if isinstance(tom_class_json.get('mod'),dict):
			tom_class['mod'].update(tom_class_json.get('mod'))
		if isinstance(tom_class_json.get('mod'),str):
			tom_class['effect'][tom_class_json.get('mod')] = True
		else:
			tom_class['effect']  = {**tom_class['effect'], **tom_class_json.get('mod')}
	if tom_class_json.get('effect') is not None:
		if isinstance(tom_class_json.get('effect'),dict):
			tom_class['mod'].update(tom_class_json.get('effect'))
		if isinstance(tom_class_json.get('effect'),str):
			tom_class['effect'][tom_class_json.get('effect')] = True
		else:
			tom_class['effect']  = {**tom_class['effect'], **tom_class_json.get('effect')}		

	if tom_class_json.get('require') is not None:
		tom_class['require'] = tom_class_json.get('require')
	else: 
		tom_class['require'] = "Nothing"
	
	tom_class['requirements'] = {}
	tom_class['requirements']['>'] = {}
	tom_class['requirements']['<'] = {}
	requirements = tom_class['requirements']
	if tom_class_json.get('require') is not None:
		require = tom_class_json.get('require')
		if isinstance(require, list):
			for e in require:
				if not isinstance(e, dict):
					requirements['>'][e] = 1
				else:
					for ent in e:
						requirements['>'][ent] = e[ent]
		elif isinstance(require, dict):
			for e in require:
				requirements['>'][e] = require[e]
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

	return tom_class



def get_full_tom_class_list():
	result_list = lib.get_json("data/", "classes")
	tom_class_list = list()
	for json_value in result_list:
		tom_class_list.append(tom_class_info(json_value))
	return tom_class_list
	
def generate_individual_cls_page(cls):
	pass

def generate_wiki(main_only=False, no_graph_gen=False):
	global lists
	lists = {
		"action": action.get_full_action_list(),
		"dungeon": dungeon.get_full_dungeon_list(),
		"furniture": furniture.get_full_furniture_list(),
		"home": home.get_full_home_list(),
		"monster": monster.get_full_monster_list(),
		"potion": potion.get_full_potion_list(),
		"resource": resource.get_full_resource_list(),
		"skill": skill.get_full_skill_list(),
		"spell": spell.get_full_spell_list(),
		"class": tom_class.get_full_tom_class_list(),
		"upgrade": upgrade.get_full_upgrade_list()
		}
	ret = list()
	
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
		if tom_class_json.get('sym') is not None:
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
		
		if not main_only:
			generate_individual_cls_page(class_json)
			ret.append(resource_json['name'])

	with open("classes.txt", "w", encoding="UTF-8") as wiki_dump:
		wiki_dump.write('This page has been automatically updated the ' + str(datetime.datetime.now()) + "\n")
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
	
	if not no_graph_gen:
		tom_class_graph(tom_class_list)

	return ret