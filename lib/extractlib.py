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
            if k is key:
                yield v
            if isinstance(v, dict):
                for result in gen_dict_extract(key, v):
                    yield result
            elif isinstance(v, list):
                for d in v:
                    for result in gen_dict_extract(key, d):
                        yield result

def get_json(path_to_json, target_name):
    json_files = [pos_json for pos_json in os.listdir(path_to_json) if pos_json.endswith('.json')]
    json_dict = {}

    # we need both the json and an index number so use enumerate()
    for index, js in enumerate(json_files):
        with open(os.path.join(path_to_json, js), 'r', encoding='utf8', errors='ignore') as json_file:
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

    main_json = json_dict[target_name + ".json"]

    return result_list + main_json