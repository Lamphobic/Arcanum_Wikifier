import os, json

class Any(object):
    def __eq__(self, other):
        return True
ANYTHING = Any()


def recurs_json_to_str(json_value):
    return_txt = ""

    if isinstance(json_value, str) or isinstance(json_value, int):
        return_txt += str(json_value) +","
    elif isinstance(json_value, list):
        for array_value in json_value:
            return_txt += recurs_json_to_str(array_value) +","
    elif isinstance(json_value, dict):
        for dict_key in json_value:
            if isinstance(json_value[dict_key], str):
                return_txt += str(dict_key) + ": " + str(json_value[dict_key]) +","
            else:
                return_txt += str(dict_key) + ": " + recurs_json_to_str(json_value[dict_key]) +","
    else:
        print("error: " + str(json_value))
    return return_txt[:-1]


def gen_dict_extract(key, var):
    if hasattr(var,'items'):
        for k, v in var.items():
            if k == key:
                yield v
            if isinstance(v, dict):
                for result in gen_dict_extract(key, v):
                    yield result
            elif isinstance(v, list):
                for d in v:
                    for result in gen_dict_extract(key, d):
                        yield result

						
def name_exceptions(map):
	exceptions = {
		'up_apprentice': 'Apprentice(Upgrade)',
		'apprentice': 'Apprentice(Class)',
		'm_avatar': 'Avatar(Monster)',
		'c_avatar': 'Avatar(Class)',
		'clockworkexpansion2': 'Clockwork Expansion 2',
		'clockworkexpansion': 'Clockwork Expansion 1',
		'clockworkexpansion3': 'Clockwork Expansion 3',
		'm_druid': 'Druid(Monster)',
		'druid': 'Druid(Class)',
		'garden': 'Garden(Furniture)',
		'act_garden': 'Garden(Task)',
		'gryffonmount': 'Gryffon(Upgrade)',
		'gryffon': 'Gryffon(Monster)',
		'up_lich': 'Lich(Upgrade)',
		'm_lich': 'Lich(Monster)',
		'mana3': 'Mana(Spell)',
		'mana': 'Mana(Resource)',
		'pegasusmount': 'Pegasus(Upgrade)',
		'pegasus': 'Pegasus(Monster)',
		'pot_poisonward': 'Poison Ward(Potion)',
		'poisonward': 'Poison Ward(Spell)',
		'smchest': 'Small Chest(Monster)',
		'smbox': 'Small Chest(Furniture)',
		'studyroom': 'Study(Skill)',
		'study': 'Study(Task)',
		's_travel': 'Travel(Skill)',
		'a_travel': 'Travel(Task)',
		'good_sacrifice': 'Winter Fog(Good)',
		'evil_sacrifice': 'Winter Fog(Evil)'
		}
	if map['id'] in exceptions:
		map['name'] = exceptions[map['id']]

						
def get_json(path_to_json, target_name):
    
    with open(path_to_json + "/modules.json", "r", encoding="UTF-8") as module_file:
        module_json = json.load(module_file)
        json_files = []

        for key, value in module_json.items():
            if key == "core":
                for module_name in value:
                    json_files.append(module_name)
            elif key == "modules":
                for module_name in value:
                    json_files.append("modules/" + module_name)

    json_dict = {}

    for js in json_files:
        with open(os.path.join(path_to_json, js + ".json"), 'r', encoding='utf8', errors='ignore') as json_file:
            json_dict[js] = json.load(json_file)

    tmp_json = []
    result_list = []
    for json_source in json_dict:
        unencapsulated_json = json_dict[json_source]
        while type(unencapsulated_json) is not dict and unencapsulated_json:
            unencapsulated_json = unencapsulated_json[0]
        if not unencapsulated_json:
            continue
        evt_sym = unencapsulated_json.get("sym")
        tmp_return = [result for result in gen_dict_extract(target_name, unencapsulated_json)]
        if tmp_return:
            for object_json in tmp_return[0]:
                object_json['sym'] = evt_sym
            tmp_json += tmp_return

    for json_found in tmp_json:
        result_list += json_found 
    #tmp_json = [result for result in gen_dict_extract(target_name, json_dict)][0]

    main_json = json_dict[target_name]
    
    return result_list + main_json