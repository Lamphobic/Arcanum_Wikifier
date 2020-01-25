import os, json, datetime
import pywikibot

def make_table(table_keys, table_lines, table_filter=None):
	"""
	table_filter should look like:
	[
		[5, "'gold.max' in cell"],
		[2, "'naturesource' in cell or 'plantesource' in cell"],...
	]
	Multiple filters are effectively boolean OR
	"""
	table_return = ""
	table_return += '{| class="wikitable sortable"\n'
	table_return += '|-\n'
	for key in table_keys:
		table_return += '! ' + str(key) + ' !'
	table_return = table_return[:-2]
	table_return += '\n|-\n'
	if table_filter is None:
		for line in table_lines:
			for cell in line:
				table_return += cell + ' || '
			table_return = table_return[:-4]
			table_return += '\n|-\n'
	else:
		for line in table_lines:
			is_true = False
			for filter_eval in table_filter:
				cell = line[filter_eval[0]]
				if eval(filter_eval[1]):
					is_true = True
			if is_true is True:
				for cell in line:
					table_return += cell + ' || '
				table_return = table_return[:-4]
				table_return += '\n|-\n'
	table_return += '|}'
	return table_return

def bot_update(page_name, file_name):
	with open(file_name, "r", encoding="UTF-8") as wiki_dump:
		site = pywikibot.Site()  # The site we want to run our bot on
		page = pywikibot.Page(site, page_name)
		page.text = wiki_dump.read()
		page.save('Automatic update from: ' + str(datetime.datetime.now()))  # Saves the page
