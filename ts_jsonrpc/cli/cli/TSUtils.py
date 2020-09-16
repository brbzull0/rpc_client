
def fix_match_all(elements):
    print("elements {}".format(elements))
    for pos, val in enumerate(elements):
        print("input {}".format(val))
        if val == "*":
            elements[pos] = ".*"


def class_to_string(rec_class):
    if rec_class == "1":
        return 'CONFIG'
    elif rec_class == "16":
        return 'LOCAL'
    else:
        return 'UNKNOWN'


rec_types_dict = {'0': 'NULL', '1': 'INT', '2': 'FLOAT', '3': 'STRING', '4': 'COUNTER'}


def type_to_string(record_type):
    if record_type in rec_types_dict:
        return rec_types_dict[record_type]
    else:
        return 'UNDEFINED'


access_control_dict = {'0': 'default', '1': 'no access', '2': 'read only'}


def access_control_to_string(rec_access):
    if rec_access in access_control_dict:
        return access_control_dict[rec_access]
    else:
        return access_control_dict['0']


update_type_dict = {
    '0': 'none',
    '1': 'dynamic, no restart',
    '2': 'static, restart traffic_server',
    '3': 'static, restart traffic_manager'}


def update_type_to_string(rec_update):
    if rec_update in update_type_dict:
        return update_type_dict[rec_update]
    else:
        return update_type_dict['0']


source_string_dict = {'1': 'built in default', '2': 'plugin default', '3': 'administratively set', '4': 'environment'}


def source_to_string(rec_source):
    if rec_source in source_string_dict:
        return source_string_dict[rec_source]
    else:
        return 'unknown'


syntax_check_dict = {'1': 'string matching a regular expression', '2': 'integer with a specified rang', '3': 'IP address'}


def syntax_check_to_string(syntax_check):
    if syntax_check in syntax_check_dict:
        return syntax_check_dict[syntax_check]
    else:
        return 'none'
