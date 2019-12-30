import os, json

def make_table(table_keys, table_lines, table_filter=None):
	"""
	table_filter should look like:
	[
		[5, "'gold.max' in cell"],
		[2, "'naturesource' in cell or 'plantesource' in cell"],...
	]
	"""
	table_return = ""
	table_return += '{| class="wikitable sortable"\n'
	table_return += '|-\n'
	for key in table_keys:
		table_return += '! ' + str(key) + ' !'
	table_return = table_return[:-2]
	table_return += '\n|-\n'
	if table_filter == None:
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
			if is_true == True:
				for cell in line:
					table_return += cell + ' || '
				table_return = table_return[:-4]
				table_return += '\n|-\n'
	table_return += '|}'
	return table_return